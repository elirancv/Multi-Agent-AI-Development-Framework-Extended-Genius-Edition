#!/usr/bin/env bash

set -euo pipefail

# -------- settings --------
BRANCH_DEFAULT="main"                # Change if needed
CREATE_TAG="${CREATE_TAG:-false}"    # export CREATE_TAG=true to create tag
TAG_NAME="${TAG_NAME:-v1.0.0}"       # override if needed
SIGN_TAG="${SIGN_TAG:-false}"        # export SIGN_TAG=true for GPG signing
DRY_RUN="${DRY_RUN:-false}"          # export DRY_RUN=true for dry-run without push
# --------------------------

echo "[1/7] Detecting branch & remote..."
BRANCH=$(git rev-parse --abbrev-ref HEAD || echo "$BRANCH_DEFAULT")
REMOTE=$(git remote 2>/dev/null | head -n1 || echo origin)
echo "   • branch: $BRANCH"
echo "   • remote: $REMOTE"

echo "[2/7] Housekeeping: formatting & linting..."
if command -v pre-commit >/dev/null 2>&1; then
  pre-commit install >/dev/null 2>&1 || true
  pre-commit run --all-files
else
  echo "   (pre-commit not found, skipping)"
fi

if command -v ruff >/dev/null 2>&1; then
  ruff check --fix .
fi

if command -v mypy >/dev/null 2>&1; then
  mypy .
else
  echo "   (mypy not found, skipping type-check)"
fi

echo "[3/7] Tests..."
pytest -q
python scripts/smoke_test.py --skip-slow --json >/dev/null || true

echo "[4/7] Build docs (optional)..."
if command -v pdoc >/dev/null 2>&1; then
  pdoc -o docs/api src || echo "   (pdoc failed/absent, continuing)"
else
  echo "   (pdoc not found, skipping api docs)"
fi

echo "[5/7] Export graph (optional)..."
python cli.py --pipeline pipeline/production.yaml --dry-run --export-graph out/pipeline.dot || true

echo "[6/7] Git add & commit..."
git add -A

# Build a clean Conventional Commit message
VERSION_LINE=$(python -c "import sys; sys.path.insert(0, '.'); from src import __version__; print(__version__)" 2>/dev/null || echo "unknown")
COMMIT_MSG="chore(repo): tidy project & release bundle

- run pre-commit, ruff fix, type-checks
- run tests & smoke
- update docs/api (if available) & export graph
- prepare release assets

Version: ${VERSION_LINE}
"

if git diff --cached --quiet; then
  echo "   No staged changes. Skipping commit."
else
  git commit -m "$COMMIT_MSG"
fi

echo "[7/7] Push..."
if [ "$DRY_RUN" = "true" ]; then
  echo "   DRY_RUN=true -> skipping push"
else
  git push "$REMOTE" "$BRANCH"
fi

if [ "$CREATE_TAG" = "true" ]; then
  echo "   Creating tag: $TAG_NAME"
  if [ "$SIGN_TAG" = "true" ]; then
    git tag -s "$TAG_NAME" -m "Release $TAG_NAME"
  else
    git tag "$TAG_NAME" -m "Release $TAG_NAME"
  fi
  [ "$DRY_RUN" = "true" ] || git push "$REMOTE" "$TAG_NAME"
fi

echo "✅ Done."
