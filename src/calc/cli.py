from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from json import JSONDecodeError, loads
from importlib.metadata import PackageNotFoundError, version as package_version
from urllib.error import URLError
from urllib.parse import quote_plus
from urllib.request import urlopen

from sympy import latex as to_latex

from .core import evaluate

PACKAGE_NAME = "philcalc"
CLI_NAME = "phil"
UPDATE_CMD = "uv tool upgrade philcalc"


def _calc_version() -> str:
    try:
        return package_version(PACKAGE_NAME)
    except PackageNotFoundError:
        return "dev"


VERSION = _calc_version()
PROMPT = f"{CLI_NAME}> "
HELP_TEXT = (
    f"{CLI_NAME} v{VERSION} - symbolic CLI calculator\n"
    "\n"
    "usage:\n"
    f"  {CLI_NAME} [--format MODE] [--latex|--latex-inline|--latex-block] [--strict] [--no-simplify] [--wa] [--copy-wa] '<expression>'\n"
    f"  {CLI_NAME}\n"
    f"  {CLI_NAME} :examples\n"
    "\n"
    "options:\n"
    "  --format MODE   output mode: plain, pretty, latex, latex-inline, latex-block\n"
    "  --latex         print raw LaTeX (no delimiters)\n"
    "  --latex-inline  print LaTeX wrapped as $...$\n"
    "  --latex-block   print LaTeX wrapped as $$...$$\n"
    "  --strict        disable relaxed input parsing\n"
    "  --no-simplify   skip simplify() on parsed expressions\n"
    "  --wa            always print WolframAlpha equivalent link\n"
    "  --copy-wa       copy WolframAlpha link to clipboard when shown\n"
    "\n"
    "upgrade:\n"
    f"  {UPDATE_CMD}\n"
    "\n"
    "repl commands:\n"
    "  :h, :help      show this help\n"
    "  :examples      show example expressions\n"
    "  :v, :version   show version\n"
    "  :update, :check  check current vs latest version\n"
    "  :q, :quit, :x  quit\n"
    "\n"
    "quick examples:\n"
    "  (1 - 25e^5)e^{-5t} + (25e^5 - 1)t e^{-5t} + t e^{-5t} ln(t)\n"
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
    "  (854/2197)e^{8t}+(1343/2197)e^{-5t}+((9/26)t^2 -(9/169)t)e^{8t}\n"
    "  dsolve(Eq(f(t).diff(t), f(t)), f(t))\n"
    "  N(pi, 20)"
)


def _wolframalpha_url(expr: str) -> str:
    return f"https://www.wolframalpha.com/input?i={quote_plus(expr)}"


def _is_complex_expression(expr: str) -> bool:
    if len(expr) >= 40:
        return True
    markers = ("d(", "int(", "solve(", "dsolve(", "Eq(", "ln(", "log(", "^", "{", "}", "e^{")
    return any(marker in expr for marker in markers)


def _format_clickable_link(label: str, url: str) -> str:
    if not sys.stderr.isatty() or os.getenv("TERM") == "dumb":
        return url
    esc = "\033"
    return f"{esc}]8;;{url}{esc}\\{label}{esc}]8;;{esc}\\"


def _copy_to_clipboard(text: str) -> bool:
    commands = (
        ["pbcopy"],
        ["wl-copy"],
        ["xclip", "-selection", "clipboard"],
        ["xsel", "--clipboard", "--input"],
        ["clip"],
    )
    for cmd in commands:
        if shutil.which(cmd[0]) is None:
            continue
        try:
            subprocess.run(cmd, input=text, text=True, check=True, capture_output=True)
            return True
        except Exception:
            continue
    return False


def _print_wolfram_hint(expr: str, copy_link: bool = False) -> None:
    url = _wolframalpha_url(expr)
    # Always print raw URL for maximum terminal compatibility (e.g., iTerm2 auto-linking).
    print(f"hint: try WolframAlpha: {url}", file=sys.stderr)
    if copy_link:
        if _copy_to_clipboard(url):
            print("hint: WolframAlpha link copied to clipboard", file=sys.stderr)
        else:
            print("hint: clipboard copy unavailable on this system", file=sys.stderr)


def _print_error(exc: Exception, expr: str | None = None) -> None:
    print(f"E: {exc}", file=sys.stderr)
    hint = _hint_for_error(str(exc), expr=expr)
    if hint:
        print(f"hint: {hint}", file=sys.stderr)
    if expr:
        _print_wolfram_hint(expr)


def _hint_for_error(message: str, expr: str | None = None) -> str | None:
    text = message.lower()
    if "unexpected eof" in text:
        if expr and ("/d" in expr or expr.strip().startswith("d(")):
            return "derivative syntax: d(expr, var) or d(sin(x))/dx or df(t)/dt"
        return "check missing closing ')' or unmatched quote"
    if "invalid syntax" in text:
        if expr:
            compact = re.sub(r"\s+", "", expr)
            if "d(" in compact or re.search(r"\bd[A-Za-z0-9_]+/d[A-Za-z0-9_]+\b", compact):
                return "derivative syntax: d(expr, var) or d(sin(x))/dx or df(t)/dt"
            if "matrix(" in compact.lower():
                return "matrix syntax: Matrix([[1,2],[3,4]])"
        return "check commas and brackets; try :examples for working patterns"
    if "name '" in text and "is not defined" in text:
        if expr and ("/d" in expr or expr.strip().startswith("d")):
            return "derivative syntax: d(expr, var) or d(sin(x))/dx or df(t)/dt"
        return "use one of: x y z t pi e f and documented functions"
    if "data type not understood" in text:
        if expr and "matrix(" in expr.lower():
            return "matrix syntax: Matrix([[1,2],[3,4]])"
    if "blocked token" in text:
        return "remove blocked patterns like '__', ';', or newlines"
    if "empty expression" in text:
        return "enter a math expression, or use :examples"
    return None


