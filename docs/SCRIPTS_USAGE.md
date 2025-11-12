# Release Scripts Usage Guide

This document describes how to use the automated release scripts for committing, testing, and pushing changes.

## Overview

The `scripts/commit_push.sh` (Bash) and `scripts/commit_push.ps1` (PowerShell) scripts automate the release process:

1. **Formatting & Linting**: Runs pre-commit, ruff, mypy
2. **Testing**: Runs pytest and smoke tests
3. **Documentation**: Generates API docs (pdoc) and pipeline graph
4. **Git Operations**: Stages, commits, and pushes changes
5. **Tagging** (optional): Creates and pushes version tags

## Bash Script (Linux/macOS)

### Basic Usage

```bash
# Make executable (first time only)
chmod +x scripts/commit_push.sh

# Run script
./scripts/commit_push.sh
```

### With Tag Creation

```bash
# Create unsigned tag
CREATE_TAG=true TAG_NAME=v1.0.0 ./scripts/commit_push.sh

# Create signed tag (requires GPG)
CREATE_TAG=true SIGN_TAG=true TAG_NAME=v1.0.0 ./scripts/commit_push.sh
```

### Dry Run (No Push)

```bash
# Test without pushing
DRY_RUN=true ./scripts/commit_push.sh
```

### All Options

```bash
CREATE_TAG=true \
SIGN_TAG=true \
TAG_NAME=v1.0.0 \
DRY_RUN=false \
./scripts/commit_push.sh
```

## PowerShell Script (Windows)

### Basic Usage

```powershell
# Set execution policy (first time only, if needed)
Set-ExecutionPolicy -Scope Process RemoteSigned

# Run script
.\scripts\commit_push.ps1
```

### With Tag Creation

```powershell
# Create unsigned tag
.\scripts\commit_push.ps1 -CreateTag:$true -TagName "v1.0.0"

# Create signed tag (requires GPG)
.\scripts\commit_push.ps1 -CreateTag:$true -SignTag:$true -TagName "v1.0.0"
```

### Dry Run (No Push)

```powershell
# Test without pushing
.\scripts\commit_push.ps1 -DryRun:$true
```

### All Options

```powershell
.\scripts\commit_push.ps1 `
  -BranchDefault "main" `
  -CreateTag:$true `
  -TagName "v1.0.0" `
  -SignTag:$true `
  -DryRun:$false
```

## What the Scripts Do

### Step 1: Detect Branch & Remote
- Detects current git branch (defaults to `main`)
- Detects git remote (defaults to `origin`)

### Step 2: Formatting & Linting
- Installs/runs `pre-commit` hooks
- Runs `ruff check --fix` for code formatting
- Runs `mypy` for type checking (if available)

### Step 3: Tests
- Runs `pytest -q` (quiet mode)
- Runs `scripts/smoke_test.py --skip-slow`

### Step 4: Build Docs (Optional)
- Generates API docs with `pdoc -o docs/api src`
- Continues if pdoc fails or is not available

### Step 5: Export Graph (Optional)
- Exports pipeline graph: `python cli.py --pipeline pipeline/production.yaml --dry-run --export-graph out/pipeline.dot`
- Continues if graphviz/graph export fails

### Step 6: Git Add & Commit
- Stages all changes: `git add -A`
- Creates commit with Conventional Commit message
- Includes version from `src/__version__`
- Skips commit if no staged changes

### Step 7: Push
- Pushes to remote branch
- Creates and pushes tag (if `CREATE_TAG=true`)
- Signs tag (if `SIGN_TAG=true`)

## Commit Message Format

The script generates a Conventional Commit message:

```
chore(repo): tidy project & release bundle

- run pre-commit, ruff fix, type-checks
- run tests & smoke
- update docs/api (if available) & export graph
- prepare release assets

Version: 1.0.0
```

## Environment Variables (Bash)

| Variable | Default | Description |
|----------|---------|-------------|
| `CREATE_TAG` | `false` | Set to `true` to create a tag |
| `TAG_NAME` | `v1.0.0` | Tag name to create |
| `SIGN_TAG` | `false` | Set to `true` to sign tag with GPG |
| `DRY_RUN` | `false` | Set to `true` to skip push |

## Parameters (PowerShell)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `BranchDefault` | `string` | `main` | Default branch name |
| `CreateTag` | `bool` | `false` | Create a tag |
| `TagName` | `string` | `v1.0.0` | Tag name |
| `SignTag` | `bool` | `false` | Sign tag with GPG |
| `DryRun` | `bool` | `false` | Skip push |

## Prerequisites

### Required Tools
- `git` - Version control
- `python` - Python interpreter
- `pytest` - Testing framework

### Optional Tools
- `pre-commit` - Pre-commit hooks
- `ruff` - Code formatter/linter
- `mypy` - Type checker
- `pdoc` - API documentation generator
- `graphviz` - Graph visualization (for pipeline export)
- `gpg` - GPG signing (for signed tags)

## Quick Cleanup Check

Before/after running the script, you can manually verify:

```bash
# Format & lint
pre-commit run --all-files
ruff check --fix .

# Tests
pytest -q
python scripts/smoke_test.py --skip-slow

# Docs (optional)
pdoc -o docs/api src

# Graph (optional)
python cli.py --pipeline pipeline/production.yaml --dry-run --export-graph out/pipeline.dot
```

## Troubleshooting

### Script Fails on Pre-commit
- Install pre-commit: `pip install pre-commit`
- Or skip by removing pre-commit step from script

### Script Fails on Ruff/Mypy
- Install: `pip install ruff mypy`
- Or these steps are skipped if tools are not found

### Script Fails on Tests
- Fix failing tests before running script
- Or modify script to continue on test failures (not recommended)

### GPG Signing Fails
- Ensure GPG is configured: `gpg --list-secret-keys`
- Or use unsigned tag: `SIGN_TAG=false`

### PowerShell Execution Policy Error
```powershell
Set-ExecutionPolicy -Scope Process RemoteSigned
```

## Examples

### Release v1.0.0 (Bash)

```bash
CREATE_TAG=true SIGN_TAG=true TAG_NAME=v1.0.0 ./scripts/commit_push.sh
```

### Release v1.0.0 (PowerShell)

```powershell
.\scripts\commit_push.ps1 -CreateTag:$true -SignTag:$true -TagName "v1.0.0"
```

### Test Run Without Push (Bash)

```bash
DRY_RUN=true ./scripts/commit_push.sh
```

### Test Run Without Push (PowerShell)

```powershell
.\scripts\commit_push.ps1 -DryRun:$true
```

## Integration with Release Checklist

These scripts are designed to work with `docs/RELEASE_CHECKLIST_v1.0.0.md`:

1. Run script with `DRY_RUN=true` first to verify
2. Run script with `CREATE_TAG=true` for actual release
3. Verify release on GitHub
4. Complete post-release checklist items

## See Also

- [Release Checklist](docs/RELEASE_CHECKLIST_v1.0.0.md)
- [Semantic Release Guidelines](docs/SEMANTIC_RELEASE.md)
- [Release Summary](docs/RELEASE_SUMMARY.md)
