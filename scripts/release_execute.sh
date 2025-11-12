#!/usr/bin/env bash

set -euo pipefail

# Release Execution Pack - Complete v1.0.0 release workflow
# Usage: ./scripts/release_execute.sh

echo "🚀 Starting v1.0.0 Release Process..."
echo ""

# Sanity checks
echo "[1/4] Running sanity checks..."
python cli.py --version
python cli.py --pipeline pipeline/production.yaml --dry-run --export-graph out/pipeline.dot
python scripts/smoke_test.py --skip-slow --json
coverage run -m pytest && coverage xml -o coverage.xml && coverage report

echo ""
echo "[2/4] Tagging and releasing..."
CREATE_TAG=true SIGN_TAG=true TAG_NAME=v1.0.0 ./scripts/commit_push.sh

echo ""
echo "[3/4] Post-release version bump..."
./scripts/post_release_bump.sh 1.0.0 1.0.1-dev

echo ""
echo "[4/4] Committing version bump..."
git add -A
git commit -m "chore: bump version to 1.0.1-dev"
git push

echo ""
echo "✅ Release process complete!"
echo ""
echo "Next steps:"
echo "  1. Create GitHub Release: https://github.com/<owner>/<repo>/releases/new"
echo "  2. Copy body from: docs/GITHUB_RELEASE_SHORT_v1.0.0.md"
echo "  3. Create v1.1 milestone and issues (see scripts/create_v1.1_issues.sh)"

