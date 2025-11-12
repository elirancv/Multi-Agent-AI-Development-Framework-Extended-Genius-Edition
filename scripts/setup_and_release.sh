#!/usr/bin/env bash

set -euo pipefail

# One-Liner: Setup Repo → Re-Validate → Release
# Usage: ./scripts/setup_and_release.sh [--dry-run]

OWNER="elirancv"
REPO="Multi-Agent-AI-Development-Framework-Extended-Genius-Edition"
DRY_RUN="${1:-}"

echo "🚀 Setup & Release - $OWNER/$REPO"
echo "=================================="
echo ""

# Step 1: Git init & remote
echo "[1/5] Setting up Git repository..."
git init -b main 2>/dev/null || true
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$OWNER/$REPO.git" 2>/dev/null || true
echo "  ✅ Remote configured: $OWNER/$REPO"

# Step 2: Create .env
echo "[2/5] Creating .env file..."
printf "OWNER=$OWNER\nREPO=$REPO\n" > .env
echo "  ✅ .env created"

# Step 3: Re-validate (installs tools, patches badges, runs checks)
echo "[3/5] Running re-validation..."
chmod +x scripts/revalidate.sh 2>/dev/null || true
./scripts/revalidate.sh || {
    echo "  ⚠️  Re-validation had warnings (check out/validation/FINAL_VALIDATION.md)"
}

# Step 4: Commit changes (badges, .env, etc.)
echo "[4/5] Committing changes..."
git add -A
if git diff --cached --quiet; then
    echo "  (no changes to commit)"
else
    git commit -m "chore: repo wiring + badges patch for $OWNER/$REPO" || true
    echo "  ✅ Changes committed"
fi

# Step 5: Release (dry-run or real)
echo "[5/5] Release process..."
if [ "$DRY_RUN" == "--dry-run" ]; then
    echo "  [DRY-RUN] Would run release..."
    ./scripts/release_all.sh --dry-run || true
else
    echo "  ⚠️  Ready to release. Run manually:"
    echo "     ./scripts/release_all.sh"
    echo ""
    echo "  Or push first:"
    echo "     git push -u origin main"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Push to GitHub: git push -u origin main"
echo "  2. Review: out/validation/FINAL_VALIDATION.md"
echo "  3. Release: ./scripts/release_all.sh"
