from __future__ import annotations
import csv
import json
import random
from datetime import datetime, timezone
from pathlib import Path
from token_analysis.config import ExperimentConfig
from token_analysis.dataset.dataset_loader import PromptPair
from token_analysis.metrics.cost_calculator import calculate_input_cost, calculate_output_cost, calculate_total_cost

FIELDS = ["id", "category", "language", "prompt", "output", "input_tokens", "output_tokens",
          "total_tokens", "input_cost_usd", "output_cost_usd", "cost_usd", "latency_s",
          "model", "temperature", "seed", "max_output_tokens", "run_order", "done_reason",
          "response_status", "error", "timestamp", "prompt_eval_duration_ns", "eval_duration_ns"]


def make_run_order(pairs: list[PromptPair], seed: int) -> list[tuple[PromptPair, str]]:
    """Alternate language order while preserving pair identity."""
    rng = random.Random(seed)
    ordered = pairs[:]
    rng.shuffle(ordered)
    requests_to_run = []
    for pair in ordered:
        languages = ["english", "bangla"]
        rng.shuffle(languages)
        requests_to_run.extend((pair, language) for language in languages)
    return requests_to_run


def existing_successes(path: Path, config: ExperimentConfig) -> set[tuple[str, str]]:
    if not path.exists():
        return set()
    with path.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    for row in rows:
        if (row.get("model") != config.model or
            row.get("seed") != str(config.seed) or
            row.get("max_output_tokens") != str(config.num_predict) or
            row.get("temperature") != str(config.temperature)):
            raise ValueError("Existing results use different settings; use --fresh or a new results path")
    return {(r["id"], r["language"]) for r in rows
            if r.get("response_status") == "ok"}


def run_experiment(pairs: list[PromptPair], client, config: ExperimentConfig,
                   output_path: Path, max_pairs: int | None = None, resume: bool = True) -> dict:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    selected = pairs[:max_pairs] if max_pairs is not None else pairs
    order = make_run_order(selected, config.seed)
    successful = existing_successes(output_path, config) if resume else set()
    mode = "a" if resume and output_path.exists() else "w"
    attempts = failures = skipped = 0
    with output_path.open(mode, encoding="utf-8-sig" if mode == "w" else "utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        if mode == "w" or output_path.stat().st_size == 0:
            writer.writeheader()
        for index, (pair, language) in enumerate(order, start=1):
            key = (pair.id, language)
            if key in successful:
                skipped += 1
                continue
            prompt = getattr(pair, language)
            row = {key: "" for key in FIELDS}
            row.update(id=pair.id, category=pair.category, language=language, prompt=prompt,
                       model=config.model, temperature=config.temperature, seed=config.seed,
                       max_output_tokens=config.num_predict, run_order=index,
                       timestamp=datetime.now(timezone.utc).isoformat())
            attempts += 1
            try:
                result = client.generate(prompt)
                row.update(output=result.output, input_tokens=result.input_tokens,
                           output_tokens=result.output_tokens,
                           total_tokens=result.input_tokens + result.output_tokens,
                           input_cost_usd=str(calculate_input_cost(result.input_tokens)),
                           output_cost_usd=str(calculate_output_cost(result.output_tokens)),
                           cost_usd=str(calculate_total_cost(result.input_tokens, result.output_tokens)),
                           latency_s=f"{result.latency_s:.6f}", done_reason=result.done_reason,
                           prompt_eval_duration_ns=result.prompt_eval_duration_ns,
                           eval_duration_ns=result.eval_duration_ns,
                           response_status="ok" if result.done_reason != "length" else "truncated")
                # Length-truncated responses are retained, but excluded from complete comparisons.
                if row["response_status"] != "ok":
                    failures += 1
            except Exception as exc:
                row.update(response_status="error", error=f"{type(exc).__name__}: {exc}")
                failures += 1
            writer.writerow(row)
            stream.flush()
    return {"attempted": attempts, "failed_or_truncated": failures, "skipped": skipped,
            "total_planned": len(order), "output": str(output_path)}
