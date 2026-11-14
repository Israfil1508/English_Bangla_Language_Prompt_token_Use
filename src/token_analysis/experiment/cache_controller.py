from token_analysis.config import ExperimentConfig


def caching_protocol() -> str:
    """Document limitations; this does not claim to disable Ollama caching."""
    return ("Each request uses a fresh system+user message list. The dataset run order is "
            "seeded and randomized by pair and language. Ollama/runtime cache state "
            "cannot be guaranteed cold; measure repeated counts and durations separately.")


def measure_reference(client, prompt: str = "Hello.", repeats: int = 2) -> list[dict]:
    return [{"input_tokens": r.input_tokens, "output_tokens": r.output_tokens,
             "latency_s": r.latency_s, "prompt_eval_duration_ns": r.prompt_eval_duration_ns}
            for r in (client.generate(prompt) for _ in range(repeats))]
