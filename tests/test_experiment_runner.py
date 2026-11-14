import csv
from token_analysis.config import ExperimentConfig
from token_analysis.dataset.dataset_loader import PromptPair
from token_analysis.experiment.runner import run_experiment
from token_analysis.llm.ollama_client import LLMResponse

class FakeClient:
    def __init__(self):
        self.prompts = []
    def generate(self, prompt):
        self.prompts.append(prompt)
        return LLMResponse("ok", 20, 5, 0.01, 100, 200, "stop")


def test_runner_and_resume(tmp_path):
    pairs = [PromptPair("P01", "factual", "Hello", "হ্যালো")]
    file = tmp_path / "results.csv"
    client = FakeClient()
    first = run_experiment(pairs, client, ExperimentConfig(), file)
    second = run_experiment(pairs, client, ExperimentConfig(), file)
    assert first["attempted"] == 2
    assert second["skipped"] == 2
    with file.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    assert {r["language"] for r in rows} == {"english", "bangla"}
