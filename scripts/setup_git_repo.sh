#!/bin/bash
# Git Repository Setup Script for v1.0.0
# Run this script to initialize git and push to GitHub

set -e

echo "=== Git Repository Setup for v1.0.0 ==="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: Git is not installed"
    exit 1
fi

echo "Git found: $(git --version)"
echo ""

# Check if already a git repo
if [ -d ".git" ]; then
    echo "Warning: .git directory already exists"
    echo "Checking current status..."
    git status --short | head -10
    echo ""
    read -p "Continue with setup? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
else
    echo "[1/6] Initializing git repository..."
    git init
    echo "✅ Git repository initialized"
fi

# Check current branch
echo "[2/6] Checking branch..."
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "")
if [ -n "$CURRENT_BRANCH" ] && [ "$CURRENT_BRANCH" != "main" ]; then
    echo "Renaming branch to 'main'..."
    git branch -M main
fi
echo "✅ Branch: main"

# Add all files
echo "[3/6] Staging all files..."
git add .
STAGED_COUNT=$(git status --short | wc -l)
echo "✅ Staged $STAGED_COUNT files"

# Initial commit
echo "[4/6] Creating initial commit..."
git commit -m "chore: initial commit - v1.0.0 release"
echo "✅ Initial commit created"

# Create v1.0.0 tag
echo "[5/6] Creating v1.0.0 tag..."
git tag v1.0.0
echo "✅ Tag v1.0.0 created"

# Set remote
echo "[6/6] Setting up remote..."
REMOTE_URL="https://github.com/elirancv/Multi-Agent-AI-Development-Framework-Extended-Genius-Edition.git"

# Check if remote exists
if git remote get-url origin &>/dev/null; then
    EXISTING_URL=$(git remote get-url origin)
    echo "Remote 'origin' already exists: $EXISTING_URL"
    read -p "Update to new URL? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git remote set-url origin "$REMOTE_URL"
        echo "✅ Remote updated"
    fi
else
    git remote add origin "$REMOTE_URL"
    echo "✅ Remote added: $REMOTE_URL"
fi

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "Next steps:"
echo "1. Review changes: git status"
echo "2. Push to GitHub: git push -u origin main"
echo "3. Push tags: git push origin --tags"
echo ""
echo "Ready to push? Run:"
echo "  git push -u origin main"
echo "  git push origin --tags"
