from __future__ import annotations

import re

from sympy import (
    Abs,
    E,
    Eq,
    Float,
    Function,
    Integer,
    N,
    Rational,
    Symbol,
    cos,
    diff,
    dsolve,
    exp,
    factorial,
    integrate,
    log,
    pi,
    simplify,
    sin,
    solve,
    sqrt,
    symbols,
    tan,
)
from sympy.parsing.sympy_parser import auto_number, convert_xor, factorial_notation, parse_expr

x, y, z, t = symbols("x y z t")
f = Function("f")

LOCALS_DICT = {
    "x": x,
    "y": y,
    "z": z,
    "t": t,
    "pi": pi,
    "e": E,
    "f": f,
    "d": lambda expr, var: diff(expr, var),
    "int": lambda expr, var: integrate(expr, var),
    "solve": solve,
    "dsolve": dsolve,
    "Eq": Eq,
    "N": N,
    "sin": sin,
    "cos": cos,
    "tan": tan,
    "exp": exp,
    "log": log,
    "sqrt": sqrt,
    "abs": Abs,
}

# parse_expr internally uses eval. Keep globals minimal and disable builtins.
GLOBAL_DICT = {
    "__builtins__": {},
    "Integer": Integer,
    "Float": Float,
    "Rational": Rational,
    "Symbol": Symbol,
    "factorial": factorial,
}

TRANSFORMS = (auto_number, factorial_notation, convert_xor)
MAX_EXPRESSION_CHARS = 2000
BLOCKED_PATTERN = re.compile(r"(__|;|\n|\r)")


def _validate_expression(expression: str) -> None:
    if not expression.strip():
        raise ValueError("empty expression")
    if len(expression) > MAX_EXPRESSION_CHARS:
        raise ValueError(f"expression too long (max {MAX_EXPRESSION_CHARS} chars)")
    if BLOCKED_PATTERN.search(expression):
        raise ValueError("blocked token in expression")


def evaluate(expression: str):
    _validate_expression(expression)
    parsed = parse_expr(
        expression,
        local_dict=LOCALS_DICT,
        global_dict=GLOBAL_DICT,
        transformations=TRANSFORMS,
        evaluate=True,
    )
    if isinstance(parsed, (list, tuple, dict)):
        return parsed
    return simplify(parsed)
