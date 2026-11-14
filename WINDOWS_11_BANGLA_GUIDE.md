# Windows 11 বাংলা গাইড — Assignment 2

## ১. মূল লক্ষ্য
একই অর্থের ৫০টি English ও ৫০টি Bangla prompt Ollama-তে পাঠিয়ে input/output tokens, কাল্পনিক cost, response latency এবং quality তুলনা করা। ১০০টি live call তোমার Windows 11 laptop-এ চালাতে হবে।

## ২. প্রয়োজনীয় লাইব্রেরি
| Tool | কাজ | ধরন |
|---|---|---|
| Python | মূল ভাষা | প্রয়োজনীয় |
| Ollama + qwen3.5:4b | লোকাল মডেল | প্রয়োজনীয় |
| requests | HTTP API | প্রয়োজনীয় |
| pytest | automated test | প্রয়োজনীয় |
| pandas | comparison data | analysis সুবিধা |
| numpy | numerical dependencies | analysis সুবিধা |
| matplotlib | chart | প্রয়োজনীয় chart-এর জন্য |
| python-dotenv | .env settings | configuration |
| csv,json,random,statistics,time,pathlib | file/metric utilities | Python built-in |

## ৩. চালানোর নিয়ম
VS Code-এ project folder খুলে PowerShell terminal-এ:

```powershell
python --version
ollama --version
ollama list
ollama pull qwen3.5:4b
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -e .
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m token_analysis.main validate
.\.venv\Scripts\python.exe -m token_analysis.main check
.\.venv\Scripts\python.exe -m token_analysis.main overhead
.\.venv\Scripts\python.exe -m token_analysis.main smoke
.\.venv\Scripts\python.exe -m token_analysis.main run --fresh
.\.venv\Scripts\python.exe -m token_analysis.main analyze
```

**সতর্কতা:** `run --fresh` দিলে আগের `results.csv` overwrite হবে। প্রথমে ২ pair smoke test করো, এরপর formal run শুরু করো।

## ৪. ফাইলগুলো কী করে
- `data/dataset.tsv`: ৫০টি English–Bangla pair; অর্থ মিলিয়ে নিজে review করবে।
- `src/token_analysis/llm/ollama_client.py`: Ollama API request ও actual token metadata।
- `experiment/runner.py`: call order, retry/resume ও results.csv লেখা।
- `metrics/token_counter.py`: `prompt_eval_count`, `eval_count`।
- `metrics/cost_calculator.py`: কাল্পনিক USD cost।
- `metrics/comparison.py`: pair matching ও token/cost ratio।
- `analysis/statistics.py`: overall/category totals ও 95% bootstrap CI।
- `visualization/charts.py`: chart PNG ফাইল।
- `tests/`: fake-model based unit tests।
- `reports/final_report.md`: actual results বসানোর template।

## ৫. খরচের সূত্র
Input cost = input tokens × 0.15 / 1,000,000। Output cost = output tokens × 0.60 / 1,000,000। Total = দুটো যোগ। এটি বাস্তব টাকা কাটা নয়।

## ৬. Experiment-এর গুরুত্বপূর্ণ সীমাবদ্ধতা
- Ollama cache নিশ্চিতভাবে off করা হয়নি। `overhead` command reference prompt repeat করে; রিপোর্টে লিখবে।
- কোনো generated result বানানো হয়নি। `run` command দিয়ে live token/latency সংগ্রহ করতে হবে।
- quality_review.csv-এর দশটি pair-এর মান নিজে যাচাই ও score করবে।
- `reports/final_report.md`-এ প্রকৃত সংখ্যা, একটি chart, সবচেয়ে বড় gap ও surprising case যোগ করবে।
- সব prompt-এর উত্তর যদি `length` দিয়ে শেষ হয়, `OLLAMA_NUM_PREDICT` বাড়ানোর আগে সেটিং ও পরীক্ষার নীতি লিখে রাখবে।
