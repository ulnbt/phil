#!/usr/bin/env bash
set -euo pipefail

echo "[checks] running test suite"
uv run --group dev pytest

echo "[checks] running coverage gate"
uv run --group dev pytest --cov=calc --cov-report=term-missing --cov-fail-under=90

echo "[checks] done"
