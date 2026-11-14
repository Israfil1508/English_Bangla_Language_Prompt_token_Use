# Assignment 2: Requirement Traceability and Research Design

## Main goal
Measure how much English versus Bangla **semantically equivalent prompts** differ in Ollama-reported prompt tokens, completion tokens, hypothetical costs, latency, and response quality with `qwen3.5:4b` (digest prefix `d8b0f5e9760c`).

## Requirements-to-code matrix

| ID | Assignment requirement | Implemented in | How to verify | Priority |
|---|---|---|---|---|
| R01 | 50 aligned English and Bangla prompts | `data/dataset.tsv` | `test_dataset.py` and human translation review | Mandatory |
| R02 | Prompt variety, paired fields | `data/dataset.tsv` | Category distribution check | Mandatory |
| R03 | Ollama token counts, not character estimates | `metrics/token_counter.py` | `test_token_counter.py` | Mandatory |
| R04 | Fixed system prompt/template overhead discussion | `config.py`, `experiment/cache_controller.py` | `overhead` CLI and report notes | Mandatory |
| R05 | Cache/repeated-request issue addressed | `experiment/cache_controller.py` | Repeat reference calls, report limits | Mandatory |
| R06 | Equal model/settings for both languages | `llm/ollama_client.py` | `test_ollama_client.py` | Mandatory |
| R07 | One result per call with token/cost/latency | `experiment/runner.py` | `test_experiment_runner.py` | Mandatory |
| R08 | Input $0.15/M, output $0.60/M notional | `metrics/cost_calculator.py` | `test_cost_calculator.py` | Mandatory |
| R09 | 50 paired ratio records | `metrics/comparison.py` | `test_full_pipeline.py` + formal run | Mandatory |
| R10 | Totals, mean, median, min, max, 95% interval | `analysis/statistics.py`, `analysis/bootstrap.py` | `test_bootstrap.py` + full run | Mandatory |
| R11 | Category, surprising example, quality of 10 pairs | `analysis/category_analysis.py`, `data/quality_review.csv` | Manual scoring and `test_quality_analysis.py` | Mandatory |
| R12 | At least one chart | `visualization/charts.py` | `test_full_pipeline.py` | Mandatory |
| R13 | 1–2 page report, CSVs, README | `reports/`, `results/`, `README.md` | Inspect output artifacts | Mandatory |
| R14 | Tests with fake backend | `tests/` | `pytest -q` | Mandatory |
| R15 | Second model tokenizer comparison | Not included | Optional future extension | Bonus |

## Scoring rubric (100 points)
- Dataset correctness and variety: **20**.
- Token counts, template overhead and caching methodology: **20**.
- Matched settings, runner and saved results: **20**.
- Cost calculations, pair comparison and spread: **20**.
- Analysis, chart and honest interpretation: **15**.
- Reproducibility: **5**.
- Optional second model comparison: up to **5 bonus**.

## Research hypotheses (to test, not assume)
H1: Input tokens differ by language for semantically equivalent prompts.
H2: Different token use affects hypothetical cost.
H3: Magnitude of differences varies by prompt category and length.
H4: Token cost is not a substitute for answer quality.

## Dataset categories
10 factual, 10 instructions, 10 explanations, 8 arithmetic, 7 summarizations, 5 longer prompts = **50 pairs**.

## Experimental protocol
- Record the Ollama tag and model digest from `ollama list` / `/api/tags` before the experiment.
- Use Python 3.11+, local Windows 11, same fixed model and system prompt.
- Independent per-prompt chat messages; seeded randomized pair/language ordering.
- Conduct reference prompt repetitions (`overhead`) and disclose caching uncertainty.
- Collect both token fields from Ollama; compute full precision hypothetical cost.
- Mark errors and truncated generations rather than turning them into zero-token successes.
- Use completed aligned pairs only for paired metrics.
- Bootstrap a 95% interval for the **mean of pairwise input-token ratios** with seed 2026.
- Separately compute the **ratio of total input tokens**; do not confuse the two estimators.
- Review ten selected output pairs manually and document possible translation adjustments before formal measurement.
- State that measurements apply to this particular model/dataset, not to all languages or LLMs.

## Implementation order and test-first practice
Write or approve tests, observe the initial failure, implement minimal behavior, and rerun tests, repeating for loader → API client → metrics → runner → comparison → statistics → plots → report. The supplied code and tests are a starting implementation. The student must review and approve them, verify on their own machine, and document that review in the AI assistance log.
