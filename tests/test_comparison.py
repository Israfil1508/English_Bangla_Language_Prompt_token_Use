from token_analysis.metrics.comparison import safe_ratio


def test_ratios():
    assert safe_ratio(25, 10) == 2.5
    assert safe_ratio(0, 0) is None
