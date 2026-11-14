from token_analysis.config import ROOT
from token_analysis.analysis.quality_analysis import load_quality_review, completed_reviews


def test_unfilled_reviews_not_treated_as_completed():
    rows = load_quality_review(ROOT / "data" / "quality_review.csv")
    assert len(rows) == 10
    assert completed_reviews(rows) == []
