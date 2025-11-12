# Pre-Release Sanity Checks

Quick checklist to run before tagging v1.0.0.

## ✅ Required Checks

### 1. Doctor Command
```bash
python scripts/doctor.py --verbose
```
**Expected**: Exit code 0, all checks pass

### 2. Dependency Audit
```bash
python scripts/deps_audit.py
```
**Expected**: All dependencies have allowed licenses (MIT/Apache2/BSD)

### 3. Smoke Tests
```bash
python scripts/smoke_test.py --skip-slow --json
```
**Expected**: Tests pass (may fail without artifacts in dry-run - OK)

### 4. Version Check
```bash
python cli.py --version
```
**Expected**: Outputs `1.0.0`

### 5. Dry-Run Pipeline
```bash
python cli.py --pipeline pipeline/production.yaml --dry-run --export-graph out/pipeline.dot
```
**Expected**: Pipeline validates, graph exported

## ✅ Optional Checks

### API Docs Generation
```bash
pdoc -o docs/api src
```
**Expected**: API docs generated in `docs/api/`

### Coverage Report
```bash
pip install coverage
coverage run -m pytest
coverage xml -o coverage.xml
coverage report
```
**Expected**: Coverage report generated

### Build Check
```bash
python -m pip install --upgrade build twine
python -m build
twine check dist/*
```
**Expected**: Package builds successfully, passes validation

## ✅ Script Dry-Run

### Bash
```bash
DRY_RUN=true ./scripts/commit_push.sh
```

### PowerShell
```powershell
.\scripts\commit_push.ps1 -DryRun:$true
```

**Expected**: All checks run, no actual push

## ✅ Final Verification

- [ ] All required checks pass
- [ ] Version is 1.0.0
- [ ] No blocking errors
- [ ] Warnings reviewed and acceptable
- [ ] Ready to tag and release

## Release Commands

Once all checks pass:

```bash
# Bash
CREATE_TAG=true SIGN_TAG=true TAG_NAME=v1.0.0 ./scripts/commit_push.sh

# PowerShell
.\scripts\commit_push.ps1 -CreateTag:$true -SignTag:$true -TagName "v1.0.0"
```

## See Also

- [Release Checklist](RELEASE_CHECKLIST_v1.0.0.md)
- [Definition of Done](DEFINITION_OF_DONE_v1.0.md)
- [Release Verification](RELEASE_VERIFICATION.md)

