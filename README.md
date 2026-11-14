# Assignment 2 — English vs Bangla Token Cost Analysis

A local, reproducible **Windows 11 / VS Code / Ollama** experiment with 50 paired prompts, real Ollama token counts, hypothetical costs, paired statistics, bootstrap CI, charts and tests. **Live results are not included**; run Ollama locally to produce them.

## Research design
- 50 aligned pairs, six categories; review each translation before final measurement.
- `qwen3.5:4b` (digest prefix `d8b0f5e9760c`), same system prompt, temperature 0, seed 2026, `num_predict=160`, fresh per-call message lists.
- Token metadata: `prompt_eval_count` and `eval_count` from Ollama `/api/chat`.
- Notional USD: input $0.15/million, output $0.60/million (not an actual bill).
- Seeded randomized pair order and language order; reproducible sequence, but GPU/hardware latency and cache state can still vary.
- No guaranteed cold cache: record reference prompt repetitions with `overhead`.

## Windows 11 prerequisites
Install Python 3.11+, VS Code, Ollama. Pull the model once:

```powershell
ollama pull qwen3.5:4b
ollama list
```

## Five-command reproducibility workflow (after prerequisites)
Open the project folder in PowerShell and run:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -e .
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m token_analysis.main run
.\.venv\Scripts\python.exe -m token_analysis.main analyze
```

Optional diagnostics (run before the full experiment):

```powershell
.\.venv\Scripts\python.exe -m token_analysis.main check
.\.venv\Scripts\python.exe -m token_analysis.main validate
.\.venv\Scripts\python.exe -m token_analysis.main overhead
.\.venv\Scripts\python.exe -m token_analysis.main smoke
```

**Important:** smoke writes to `results/raw/results.csv`; `run` resumes remaining records. To start the formal experiment from scratch run `run --fresh`. Avoid mixing smoke measurements and a formal experiment unless settings and hardware are unchanged.

### Outputs
- `data/dataset.tsv`: 50 aligned prompt pairs, manually review before submission.
- `results/raw/results.csv`: per-call prompt, response, counts, cost, elapsed time and errors.
- `results/processed/comparison.csv`: one completed row per aligned pair.
- `results/processed/summary.json`: totals, ratios, bootstrap interval, category statistics.
- `results/charts/*.png`: five figures based on actual data.
- `data/quality_review.csv`: 10 review slots; manually fill correctness/usefulness 0–2.
- `reports/final_report.md`: 1–2 page **template**, fill with verified results.
- `reports/generated_report.md`: automatically generated grounded draft after `analyze`; manual quality review and interpretation still required.

### Interpretation
Overall input-token ratio = sum(Bangla input) / sum(English input). Mean pairwise ratio = mean(Bangla input per pair / English input per pair); **these are distinct**. Bootstrap CI represents the mean of pairwise input ratios. The model may stop due to length, so the runner marks `done_reason=length` as truncated and excludes these rows from completed pairs. Increase `OLLAMA_NUM_PREDICT` in `.env` and rerun if truncation makes the evaluation incomplete; record that setting.

### Current limitations
Ollama's cache cannot be guaranteed cleared via this project. No live runs are claimed here. Human bilingual equivalence and the 10 quality reviews remain student responsibilities. A full experiment requires 100 successful calls; investigate any errors or truncations. If a prior failed attempt is retried, the most recent successful record is used in analysis. Failure entries remain in the audit log.

### Troubleshooting
- `ollama` not found: install Ollama for Windows, reopen terminal.
- Cannot connect to 127.0.0.1:11434: start Ollama, then retry `check`.
- Model not found: `ollama pull qwen3.5:4b`.
- PowerShell activation blocked: activation is unnecessary; use `.venv\Scripts\python.exe` directly.
- `No module named token_analysis`: run `pip install -e .` using the venv Python.
- Bangla text looks wrong: open UTF-8 TSV in VS Code with a Bangla-capable font.
- Memory pressure: close large programs and keep sequential execution.
- `No complete comparisons`: complete model calls and verify `results/raw/results.csv` before analysis.
