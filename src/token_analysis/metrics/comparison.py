from __future__ import annotations
import csv
from decimal import Decimal
from pathlib import Path

COMPARISON_FIELDS = ["id", "category", "english_input_tokens", "bangla_input_tokens",
                     "english_output_tokens", "bangla_output_tokens", "english_total_tokens",
                     "bangla_total_tokens", "english_cost_usd", "bangla_cost_usd",
                     "english_latency_s", "bangla_latency_s", "input_token_ratio",
                     "output_token_ratio", "total_cost_ratio", "latency_ratio"]


def safe_ratio(numerator, denominator):
    den = Decimal(str(denominator))
    if den == 0:
        return None
    return float(Decimal(str(numerator)) / den)


def make_comparisons(raw_path: Path, comparison_path: Path) -> dict:
    with Path(raw_path).open(encoding="utf-8-sig", newline="") as stream:
        records = list(csv.DictReader(stream))
    # The most recent successful record wins when failed attempts were retried.
    indexed = {}
    for record in records:
        if record.get("response_status") == "ok":
            indexed[(record["id"], record["language"])] = record
    ids = sorted({r["id"] for r in records})
    comparisons = []
    for pair_id in ids:
        en, bn = indexed.get((pair_id, "english")), indexed.get((pair_id, "bangla"))
        if not en or not bn:
            continue
        row = {"id": pair_id, "category": en["category"]}
        for language, record in (("english", en), ("bangla", bn)):
            for key in ("input_tokens", "output_tokens", "total_tokens", "cost_usd", "latency_s"):
                row[f"{language}_{key}"] = record[key]
        for name, field in (("input_token_ratio", "input_tokens"),
                            ("output_token_ratio", "output_tokens"),
                            ("total_cost_ratio", "cost_usd"), ("latency_ratio", "latency_s")):
            ratio = safe_ratio(bn[field], en[field])
            row[name] = "" if ratio is None else ratio
        comparisons.append(row)
    comparison_path = Path(comparison_path)
    comparison_path.parent.mkdir(parents=True, exist_ok=True)
    with comparison_path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=COMPARISON_FIELDS)
        writer.writeheader()
        writer.writerows(comparisons)
    return {"pairs_compared": len(comparisons), "pairs_in_raw_results": len(ids),
            "missing_pairs": len(ids) - len(comparisons)}
