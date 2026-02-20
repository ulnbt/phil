import subprocess
import sys


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "calc", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli_success_exit_code():
    proc = run_cli("2+2")
    assert proc.returncode == 0
    assert proc.stdout.strip() == "4"


def test_cli_invalid_expression_exit_code():
    proc = run_cli("bad(")
    assert proc.returncode == 1
    assert "E:" in proc.stderr
    assert "hint:" in proc.stderr
    assert "hint: try WolframAlpha:" in proc.stderr
    assert "wolframalpha.com/input?i=bad%28" in proc.stderr


def test_cli_help_flag():
    proc = run_cli("--help")
    assert proc.returncode == 0
    assert "usage:" in proc.stdout
    assert ":examples" in proc.stdout


def test_repl_help_and_quit():
    proc = subprocess.run(
        [sys.executable, "-m", "calc"],
        input=":h\n:q\n",
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert ":h help" in proc.stdout
    assert "repl commands:" in proc.stdout


def test_repl_unknown_command_hint():
    proc = subprocess.run(
        [sys.executable, "-m", "calc"],
        input=":wat\n:q\n",
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "unknown command" in proc.stderr
    assert "use :h" in proc.stderr


def test_repl_error_shows_wolframalpha_hint():
    proc = subprocess.run(
        [sys.executable, "-m", "calc"],
        input="bad(\n:q\n",
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0
    assert "hint: try WolframAlpha:" in proc.stderr
