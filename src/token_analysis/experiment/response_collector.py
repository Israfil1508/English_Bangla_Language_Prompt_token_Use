from token_analysis.metrics.token_counter import parse_counts


def collect_response_metadata(raw: dict) -> dict:
    counts = parse_counts(raw)
    return {"input_tokens": counts.input_tokens, "output_tokens": counts.output_tokens,
            "prompt_eval_duration_ns": raw.get("prompt_eval_duration"),
            "eval_duration_ns": raw.get("eval_duration")}
