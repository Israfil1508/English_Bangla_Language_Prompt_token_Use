"""Generate a results-grounded report draft without inventing quality judgments."""
from pathlib import Path
from token_analysis.analysis.category_analysis import rank_categories
from token_analysis.analysis.quality_analysis import completed_reviews, load_quality_review


def generate_report(summary: dict, review_path: Path, output_path: Path) -> Path:
    totals = summary["language_totals"]
    english = totals["english"]
    bangla = totals["bangla"]
    ratios = summary["pairwise_input_ratios"]
    ranking = rank_categories(summary)
    highest = ranking[0][0] if ranking else "pending"
    lowest = ranking[-1][0] if ranking else "pending"
    reviewed = completed_reviews(load_quality_review(review_path))
    quality_status = (f"{len(reviewed)} of 10 reviews completed."
                      if len(reviewed) == 10 else
                      f"Human review pending: {len(reviewed)}/10 completed.")
    text = f"""# English vs Bangla Token Cost Analysis Using Qwen3.5:4B

## Objective and methodology
Compare aligned English and Bangla prompts across six categories using the same local
Ollama model, fixed system prompt and generation settings. Input/output tokens come
from Ollama rather than character estimates. Requests are independent but cold cache
state is not guaranteed. The selected sample is not representative of all Bangla text.

## Measured results (completed pairs only)

| Measure | English | Bangla |
|---|---:|---:|
| Input tokens | {english['input_tokens']} | {bangla['input_tokens']} |
| Output tokens | {english['output_tokens']} | {bangla['output_tokens']} |
| Notional cost (USD) | {english['cost_usd']:.8f} | {bangla['cost_usd']:.8f} |
| Mean latency (seconds) | {english['mean_latency_s']:.3f} | {bangla['mean_latency_s']:.3f} |

- Completed pairs: {summary['complete_pairs']}/50.
- Total input-token ratio: {summary['overall_input_token_ratio']:.4f}.
- Total cost ratio: {summary['overall_total_cost_ratio']:.4f}.
- Mean pairwise input ratio: {ratios['mean']:.4f}.
- Median pairwise input ratio: {ratios['median']:.4f}.
- Minimum / maximum ratio: {ratios['minimum']:.4f} / {ratios['maximum']:.4f}.
- Bootstrap 95% interval for the mean pairwise input ratio:
  [{ratios['bootstrap_95_ci_for_mean'][0]:.4f}, {ratios['bootstrap_95_ci_for_mean'][1]:.4f}].
- Highest input-token ratio category: {highest}.
- Lowest input-token ratio category: {lowest}.

## Quality check
{quality_status} Review English and Bangla outputs for correctness and usefulness,
recording manual scores in `data/quality_review.csv`.

## Figures and interpretation
Insert `results/charts/input_tokens_by_pair.png`. Identify an actual surprising
pair from `comparison.csv` and discuss tokenizer segmentation, source-prompt length,
and output-language differences. These are hypotheses, not proven causal factors.

## Limitations and conclusion
Tokens include system prompt and template overhead. Request order is seeded, but
runtime caching, hardware load and model versions may affect latency. The provided
costs are **hypothetical**, not bills for local inference. Do not submit this report
before dataset translation review, manual quality scoring, the complete formal run,
and the interpretation of one surprising pair.
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")
    return output_path
