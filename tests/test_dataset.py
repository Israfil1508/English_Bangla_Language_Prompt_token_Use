import pytest
from token_analysis.config import ROOT
from token_analysis.dataset.dataset_loader import load_dataset
from token_analysis.dataset.dataset_validator import validate_pairs
from token_analysis.utils.exceptions import DatasetError


def test_50_valid_pairs():
    pairs = load_dataset(ROOT / "data" / "dataset.tsv")
    validate_pairs(pairs)
    assert len(pairs) == 50


def test_reject_duplicate_id():
    pairs = load_dataset(ROOT / "data" / "dataset.tsv")
    with pytest.raises(DatasetError, match="Duplicate"):
        validate_pairs(pairs + [pairs[0]], strict=False)
