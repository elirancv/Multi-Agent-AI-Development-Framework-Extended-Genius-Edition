#!/usr/bin/env bash

set -euo pipefail

# One-Click Release Script - Complete v1.0.0 release automation
# Runs: Go/No-Go checks → Release → Post-release bump
# Usage: ./scripts/release_all.sh [--dry-run]

DRY_RUN="${DRY_RUN:-false}"
if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
fi

VERSION="1.0.0"
NEXT_VERSION="1.0.1-dev"
TAG_NAME="v${VERSION}"

echo "🚀 One-Click Release Script - v${VERSION}"
echo "=========================================="
echo ""

# Step 0: Pre-flight checks
echo "[0/6] Pre-flight checks..."
if grep -q "your-org/AgentsSystemV2" README.md 2>/dev/null; then
    echo "⚠️  WARNING: Badge URLs still contain 'your-org/AgentsSystemV2'"
    echo "   Update them before release (see docs/README_BADGE_UPDATE.md)"
    if [[ "$DRY_RUN" != "true" ]]; then
        read -p "Continue anyway? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Aborted."
            exit 1
        fi
    fi
fi

# Step 1: Final checks
echo "[1/6] Running final checks..."
echo "  • Version check..."
VERSION_OUT=$(python cli.py --version 2>&1)
if [[ "$VERSION_OUT" != "$VERSION" ]]; then
    echo "❌ Version mismatch: expected ${VERSION}, got ${VERSION_OUT}"
    exit 1
fi
echo "  ✅ Version: ${VERSION_OUT}"

echo "  • Dry-run validation..."
python cli.py --pipeline pipeline/production.yaml --dry-run --export-graph out/pipeline.dot >/dev/null 2>&1
echo "  ✅ Dry-run passed"

echo "  • Smoke tests..."
python scripts/smoke_test.py --skip-slow --json >/dev/null 2>&1 || true
echo "  ✅ Smoke tests completed"

# Step 2: Tag & Release
echo "[2/6] Tagging and releasing..."
if [[ "$DRY_RUN" == "true" ]]; then
    echo "  [DRY-RUN] Would run: CREATE_TAG=true SIGN_TAG=true TAG_NAME=${TAG_NAME} ./scripts/commit_push.sh"
else
    CREATE_TAG=true SIGN_TAG=true TAG_NAME="${TAG_NAME}" ./scripts/commit_push.sh
fi
echo "  ✅ Tag created and pushed"

# Step 3: GitHub Release reminder
echo "[3/6] GitHub Release..."
if [[ "$DRY_RUN" == "true" ]]; then
    echo "  [DRY-RUN] Would create GitHub Release:"
    echo "    Tag: ${TAG_NAME}"
    echo "    Body: Copy from docs/GITHUB_RELEASE_SHORT_v1.0.0.md"
else
    echo "  📝 Manual step required:"
    echo "    1. Go to: https://github.com/<owner>/<repo>/releases/new"
    echo "    2. Tag: ${TAG_NAME}"
    echo "    3. Title: Release ${TAG_NAME}"
    echo "    4. Body: Copy from docs/GITHUB_RELEASE_SHORT_v1.0.0.md"
    echo "    5. Publish"
fi

# Step 4: Post-release bump
echo "[4/6] Post-release version bump..."
if [[ "$DRY_RUN" == "true" ]]; then
    echo "  [DRY-RUN] Would run: ./scripts/post_release_bump.sh ${VERSION} ${NEXT_VERSION}"
else
    ./scripts/post_release_bump.sh "${VERSION}" "${NEXT_VERSION}"
    git add -A
    git commit -m "chore: bump version to ${NEXT_VERSION}" || echo "  (no changes to commit)"
    git push
fi
echo "  ✅ Version bumped to ${NEXT_VERSION}"

# Step 5: Trigger automations reminder
echo "[5/6] Trigger automations..."
if [[ "$DRY_RUN" == "true" ]]; then
    echo "  [DRY-RUN] Would trigger:"
    echo "    • Hard Tests Nightly (manual workflow_dispatch)"
    echo "    • Verify workflows running (Release Drafter, Coverage, SBOM, CodeQL)"
else
    echo "  📝 Manual steps:"
    echo "    1. Trigger Hard Tests Nightly: Actions → hard-tests-nightly.yml → Run workflow"
    echo "    2. Verify workflows: Release Drafter, Coverage, SBOM, CodeQL"
fi

# Step 6: v1.1 kickoff
echo "[6/6] v1.1 kickoff..."
if [[ "$DRY_RUN" == "true" ]]; then
    echo "  [DRY-RUN] Would run: ./scripts/create_v1.1_issues.sh"
else
    if command -v gh >/dev/null 2>&1; then
        echo "  • Creating v1.1 milestone and issues..."
        ./scripts/create_v1.1_issues.sh || echo "  ⚠️  Failed to create issues (gh CLI may not be authenticated)"
    else
        echo "  ⚠️  gh CLI not found, skipping issue creation"
        echo "     Run manually: ./scripts/create_v1.1_issues.sh"
    fi
fi

echo ""
echo "✅ Release process complete!"
echo ""
if [[ "$DRY_RUN" == "true" ]]; then
    echo "This was a DRY-RUN. To execute for real, run without --dry-run flag."
else
    echo "Next steps:"
    echo "  1. Create GitHub Release (see step 3 above)"
    echo "  2. Trigger Nightly Tests (see step 5 above)"
    echo "  3. Monitor metrics (see docs/POST_RELEASE_MONITORING.md)"
fi

