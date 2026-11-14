from dataclasses import dataclass
from token_analysis.utils.exceptions import ModelResponseError

@dataclass(frozen=True)
class TokenCounts:
    input_tokens: int
    output_tokens: int

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens


def parse_counts(response: dict) -> TokenCounts:
    values = []
    for key in ("prompt_eval_count", "eval_count"):
        value = response.get(key)
        if type(value) is not int or value < 0:
            raise ModelResponseError(f"Missing or invalid Ollama token count: {key}")
        values.append(value)
    return TokenCounts(*values)
