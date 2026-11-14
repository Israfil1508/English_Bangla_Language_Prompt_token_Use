from token_analysis.config import ExperimentConfig
from token_analysis.llm.ollama_client import OllamaClient

class FakeResponse:
    def raise_for_status(self):
        pass
    def json(self):
        return {"message": {"content": "Fine"}, "prompt_eval_count": 18,
                "eval_count": 3, "done_reason": "stop"}

class FakeSession:
    def __init__(self):
        self.body = None
    def post(self, url, json, timeout):
        self.body = json
        return FakeResponse()


def test_same_fixed_settings_and_counts():
    session = FakeSession()
    config = ExperimentConfig()
    reply = OllamaClient(config, session).generate("Hello")
    assert (reply.input_tokens, reply.output_tokens) == (18, 3)
    assert session.body["options"] == config.options
    assert session.body["messages"][0]["role"] == "system"


def test_assignment_uses_required_default_model(monkeypatch):
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)
    assert ExperimentConfig().model == "qwen3.5:4b"
