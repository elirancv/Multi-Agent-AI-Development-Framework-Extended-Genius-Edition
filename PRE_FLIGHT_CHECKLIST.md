# Pre-Flight Checklist (Before Release)

Run these checks before creating the GitHub release.

## ✅ Pre-Flight Checks

### 1. Version Check
```bash
python cli.py --version
# Expected: 0.9.0
```
**Status**: ✅ PASSED

### 2. Smoke Tests JSON Output
```bash
python scripts/smoke_test.py --skip-slow --json
# Expected: Valid JSON with summary
```
**Status**: ✅ PASSED

### 3. Graph Export
```bash
python cli.py --pipeline pipeline/production.yaml --dry-run --export-graph out/pipeline.dot
# Expected: Graph exported successfully
```
**Status**: ✅ PASSED

### 4. Badges Check
- [x] Version badge points to correct branch (main)
- [x] Badge is dynamic (uses GitHub tag API)
- [x] All badges are valid URLs

### 5. Requirements Sync
- [x] `requirements.txt` versions match `pyproject.toml`
- [x] All dependencies have upper bounds
- [x] Scripts entry point configured (`multiagent = cli:main`)

### 6. Documentation
- [x] `CHANGELOG.md` updated
- [x] `RELEASE_NOTES_v0.9.0.md` created
- [x] `docs/INDEX.md` has Quick Links
- [x] `README.md` badges updated

### 7. GitHub Templates
- [x] `.github/ISSUE_TEMPLATE/bug.md` exists
- [x] `.github/ISSUE_TEMPLATE/feature.md` exists
- [x] `.github/pull_request_template.md` exists
- [x] `.github/dependabot.yml` configured

### 8. CI/CD
- [x] Smoke tests workflow exists
- [x] Release bundle workflow exists
- [x] All tests passing (87/87)

## 🚀 Release Commands

### Step 1: Update Version for Post-Release
```bash
# Update src/__init__.py to 0.9.1-dev
sed -i 's/__version__ = "0.9.0"/__version__ = "0.9.1-dev"/' src/__init__.py
```

### Step 2: Commit Pre-Release Changes
```bash
git add .
git commit -m "chore: prepare for v0.9.0 release"
```

### Step 3: Create Tag
```bash
git tag v0.9.0
git push origin v0.9.0
```

### Step 4: Create GitHub Release
1. Go to [Releases](https://github.com/your-org/AgentsSystemV2/releases)
2. Click "Draft a new release"
3. **Tag**: `v0.9.0`
4. **Title**: `v0.9.0 – Production-ready Orchestrator`
5. **Description**: Copy from `GITHUB_RELEASE_BODY.md`
6. **Attach artifacts** (if release-bundle workflow created them)
7. Check "Set as the latest release"
8. Publish release

### Step 5: Post-Release
```bash
# Commit version bump
git add src/__init__.py
git commit -m "chore: bump version to 0.9.1-dev"
git push origin main
```

## 📋 Post-Release Tasks

See [POST_RELEASE_CHECKLIST.md](POST_RELEASE_CHECKLIST.md) for:
- Opening tracking issues
- Enabling Dependabot
- Configuring branch protection
- Security audit

## ✅ Final Checklist

- [ ] All pre-flight checks passed
- [ ] Version bumped to 0.9.1-dev
- [ ] Tag created and pushed
- [ ] GitHub release created
- [ ] Release bundle uploaded (if workflow ran)
- [ ] Post-release tasks started

---

**Ready to release!** 🎉
