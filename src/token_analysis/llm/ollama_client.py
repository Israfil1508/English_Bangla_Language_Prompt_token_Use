from __future__ import annotations
from dataclasses import dataclass
import time
import requests
from token_analysis.config import ExperimentConfig
from token_analysis.metrics.token_counter import parse_counts
from token_analysis.utils.exceptions import ModelResponseError

@dataclass(frozen=True)
class LLMResponse:
    output: str
    input_tokens: int
    output_tokens: int
    latency_s: float
    prompt_eval_duration_ns: int | None
    eval_duration_ns: int | None
    done_reason: str


class OllamaClient:
    def __init__(self, config: ExperimentConfig, session: requests.Session | None = None):
        self.config = config
        self.session = session or requests.Session()

    def generate(self, prompt: str) -> LLMResponse:
        payload = {
            "model": self.config.model,
            "stream": False,
            "messages": [
                {"role": "system", "content": self.config.system_prompt},
                {"role": "user", "content": prompt},
            ],
            "options": self.config.options,
            "keep_alive": "5m",
        }
        started = time.perf_counter()
        response = self.session.post(
            self.config.url.rstrip("/") + "/api/chat",
            json=payload,
            timeout=self.config.timeout,
        )
        response.raise_for_status()
        latency = time.perf_counter() - started
        raw = response.json()
        if not isinstance(raw, dict) or not isinstance(raw.get("message"), dict):
            raise ModelResponseError("Ollama response does not contain a message")
        output = raw["message"].get("content")
        if not isinstance(output, str):
            raise ModelResponseError("Model output is missing")
        counts = parse_counts(raw)
        return LLMResponse(
            output=output,
            input_tokens=counts.input_tokens,
            output_tokens=counts.output_tokens,
            latency_s=latency,
            prompt_eval_duration_ns=raw.get("prompt_eval_duration"),
            eval_duration_ns=raw.get("eval_duration"),
            done_reason=str(raw.get("done_reason", "unknown")),
        )

    def healthcheck(self) -> dict:
        response = self.session.get(self.config.url.rstrip("/") + "/api/tags", timeout=10)
        response.raise_for_status()
        return response.json()
