#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "usage: scripts/release_notes.sh <version> [--body]"
  echo "example: scripts/release_notes.sh 0.3.0 --body"
  exit 1
fi

VERSION="$1"
MODE="${2:-}"

if [[ ! "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "error: version must be semver-like (e.g. 0.3.0)"
  exit 1
fi

DRAFT_FILE="release-notes/v${VERSION}-draft.md"

if [[ ! -f "$DRAFT_FILE" ]]; then
  echo "error: draft not found: ${DRAFT_FILE}"
  exit 1
fi

if [[ -z "$MODE" ]]; then
  cat "$DRAFT_FILE"
  exit 0
fi

if [[ "$MODE" != "--body" ]]; then
  echo "error: unknown option: ${MODE}"
  echo "usage: scripts/release_notes.sh <version> [--body]"
  exit 1
fi

awk '
  /^## GitHub Release Body \(Final Copy\)/ { in_section = 1; next }
  in_section && /^````md$/ { in_fence = 1; next }
  in_fence && /^````$/ { exit 0 }
  in_fence { print }
' "$DRAFT_FILE"
