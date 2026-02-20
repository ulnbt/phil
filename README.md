# calc

A minimal command-line calculator for exact arithmetic, symbolic differentiation, integration, algebraic equation solving, and ordinary differential equations.

Powered by [SymPy](https://www.sympy.org/).

## Install

Requires [uv](https://docs.astral.sh/uv/).

Install from the project directory:

```bash
uv tool install .
```

Run without installing:

```bash
uv run calc '2+2'
```

## 60-Second Start

```bash
uv tool install .
calc --help
calc '1/3 + 1/6'
calc
```

Then in REPL, try:

1. `d(x^3 + 2*x, x)`
2. `int(sin(x), x)`
3. `solve(x^2 - 4, x)`

## Usage

### One-shot

```bash
calc '<expression>'
```

### Interactive

```bash
calc
calc> <expression>
```

REPL commands:

- `:h` / `:help` show help
- `:examples` show sample expressions
- `:q` / `:quit` / `:x` exit

The REPL starts with a short hint line and prints targeted `hint:` messages on common errors.
Unknown `:` commands return a short correction hint.
Evaluation errors also include: `hint: try WolframAlpha: <url>`.

### Help

```bash
calc --help
```

## Examples

```bash
$ calc '1/3 + 1/6'
1/2

$ calc 'd(x^3 + 2*x, x)'
3*x**2 + 2

$ calc 'int(sin(x), x)'
-cos(x)

$ calc 'solve(x^2 - 4, x)'
[-2, 2]

$ calc 'N(pi, 30)'
3.14159265358979323846264338328
```

## Test

```bash
uv run --group dev pytest
```

## GitHub

- CI: `.github/workflows/ci.yml` runs tests on pushes and PRs.
- License: MIT (`LICENSE`).
- Ignore rules: Python/venv/cache (`.gitignore`).
- Contribution guide: `CONTRIBUTOR.md`.

## Learn by Doing

Try this sequence in REPL mode:

1. `1/3 + 1/6`
2. `d(x^3 + 2*x, x)`
3. `int(sin(x), x)`
4. `solve(x^2 - 4, x)`
5. `N(pi, 20)`

If you get stuck, run `:examples` or `:h`.

## Reference

### Operations

| Operation | Syntax |
|-----------|--------|
| Derivative | `d(expr, var)` |
| Integral | `int(expr, var)` |
| Solve equation | `solve(expr, var)` |
| Solve ODE | `dsolve(Eq(...), func)` |
| Equation | `Eq(lhs, rhs)` |
| Numeric eval | `N(expr, digits)` |

### Symbols

`x`, `y`, `z`, `t`, `pi`, `e`, `f`

### Functions

`sin`, `cos`, `tan`, `exp`, `log`, `sqrt`, `abs`

### Syntax notes

- `^` is exponentiation (`x^2`)
- `!` is factorial (`5!`)
- `*` is required for multiplication (`2*x`, not `2x`)
- Undefined symbols raise an error

## Safety limits

- Expressions longer than 2000 chars are rejected.
- Inputs containing blocked tokens like `__`, `;`, or newlines are rejected.

See [DESIGN.md](DESIGN.md) for implementation details.
