from collections import Counter
from token_analysis.dataset.dataset_loader import PromptPair
from token_analysis.utils.exceptions import DatasetError

EXPECTED_CATEGORIES = {
    "factual": 10,
    "instruction": 10,
    "explanation": 10,
    "arithmetic": 8,
    "summarization": 7,
    "long": 5,
}


def validate_pairs(pairs: list[PromptPair], strict: bool = True) -> None:
    if strict and len(pairs) != 50:
        raise DatasetError(f"Expected 50 pairs, received {len(pairs)}")
    ids = [p.id for p in pairs]
    if len(ids) != len(set(ids)):
        raise DatasetError("Duplicate IDs are not allowed")
    for pair in pairs:
        if not all([pair.id.strip(), pair.category.strip(), pair.english.strip(), pair.bangla.strip()]):
            raise DatasetError(f"Empty field in pair {pair.id}")
        if pair.category not in EXPECTED_CATEGORIES:
            raise DatasetError(f"Invalid category: {pair.category}")
        if not any("\u0980" <= char <= "\u09ff" for char in pair.bangla):
            raise DatasetError(f"Bangla script missing in pair {pair.id}")
    if strict and Counter(pair.category for pair in pairs) != EXPECTED_CATEGORIES:
        raise DatasetError("Category counts do not match the specified distribution")
