#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: scripts/release.sh <version>"
  echo "example: scripts/release.sh 0.1.8"
  exit 1
fi

VERSION="$1"
TAG="v${VERSION}"

if [[ ! "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "error: version must be semver-like (e.g. 0.1.8)"
  exit 1
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "error: working tree is not clean; commit or stash changes first"
  exit 1
fi

if git rev-parse -q --verify "refs/tags/${TAG}" >/dev/null; then
  echo "error: tag ${TAG} already exists"
  exit 1
fi

echo "[release] running local gates"
scripts/checks.sh

echo "[release] pushing main"
git push origin main

echo "[release] creating tag ${TAG}"
git tag -a "${TAG}" -m "Release ${TAG}"
git push origin "${TAG}"

echo "[release] queued:"
echo "  GitHub Actions: https://github.com/sacchen/phil/actions"
echo "  PyPI: https://pypi.org/project/philcalc/"
