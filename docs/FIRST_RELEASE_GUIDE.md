# First Release Guide - v1.0.0

## Quick Release (GitHub Web UI)

### Step 1: Create Release on GitHub

1. Go to: **https://github.com/elirancv/Multi-Agent-AI-Development-Framework-Extended-Genius-Edition/releases/new**

2. Fill in:
   - **Tag**: `v1.0.0`
   - **Title**: `Release v1.0.0`
   - **Description**: Copy from `docs/GITHUB_RELEASE_SHORT_v1.0.0.md` (see below)

3. Click **"Publish release"**

---

## Release Description (Copy-Paste)

```
🚀 Multi-Agent AI Development Framework v1.0.0

Production-ready orchestrator with 20+ agents, strict advisor council & policy-driven QA.
87/87 tests green. Start in 60s: `python cli.py --pipeline pipeline/production.yaml --preset mvp-fast`

**Full notes**: See [Release Notes](https://github.com/elirancv/Multi-Agent-AI-Development-Framework-Extended-Genius-Edition/blob/main/docs/GITHUB_RELEASE_BODY_v1.0.0.md)

**Stability Guarantees**: No breaking changes in 1.0.x
```

---

## Automated Release (Command Line)

### Option 1: Full Release Script

```powershell
.\scripts\release_all.ps1
```

This will:
- ✅ Run pre-flight checks
- ✅ Create signed tag `v1.0.0`
- ✅ Push tag to GitHub
- ✅ Bump version to `1.0.1-dev`
- ✅ Remind you to create GitHub Release

### Option 2: Manual Tag & Push

```powershell
# Create tag
git tag -s v1.0.0 -m "Release v1.0.0"

# Push tag
git push origin v1.0.0

# Then create release on GitHub web UI (see Step 1 above)
```

---

## After Release

1. **Verify Release**: Check https://github.com/elirancv/Multi-Agent-AI-Development-Framework-Extended-Genius-Edition/releases

2. **Check Badges**: Verify badges on README show correct version

3. **Monitor Workflows**: Check GitHub Actions are running successfully

4. **Set Secrets** (if needed):
   - CODECOV_TOKEN (for private repos or if required)
   - PYPI_TOKEN (for future PyPI publishing)

5. **Enable Branch Protection**: See `docs/GITHUB_PROTECTION_SETUP.md`

---

## Troubleshooting

### "Tag already exists"
**Fix**: Delete tag locally and remotely:
```powershell
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
```

### "Permission denied"
**Fix**: Ensure your token has `workflow` scope, or use GitHub web UI.

---

**Last Updated**: 2025-01-12
