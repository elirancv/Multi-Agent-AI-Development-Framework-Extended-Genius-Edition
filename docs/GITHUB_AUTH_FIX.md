# GitHub Authentication Fix

## Problem

Push failed with error:
```
refusing to allow a Personal Access Token to create or update workflow `.github/workflows/api-docs.yml` without `workflow` scope
```

## Solutions

### Option 1: Update Personal Access Token (Recommended)

1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Create new token or edit existing one
3. **Required scopes:**
   - ✅ `repo` (full control)
   - ✅ `workflow` (update GitHub Action workflows)
4. Copy new token
5. Update git credentials:
   ```bash
   git remote set-url origin https://<YOUR_TOKEN>@github.com/elirancv/Multi-Agent-AI-Development-Framework-Extended-Genius-Edition.git
   ```

### Option 2: Use SSH (Alternative)

1. Generate SSH key (if you don't have one):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. Add SSH key to GitHub:
   - Copy public key: `cat ~/.ssh/id_ed25519.pub`
   - GitHub → Settings → SSH and GPG keys → New SSH key

3. Change remote to SSH:
   ```bash
   git remote set-url origin git@github.com:elirancv/Multi-Agent-AI-Development-Framework-Extended-Genius-Edition.git
   ```

4. Push again:
   ```bash
   git push -u origin main
   git push origin --tags
   ```

### Option 3: Use GitHub CLI (Easiest)

1. Install GitHub CLI: https://cli.github.com/
2. Authenticate:
   ```bash
   gh auth login
   ```
3. Push:
   ```bash
   git push -u origin main
   git push origin --tags
   ```

### Option 4: Push Without Workflows (Temporary)

If you just want to push the code without workflows first:

1. Temporarily remove workflows:
   ```bash
   git rm .github/workflows/api-docs.yml
   git commit -m "temp: remove workflow for initial push"
   git push -u origin main
   ```

2. Then add workflows back:
   ```bash
   git checkout HEAD~1 -- .github/workflows/api-docs.yml
   git commit -m "chore: restore workflow files"
   git push origin main
   ```

## Recommended: Use GitHub CLI

The easiest solution is to use GitHub CLI:

```bash
# Install GitHub CLI (if not installed)
# Windows: winget install GitHub.cli
# macOS: brew install gh
# Linux: See https://cli.github.com/manual/installation

# Authenticate
gh auth login

# Push
git push -u origin main
git push origin --tags
```

---

**After fixing authentication, run:**
```bash
git push -u origin main
git push origin --tags
```

