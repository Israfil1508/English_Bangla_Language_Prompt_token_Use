from decimal import Decimal
import pytest
from token_analysis.metrics.cost_calculator import calculate_total_cost, calculate_input_cost


def test_notional_cost_exact():
    assert calculate_total_cost(1_000_000, 1_000_000) == Decimal("0.75")
    assert calculate_total_cost(100, 200) == Decimal("0.000135")


def test_negative_tokens():
    with pytest.raises(ValueError):
        calculate_input_cost(-1)
