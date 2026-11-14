import pytest
from token_analysis.metrics.token_counter import parse_counts
from token_analysis.utils.exceptions import ModelResponseError


def test_ollama_counts():
    result = parse_counts({"prompt_eval_count": 12, "eval_count": 7})
    assert (result.input_tokens, result.output_tokens, result.total_tokens) == (12, 7, 19)

@pytest.mark.parametrize("value", [None, -1, "3", True])
def test_reject_bad_count(value):
    with pytest.raises(ModelResponseError):
        parse_counts({"prompt_eval_count": value, "eval_count": 2})
