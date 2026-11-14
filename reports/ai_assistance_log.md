# AI Assistance Log

1. **What the assistant wrote:** Updated the chart generator for current Matplotlib boxplot tick labels, returned all five chart paths, and aligned the default Ollama model/documentation with the selected `qwen3.5:4b` model (digest prefix `d8b0f5e9760c`).
2. **Which tests prove it:** `python -m pytest -q` passed all 17 tests, including the full fake-client pipeline and the required-model regression test; dataset validation passed for 50 aligned pairs.
3. **What I reviewed:** I reviewed the changed chart/config/report documentation, the generated-file contract, the fixed settings, and the assignment constraints; real Ollama outputs and the 10 human quality scores still require student review after the formal run.