def _format_result(value, format_mode: str) -> str:
    if format_mode == "plain":
        return str(value)
    if format_mode == "pretty":
        from sympy import pretty as to_pretty

        return to_pretty(value)
    rendered = to_latex(value)
    if format_mode == "latex-inline":
        return f"${rendered}$"
    if format_mode == "latex-block":
        return f"$$\n{rendered}\n$$"
    return rendered


def _latest_pypi_version() -> str | None:
    url = f"https://pypi.org/pypi/{PACKAGE_NAME}/json"
    try:
        with urlopen(url, timeout=2.0) as response:
            payload = loads(response.read().decode("utf-8"))
        return payload.get("info", {}).get("version")
    except (OSError, URLError, TimeoutError, ValueError, JSONDecodeError):
        return None


def _print_update_status() -> None:
    if VERSION == "dev":
        print("current version: dev (local checkout)")
        print("latest version: unknown from local checkout")
        print("install latest local changes with: uv tool install --force --reinstall --refresh .")
        return

    latest = _latest_pypi_version()
    print(f"current version: {VERSION}")
    if latest is None:
        print("latest version: unavailable (offline or PyPI unreachable)")
    elif latest == VERSION:
        print(f"latest version: {latest} (up to date)")
    else:
        print(f"latest version: {latest} (update available)")
    print(f"update with: {UPDATE_CMD}")


def _parse_options(args: list[str]) -> tuple[str, bool, bool, bool, bool, list[str]]:
    format_mode = "plain"
    relaxed = True
    simplify_output = True
    always_wa = False
    copy_wa = False
    idx = 0
    while idx < len(args) and args[idx].startswith("-"):
        arg = args[idx]
        if arg in {"-h", "--help"}:
            print(HELP_TEXT)
            raise SystemExit(0)
        if arg == "--format":
            if idx + 1 >= len(args):
                raise ValueError("missing value for --format")
            mode = args[idx + 1]
            if mode not in {"plain", "pretty", "latex", "latex-inline", "latex-block"}:
                raise ValueError(f"unknown format mode: {mode}")
            format_mode = mode
            idx += 2
            continue
        if arg.startswith("--format="):
            mode = arg.split("=", 1)[1]
            if mode not in {"plain", "pretty", "latex", "latex-inline", "latex-block"}:
                raise ValueError(f"unknown format mode: {mode}")
            format_mode = mode
            idx += 1
            continue
        if arg == "--latex":
            format_mode = "latex"
            idx += 1
            continue
        if arg == "--latex-inline":
            format_mode = "latex-inline"
            idx += 1
            continue
        if arg == "--latex-block":
            format_mode = "latex-block"
            idx += 1
            continue
        if arg == "--strict":
            relaxed = False
            idx += 1
            continue
        if arg == "--no-simplify":
            simplify_output = False
            idx += 1
            continue
        if arg == "--wa":
            always_wa = True
            idx += 1
            continue
        if arg == "--copy-wa":
            copy_wa = True
            idx += 1
            continue
        if arg == "--":
            idx += 1
            break
        if arg.startswith("--"):
            raise ValueError(f"unknown option: {arg}")
        break
    return format_mode, relaxed, simplify_output, always_wa, copy_wa, args[idx:]


def _handle_repl_command(expr: str) -> bool:
    if expr in {":q", ":quit", ":x"}:
        raise EOFError
    if expr in {":h", ":help"}:
        print(HELP_TEXT)
        return True
    if expr == ":examples":
        print(EXAMPLES_TEXT)
        return True
    if expr in {":v", ":version"}:
        print(f"{CLI_NAME} v{VERSION}")
        return True
    if expr in {":update", ":check"}:
        _print_update_status()
        return True
    if expr.startswith(":"):
        print("E: unknown command", file=sys.stderr)
        print("hint: use :h to list commands", file=sys.stderr)
        return True
    return False


def run(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv

    try:
        format_mode, relaxed, simplify_output, always_wa, copy_wa, remaining = _parse_options(args)
    except SystemExit:
        return 0
    except Exception as exc:
        _print_error(exc)
        return 1

    if remaining:
        expr = " ".join(remaining)
        if expr == ":examples":
            print(EXAMPLES_TEXT)
            return 0
        if expr in {":v", ":version"}:
            print(f"{CLI_NAME} v{VERSION}")
            return 0
        if expr in {":update", ":check"}:
            _print_update_status()
            return 0
        try:
            print(
                _format_result(
                    evaluate(expr, relaxed=relaxed, simplify_output=simplify_output),
                    format_mode,
                )
            )
            if always_wa or _is_complex_expression(expr):
                _print_wolfram_hint(expr, copy_link=copy_wa)
            return 0
        except Exception as exc:
            _print_error(exc, expr)
            return 1

    print(f"{CLI_NAME} v{VERSION} REPL. :h help, :q quit, Ctrl-D exit.")
    print(f"update: {UPDATE_CMD}")
    session_locals: dict = {}
    while True:
        try:
            expr = input(PROMPT).strip()
            if not expr:
                continue
            if _handle_repl_command(expr):
                continue
            print(
                _format_result(
                    evaluate(
                        expr,
                        relaxed=relaxed,
                        session_locals=session_locals,
                        simplify_output=simplify_output,
                    ),
                    format_mode,
                )
            )
            if always_wa or _is_complex_expression(expr):
                _print_wolfram_hint(expr, copy_link=copy_wa)
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        except Exception as exc:
            _print_error(exc, expr)


if __name__ == "__main__":
    raise SystemExit(run())
