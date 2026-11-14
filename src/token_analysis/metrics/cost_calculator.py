from decimal import Decimal

MILLION = Decimal("1000000")
INPUT_RATE = Decimal("0.15")
OUTPUT_RATE = Decimal("0.60")


def calculate_input_cost(tokens: int) -> Decimal:
    if type(tokens) is not int or tokens < 0:
        raise ValueError("Input tokens must be a non-negative integer")
    return Decimal(tokens) * INPUT_RATE / MILLION


def calculate_output_cost(tokens: int) -> Decimal:
    if type(tokens) is not int or tokens < 0:
        raise ValueError("Output tokens must be a non-negative integer")
    return Decimal(tokens) * OUTPUT_RATE / MILLION


def calculate_total_cost(input_tokens: int, output_tokens: int) -> Decimal:
    return calculate_input_cost(input_tokens) + calculate_output_cost(output_tokens)
