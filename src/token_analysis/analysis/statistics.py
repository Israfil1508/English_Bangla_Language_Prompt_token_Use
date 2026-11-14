import csv
import statistics
from collections import defaultdict
from pathlib import Path
from token_analysis.analysis.bootstrap import bootstrap_mean_interval
from token_analysis.metrics.comparison import safe_ratio


def summarize(comparison_path: Path, seed: int = 2026) -> dict:
    with Path(comparison_path).open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError("No complete comparisons exist; run the experiment first")
    ratios = [float(r["input_token_ratio"]) for r in rows if r["input_token_ratio"]]
    if not ratios:
        raise ValueError("No defined pairwise input ratios")
    totals = {}
    for language in ("english", "bangla"):
        totals[language] = {
            "input_tokens": sum(int(row[f"{language}_input_tokens"]) for row in rows),
            "output_tokens": sum(int(row[f"{language}_output_tokens"]) for row in rows),
            "cost_usd": sum(float(row[f"{language}_cost_usd"]) for row in rows),
            "mean_latency_s": statistics.fmean(float(row[f"{language}_latency_s"]) for row in rows),
        }
    groups = defaultdict(list)
    for row in rows:
        groups[row["category"]].append(row)
    category_results = {}
    for category, group in sorted(groups.items()):
        en = sum(int(r["english_input_tokens"]) for r in group)
        bn = sum(int(r["bangla_input_tokens"]) for r in group)
        ec = sum(float(r["english_cost_usd"]) for r in group)
        bc = sum(float(r["bangla_cost_usd"]) for r in group)
        category_results[category] = {"pairs": len(group), "english_input_tokens": en,
            "bangla_input_tokens": bn, "input_token_ratio": safe_ratio(bn, en),
            "total_cost_ratio": safe_ratio(bc, ec)}
    return {
        "complete_pairs": len(rows), "language_totals": totals,
        "overall_input_token_ratio": safe_ratio(totals["bangla"]["input_tokens"], totals["english"]["input_tokens"]),
        "overall_total_cost_ratio": safe_ratio(totals["bangla"]["cost_usd"], totals["english"]["cost_usd"]),
        "pairwise_input_ratios": {"mean": statistics.fmean(ratios), "median": statistics.median(ratios),
           "minimum": min(ratios), "maximum": max(ratios),
           "bootstrap_95_ci_for_mean": bootstrap_mean_interval(ratios, seed=seed)},
        "categories": category_results,
    }
