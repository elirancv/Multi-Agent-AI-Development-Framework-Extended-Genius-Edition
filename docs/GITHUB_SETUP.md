# GitHub Repository Setup Guide

## Initial Setup (New Repository)

If this is a new repository, follow these steps:

### 1. Check Current Status

```bash
# Check if git is initialized
git status

# Check current remotes
git remote -v

# Check current branch
git branch
```

### 2. Initialize Repository (if needed)

```bash
# Only if git is not initialized
git init
```

### 3. Add All Files

```bash
# Stage all files
git add .

# Commit
git commit -m "Initial commit: v1.0.0 release"
```

### 4. Set Main Branch

```bash
# Rename branch to main (if needed)
git branch -M main
```

### 5. Add Remote

```bash
# Add GitHub remote
git remote add origin https://github.com/elirancv/Multi-Agent-AI-Development-Framework-Extended-Genius-Edition.git

# Or if remote already exists, update it:
git remote set-url origin https://github.com/elirancv/Multi-Agent-AI-Development-Framework-Extended-Genius-Edition.git

# Verify remote
git remote -v
```

### 6. Push to GitHub

```bash
# Push main branch
git push -u origin main

# Push tags (if you have v1.0.0 tag)
git push origin --tags
```

## Pre-Push Checklist

Before pushing, ensure:

- [ ] `.gitignore` is configured correctly
- [ ] No sensitive data in files (API keys, passwords)
- [ ] All tests passing
- [ ] Documentation is complete
- [ ] Version is set to 1.0.0

## Recommended .gitignore Patterns

Make sure `.gitignore` includes:

```
# Python
__pycache__/
*.py[cod]
*.so
.Python
venv/
env/

# Project specific
out/
*.db
*.db-journal
*.dot
*.png
tmp_*/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

## Post-Push Actions

After pushing to GitHub:

1. **Verify Repository**
   - Check files are visible on GitHub
   - Verify README displays correctly
   - Check badges work

2. **Create Release**
   - Go to Releases → Draft new release
   - Tag: `v1.0.0`
   - Use `GITHUB_RELEASE_BODY_v1.0.0.md` content

3. **Enable GitHub Features**
   - Enable Issues
   - Enable Discussions
   - Enable Wiki (optional)
   - Set up branch protection (main branch)

4. **Configure CI/CD**
   - Verify GitHub Actions workflows are present
   - Check workflow permissions
   - Test workflow runs

## Troubleshooting

### Remote Already Exists

```bash
# Remove existing remote
git remote remove origin

# Add new remote
git remote add origin <new-url>
```

### Push Rejected

```bash
# If push is rejected, pull first
git pull origin main --allow-unrelated-histories

# Then push
git push -u origin main
```

### Large Files

If you have large files, consider:
- Using Git LFS for large artifacts
- Excluding `out/` directory
- Using `.gitignore` to exclude build artifacts

---

**Ready to push?** Run the commands in order, and verify each step succeeds before proceeding.
