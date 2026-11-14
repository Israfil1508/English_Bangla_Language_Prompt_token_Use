# English vs Bangla Token Cost Analysis Using Qwen3.5:4B via Ollama

**Status:** Experimental results pending execution on the local Windows 11 PC. Replace bracketed placeholders only after running the model.

## Introduction and objective
Measure tokenization and notional inference cost differences between 50 drafted, subject-to-human-review, semantically aligned English–Bangla prompts across six categories, using a fixed local model and settings.

## Method
Model: `qwen3.5:4b` (digest prefix: `d8b0f5e9760c`). Ollama `/api/chat`, temperature 0, seed 2026, maximum generated tokens 160, identical fixed system prompt. Independent message lists and seeded pair/language ordering. Input/output tokens are Ollama `prompt_eval_count`/`eval_count`. Template overhead is documented with a repeated reference prompt; fully cold caches are not guaranteed. Interrupted/failed/truncated results are excluded from complete-pair metrics.

## Results (fill from `results/processed/summary.json`)
| Metric | Result |
|---|---|
| Complete pairs | [pending] |
| English input / output tokens | [pending] / [pending] |
| Bangla input / output tokens | [pending] / [pending] |
| English / Bangla notional USD | [pending] / [pending] |
| Overall input token ratio | [pending] |
| Overall total cost ratio | [pending] |
| Mean / median pairwise input ratio | [pending] / [pending] |
| Min / max pairwise input ratio | [pending] / [pending] |
| Bootstrap 95% CI for mean ratio | [pending] |
| Mean latency by language | [pending] |

**Figure:** Insert `results/charts/input_tokens_by_pair.png` after completing the experiment.

## Quality review
10 stratified sample pairs in `data/quality_review.csv` require human correctness and usefulness scoring (0–2 each). Results: [pending human review].

## Category analysis and surprising case
Largest/smallest gap: [pending]. Unexpected ratio example and explanation: [pending].

## Discussion, limitations and conclusion
These findings apply to the chosen dataset, model, tokenizer and settings only. Prompt cache state and system/chat-template overhead may affect measurements; output truncation and quality differences must be reported. The USD amounts are hypothetical, not actual local API charges. **Conclusion:** [write from measured results].
