# Contributor Guide

This project is intentionally small. Changes should make `calc` clearer, safer, or more accurate without expanding feature scope.

## Principles

- Keep the CLI fast to understand.
- Prefer explicit math operations over magic behavior.
- Treat parser security as a first-class requirement.
- Add tests for every behavior change.

## Local Development

```bash
uv run --group dev pytest
uv run calc '2+2'
uv run calc
```

## How to Add a New Operation (Educational Workflow)

1. Add the SymPy function import in `src/calc/core.py`.
2. Add the user-facing name in `LOCALS_DICT` in `src/calc/core.py`.
3. Add at least one evaluator test in `tests/test_core.py`.
4. Add one README example if it is user-facing.
5. Run the test suite.

Example pattern:

- Internal function: `sympy.sinh`
- User API entry: `"sinh": sinh`
- Test: `assert str(evaluate("sinh(0)")) == "0"`

## Safety Rules

- Do not loosen `GLOBAL_DICT` restrictions in `src/calc/core.py`.
- Do not permit dunder tokens (`__`) or command separators in expressions.
- Keep input-size limits unless there is a measured need to adjust them.

## UX Rules

- Preserve terminal-first, low-noise output.
- Keep errors short (`E:` prefix) and actionable (`hint:` line when helpful).
- Keep REPL commands minimal (`:h`, `:examples`, `:q`).

## Scope Guardrails

Avoid adding:

- Plugin systems
- Persistent state
- Auto-completion frameworks
- Large config surface areas

If a feature adds complexity, include a clear reason and benchmark/impact in the PR message.
