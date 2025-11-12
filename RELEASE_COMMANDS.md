# Release Commands for v1.0.0

## Pre-Release: Go/No-Go Checks

### Windows PowerShell
```powershell
pwsh -File scripts/go_no_go_check.ps1
```

### Linux/macOS
```bash
bash scripts/go_no_go_check.sh
```

**Expected Output**: All 5 checks should pass ✅

## Release Steps

### 1. Final Verification
```bash
# Check version
python cli.py --version  # Should show: 1.0.0

# Test dry-run
python cli.py --pipeline pipeline/production.yaml --dry-run --export-graph out/pipeline.dot

# Run smoke tests
python scripts/smoke_test.py --skip-slow --json
```

### 2. Commit & Tag
```bash
# Stage all changes
git add .

# Commit
git commit -m "chore: release v1.0.0"

# Create tag
git tag v1.0.0

# Push to remote
git push origin main --tags
```

### 3. Generate API Docs (Optional)
```bash
pip install pdoc
pdoc -o docs/api src
```

### 4. Create GitHub Release

1. Go to GitHub → Releases → Draft new release
2. **Tag**: `v1.0.0`
3. **Title**: `Release v1.0.0`
4. **Description**: Copy content from `GITHUB_RELEASE_BODY_v1.0.0.md`
5. **Attach artifacts** (if available):
   - `out/pipeline.dot` (pipeline graph)
   - `out/smoke/SMOKE_SUMMARY.md` (smoke test results)
   - `pipeline/production.yaml` (example pipeline)

### 5. Post-Release Verification

```bash
# Trigger nightly hard tests manually
# Go to GitHub Actions → Hard Tests Nightly → Run workflow

# Verify retention weekly job is scheduled
# Go to GitHub Actions → Artifact Retention (Weekly) → Check schedule
```

## Rollback (If Needed)

See [docs/ROLLBACK_PLAN.md](docs/ROLLBACK_PLAN.md) for detailed rollback steps.

Quick rollback:
```bash
git revert <commit_sha>
git tag v1.0.1
git push origin main --tags
```

## Monitoring Checklist

### First 24 Hours
- [ ] Monitor GitHub Issues
- [ ] Check CI/CD status
- [ ] Verify nightly tests run
- [ ] Check retention job schedule

### First Week
- [ ] Review KPI metrics
- [ ] Check cleanup reports
- [ ] Monitor error rates
- [ ] Collect user feedback

---

**Status**: Ready for release! 🚀

