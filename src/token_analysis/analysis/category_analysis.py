from token_analysis.analysis.statistics import summarize


def rank_categories(summary: dict) -> list[tuple[str, float]]:
    return sorted(((name, data["input_token_ratio"]) for name, data in summary["categories"].items()
                   if data["input_token_ratio"] is not None), key=lambda item: item[1], reverse=True)
