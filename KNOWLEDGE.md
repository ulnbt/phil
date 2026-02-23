# KNOWLEDGE

Project-specific knowledge for contributors.

## Product Surface

- Distribution name: `philcalc`
- CLI command: `phil`
- Core module path: `src/calc/`

## Parsing and Evaluation Model

- Uses SymPy `parse_expr` with restricted globals.
- Default mode is relaxed parsing for calculator-style input.
- Strict mode (`--strict`) disables relaxed transforms.
- Optional no-simplify mode (`--no-simplify`) returns parsed form without `simplify()`.

## Supported Syntax Highlights

- Derivative:
  - `d(expr, var)`
  - `d(expr)` when variable can be inferred uniquely
  - Leibniz shorthand: `d(sin(x))/dx`, `df(t)/dt`
  - Function exponent shorthand: `sin^2(x)`, `cos^2(x)`
  - ODE shorthand equation: `dy/dx = y`, `y' = y`, `y'' + y = 0`
  - LaTeX ODE shorthand: `\frac{dy}{dx} = y`, `\frac{d^2y}{dx^2} + y = 0`
  - LaTeX wrappers/commands normalized: `$...$`, `\(...\)`, `\sin`, `\cos`, `\ln`, `\sqrt{...}`, `\frac{a}{b}`
- Integral:
  - `int(expr, var)`
  - `int(expr)` with unique variable inference
- Exact arithmetic helpers:
  - `gcd(a, b)`, `lcm(a, b)`
  - `isprime(n)`, `factorint(n)`
  - `num(expr)`, `den(expr)` via `as_numer_denom()`
- Matrix helpers:
  - `Matrix`, `eye`, `zeros`, `ones`
  - `det`, `inv`, `rank`, `eigvals`, `rref`, `nullspace`
  - `msolve(A, b)` for matrix equations `Ax=b`
  - `linsolve((Eq(...), ...), (x, y, ...))` for symbolic linear systems
- Session behavior (REPL):
  - assignment: `A = ...`
  - `ans` = last result
  - inline options are accepted (example: `--latex d(x^2, x)`)
  - progressive help aliases: `?`, `??`, `???`
  - guided tutorial commands: `:tutorial`/`:tour`, `:next`, `:repeat`, `:done`
  - ODE helper command: `:ode`
  - linear algebra helper command: `:linalg`/`:la`

## CLI Surface

- Canonical end-user flag docs are in `README.md` (usage/options sections).
- Contributor-facing expectation: diagnostics remain on `stderr`; result payloads remain on `stdout`.
- `--format json` is the machine-readable interop mode (`input`, `parsed`, `result`).

## Error UX

- Errors start with `E:`
- Follow-up guidance via `hint:`
- Syntax-specific hints exist for common derivative and matrix mistakes.
- Ambiguous trig shorthand like `sin x^2` is rejected with an explicit disambiguation hint.
- Reserved-name assignment errors show targeted hints (e.g. `f` → ODE function-notation guidance).
- WolframAlpha hint is suppressed for reserved-name assignment errors.
- WolframAlpha hint is also suppressed for deterministic local guardrail failures (huge power/factorial limits).

## Reliability Guardrails

- Guardrail path parses with `evaluate=False` before eager evaluation.
- Huge integer powers are reduced symbolically first; non-cancellable growth fails fast.
- Exponent-tower growth cases are bounded by integer exponent limits.
- Huge factorial inputs fail fast for both literal (`100001!`, `(100001)!`) and computed-integer forms (`factorial(10^10)`).

## Testing Expectations

- Unit + integration + regression tests.
- Property tests via `hypothesis` for core invariants.
- Hypothesis profiles:
  - `default`: lighter local baseline (faster day-to-day runs)
  - `ci`: CI baseline (`HYPOTHESIS_PROFILE=ci`)
  - `fuzz`: long fuzzing runs (`HYPOTHESIS_PROFILE=fuzz`)
- Local speed defaults:
  - `uv run --group dev pytest -m "not integration"` for fast iteration
- CI checks multiple Python versions, dedicated fuzz runs, dependency audit, and install smoke tests.
