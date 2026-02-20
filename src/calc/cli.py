from __future__ import annotations

import sys
from urllib.parse import quote_plus

from .core import evaluate

PROMPT = "calc> "
HELP_TEXT = (
    "calc - symbolic CLI calculator\n"
    "\n"
    "usage:\n"
    "  calc '<expression>'\n"
    "  calc\n"
    "\n"
    "repl commands:\n"
    "  :h, :help      show this help\n"
    "  :examples      show example expressions\n"
    "  :q, :quit, :x  quit\n"
    "\n"
    "quick examples:\n"
    "  d(x^3 + 2*x, x)\n"
    "  int(sin(x), x)\n"
    "  solve(x^2 - 4, x)\n"
    "  N(pi, 20)"
)
EXAMPLES_TEXT = (
    "examples:\n"
    "  1/3 + 1/6\n"
    "  d(x^3 + 2*x, x)\n"
    "  int(sin(x), x)\n"
    "  solve(x^2 - 4, x)\n"
    "  dsolve(Eq(f(t).diff(t), f(t)), f(t))\n"
    "  N(pi, 20)"
)


def _wolframalpha_url(expr: str) -> str:
    return f"https://www.wolframalpha.com/input?i={quote_plus(expr)}"


def _print_error(exc: Exception, expr: str | None = None) -> None:
    print(f"E: {exc}", file=sys.stderr)
    hint = _hint_for_error(str(exc))
    if hint:
        print(f"hint: {hint}", file=sys.stderr)
    if expr:
        print(f"hint: try WolframAlpha: {_wolframalpha_url(expr)}", file=sys.stderr)


def _hint_for_error(message: str) -> str | None:
    text = message.lower()
    if "unexpected eof" in text:
        return "check missing closing ')' or unmatched quote"
    if "name '" in text and "is not defined" in text:
        return "use one of: x y z t pi e f and documented functions"
    if "blocked token" in text:
        return "remove blocked patterns like '__', ';', or newlines"
    if "empty expression" in text:
        return "enter a math expression, or use :examples"
    return None


def _handle_repl_command(expr: str) -> bool:
    if expr in {":q", ":quit", ":x"}:
        raise EOFError
    if expr in {":h", ":help"}:
        print(HELP_TEXT)
        return True
    if expr == ":examples":
        print(EXAMPLES_TEXT)
        return True
    if expr.startswith(":"):
        print("E: unknown command", file=sys.stderr)
        print("hint: use :h to list commands", file=sys.stderr)
        return True
    return False


def run(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv

    if args:
        if len(args) == 1 and args[0] in {"-h", "--help"}:
            print(HELP_TEXT)
            return 0
        expr = " ".join(args)
        try:
            print(evaluate(expr))
            return 0
        except Exception as exc:
            _print_error(exc, expr)
            return 1

    print("calc REPL. :h help, :q quit, Ctrl-D exit.")
    while True:
        try:
            expr = input(PROMPT).strip()
            if not expr:
                continue
            if _handle_repl_command(expr):
                continue
            print(evaluate(expr))
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        except Exception as exc:
            _print_error(exc, expr)


if __name__ == "__main__":
    raise SystemExit(run())
