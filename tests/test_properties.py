import pytest
from hypothesis import given
from hypothesis import strategies as st

from calc.core import evaluate


@pytest.mark.unit
@given(st.integers(min_value=-10_000, max_value=10_000), st.integers(min_value=-10_000, max_value=10_000))
def test_property_integer_addition_matches_python(a: int, b: int):
    expr = f"{a}+{b}"
    assert str(evaluate(expr)) == str(a + b)


@pytest.mark.unit
@given(st.integers(min_value=-50, max_value=50))
def test_property_derivative_inference_matches_explicit(coef: int):
    inferred = str(evaluate(f"d({coef}*x^2 + x)"))
    explicit = str(evaluate(f"d({coef}*x^2 + x, x)"))
    assert inferred == explicit
