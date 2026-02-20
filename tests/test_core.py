import pytest

from calc.core import evaluate


def test_exact_arithmetic():
    assert str(evaluate("1/3 + 1/6")) == "1/2"


def test_derivative():
    assert str(evaluate("d(x^3 + 2*x, x)")) == "3*x**2 + 2"


def test_integral():
    assert str(evaluate("int(sin(x), x)")) == "-cos(x)"


def test_solve():
    assert str(evaluate("solve(x^2 - 4, x)")) == "[-2, 2]"


def test_numeric_eval():
    assert str(evaluate("N(pi, 10)")) == "3.141592654"


def test_blocks_import_injection():
    with pytest.raises(Exception):
        evaluate('__import__("os").system("echo bad")')


def test_blocks_dunder_access():
    with pytest.raises(ValueError, match="blocked token"):
        evaluate("x.__class__")


def test_blocks_long_expression():
    expr = "1+" * 2000 + "1"
    with pytest.raises(ValueError, match="expression too long"):
        evaluate(expr)
