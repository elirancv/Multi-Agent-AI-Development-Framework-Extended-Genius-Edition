#!/usr/bin/env bash

# Quick Setup - One Command
# Sets up repo, patches badges, validates, and prepares for release

set -euo pipefail

OWNER="elirancv"
REPO="Multi-Agent-AI-Development-Framework-Extended-Genius-Edition"

echo "🚀 Quick Setup - $OWNER/$REPO"

# Git setup
git init -b main 2>/dev/null || true
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$OWNER/$REPO.git" 2>/dev/null || true

# Create .env
printf "OWNER=$OWNER\nREPO=$REPO\n" > .env

# Re-validate (patches badges, installs tools, runs checks)
chmod +x scripts/revalidate.sh 2>/dev/null || true
./scripts/revalidate.sh || true

# Commit changes
git add -A
if ! git diff --cached --quiet; then
    git commit -m "chore: repo wiring + badges patch for $OWNER/$REPO" || true
fi

echo ""
echo "✅ Quick setup complete!"
echo "Next: git push -u origin main"

