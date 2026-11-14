"""Exercise CSV collection, pair comparison, statistics and plotting without Ollama."""
from token_analysis.config import ExperimentConfig
from token_analysis.dataset.dataset_loader import PromptPair
from token_analysis.experiment.runner import run_experiment
from token_analysis.llm.ollama_client import LLMResponse
from token_analysis.metrics.comparison import make_comparisons
from token_analysis.analysis.statistics import summarize
from token_analysis.visualization.charts import generate_charts

class FakeClient:
    def generate(self, prompt):
        count = 12 if any("\u0980" <= ch <= "\u09ff" for ch in prompt) else 6
        return LLMResponse("Test output", count, 5, 0.1, 100, 200, "stop")


def test_pipeline(tmp_path):
    pair = [PromptPair("P01", "factual", "Hello?", "হ্যালো?")]
    raw = tmp_path / "results.csv"
    comparison = tmp_path / "comparison.csv"
    run_experiment(pair, FakeClient(), ExperimentConfig(), raw)
    stats = make_comparisons(raw, comparison)
    assert stats["pairs_compared"] == 1
    summary = summarize(comparison)
    assert summary["overall_input_token_ratio"] == 2.0
    assert len(generate_charts(comparison, tmp_path / "charts")) == 5
