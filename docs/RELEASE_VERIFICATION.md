# Release Verification Checklist

Quick checklist to verify everything is ready before pushing the release.

## Pre-Push Verification

### 1. Version Check

```bash
# Verify version in code
python -c "from src import __version__; print(__version__)"
# Should output: 1.0.0

# Verify CLI version
python cli.py --version
# Should output: 1.0.0
```

### 2. Badges Check

Verify all badges in `README.md` point to correct URLs:
- [ ] Version badge points to releases
- [ ] CI badge points to correct workflow
- [ ] Tests badge shows correct count (87/87)
- [ ] Nightly Tests badge points to workflow
- [ ] API Docs badge points to docs/api/

### 3. Documentation

- [ ] `README.md` is up to date
- [ ] `docs/QUICKSTART.md` exists and is accurate
- [ ] `docs/INDEX.md` exists and links work
- [ ] API docs generated: `docs/api/` exists (if using pdoc)

### 4. Tests

```bash
# Run all tests
pytest -q
# Should pass: 87/87

# Run smoke tests
python scripts/smoke_test.py --skip-slow --json
# Should complete without errors
```

### 5. Linting & Formatting

```bash
# Run pre-commit (if available)
pre-commit run --all-files

# Run ruff
ruff check --fix .

# Run mypy (if available)
mypy .
```

### 6. Release Files

- [ ] `GITHUB_RELEASE_BODY_v1.0.0.md` exists
- [ ] `docs/GITHUB_RELEASE_SHORT_v1.0.0.md` exists
- [ ] `docs/ANNOUNCEMENT_v1.0.0.md` exists
- [ ] `docs/RELEASE_CHECKLIST_v1.0.0.md` exists
- [ ] `CODE_OF_CONDUCT.md` exists

### 7. Scripts

```bash
# Test release script (dry-run)
DRY_RUN=true ./scripts/commit_push.sh
# OR PowerShell:
.\scripts\commit_push.ps1 -DryRun:$true
```

### 8. Pipeline Graph

```bash
# Export pipeline graph
python cli.py --pipeline pipeline/production.yaml --dry-run --export-graph out/pipeline.dot
# Should create: out/pipeline.dot
```

### 9. Git Status

```bash
# Check what will be committed
git status

# Verify no temporary files
git diff --cached --name-only
# Should not include: tmp/, sandbox/, *.tmp, *.log
```

## Post-Push Verification

### 1. GitHub Release

- [ ] Release created on GitHub
- [ ] Tag `v1.0.0` exists
- [ ] Release body is correct
- [ ] Assets attached (if any)

### 2. CI/CD

- [ ] CI workflow passes
- [ ] Smoke tests pass
- [ ] Nightly tests scheduled
- [ ] SBOM generated (if workflow enabled)

### 3. Documentation

- [ ] API docs published (if using GitHub Pages)
- [ ] Links in README work
- [ ] Badges show correct status

### 4. Announcements

- [ ] GitHub Release published
- [ ] Announcements posted (if applicable)
- [ ] Links shared (if applicable)

## Quick Verification Script

```bash
#!/bin/bash
set -e

echo "🔍 Pre-Release Verification"

echo "1. Version check..."
VERSION=$(python -c "from src import __version__; print(__version__)")
echo "   Version: $VERSION"
[ "$VERSION" = "1.0.0" ] || { echo "❌ Version mismatch!"; exit 1; }

echo "2. Tests..."
pytest -q || { echo "❌ Tests failed!"; exit 1; }

echo "3. Smoke tests..."
python scripts/smoke_test.py --skip-slow --json > /dev/null || { echo "❌ Smoke tests failed!"; exit 1; }

echo "4. Git status..."
git status --short

echo "✅ All checks passed!"
```

## PowerShell Version

```powershell
Write-Host "🔍 Pre-Release Verification"

Write-Host "1. Version check..."
$version = python -c "from src import __version__; print(__version__)"
Write-Host "   Version: $version"
if ($version -ne "1.0.0") { Write-Host "❌ Version mismatch!"; exit 1 }

Write-Host "2. Tests..."
pytest -q
if ($LASTEXITCODE -ne 0) { Write-Host "❌ Tests failed!"; exit 1 }

Write-Host "3. Smoke tests..."
python scripts/smoke_test.py --skip-slow --json | Out-Null
if ($LASTEXITCODE -ne 0) { Write-Host "❌ Smoke tests failed!"; exit 1 }

Write-Host "4. Git status..."
git status --short

Write-Host "✅ All checks passed!"
```

## See Also

- [Release Checklist](docs/RELEASE_CHECKLIST_v1.0.0.md)
- [Scripts Usage](docs/SCRIPTS_USAGE.md)
- [Release Summary](docs/RELEASE_SUMMARY.md)
