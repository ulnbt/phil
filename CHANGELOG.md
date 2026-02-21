# Changelog

## 0.1.11 - 2026-02-21

- Add matrix workflow helpers: `msolve(A, b)`, `rref(...)`, `nullspace(...)`, and `linsolve(...)`.
- Enable function-exponent parsing with SymPy transform support (for example `sin^2(x)`).
- Add `:linalg` / `:la` command with linear algebra quick-reference templates.
- Expand examples/tutorial/docs to highlight linear-system and exact symbolic workflows.

## 0.1.10 - 2026-02-21

- Add progressive help aliases (`?`, `??`, `???`) in one-shot mode and REPL for feature discovery.
- Expand help/tutorial/example text with an exact huge-integer arithmetic demo (`10^100000 + 1 - 10^100000`).
- Update contributor-facing docs to reflect the new discoverability flow.

## 0.1.9 - 2026-02-20

- Add human-friendly `ode ...` alias input for solving ODEs (including optional initial conditions like `y(0)=1`).
- Improve `:ode` help text with a beginner-first readable format.
- Render `ode ...` plain-mode solutions as `y(x) = ...` instead of raw `Eq(...)`.

## 0.1.8 - 2026-02-20

- Add `scripts/checks.sh` to run the standard test and coverage gates.
- Add `scripts/release.sh <version>` to automate local checks plus tag-based release push steps.
- Document scripted development/release workflow in contributor and README docs.

## 0.1.7 - 2026-02-20

- Refactor CLI internals to use a dedicated diagnostics module and typed option parsing.
- Keep CLI behavior stable while improving maintainability and test clarity.
- Consolidate contributor docs to keep `README.md` as the canonical CLI flag reference.

## 0.1.6 - 2026-02-20

- Add interop output mode: `--format json`.
- Improve reserved-name assignment hints (including explicit `f` function-notation guidance).
- Suppress WolframAlpha hint for reserved-name assignment errors.

## 0.1.5 - 2026-02-20

- Relaxed parsing now accepts shorthand trig input like `sinx`/`cosx`/`tanx` as `sin(x)`/`cos(x)`/`tan(x)`.
- CLI and REPL print an explicit `hint:` notice when shorthand is auto-interpreted.
- Add `--explain-parse` to show normalized input as a `hint:` on `stderr`.

## 0.1.4 - 2026-02-20

- Add in-app guided tour commands (`:tutorial`, `:tour`, `:next`, `:repeat`, `:done`).
- Add `:ode` quick reference with `Eq(...)`/`dsolve(...)` templates.
- Improve syntax hints for malformed `Eq(...)`, missing `Eq(...)` in `dsolve(...)`, and LaTeX fraction syntax errors.
- Link and expand new-user onboarding with `TUTORIAL.md`.

## 0.1.3 - 2026-02-20

- Improve ODE input ergonomics for homework-style notation.
- Accept REPL inline options and `phil ...`-prefixed input lines.
- Normalize ODE shorthand forms such as `dy/dx = y`, `y' = y`, and `y'' + y = 0`.
- Normalize common LaTeX-style inputs including `\frac{dy}{dx}`, `$...$`, and `\sin/\cos/\ln/\sqrt`.
- Add targeted `dsolve` function-notation hints for `y(x)` usage.

## 0.1.0 - 2026-02-20

- Initial public release.
- Symbolic CLI calculator with exact arithmetic and core SymPy operations.
- Hardened parser configuration and input guardrails.
- Minimal terminal UX (`:h`, `:examples`, `:q`, `:x`) with actionable hints.
- Optional WolframAlpha fallback hint on evaluation errors.
- uv package layout, tests, and GitHub Actions CI.
