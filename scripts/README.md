# Release Scripts

Automated scripts for release preparation, testing, and deployment.

## Quick Start

### Bash (Linux/macOS)

```bash
chmod +x scripts/commit_push.sh
./scripts/commit_push.sh
```

### PowerShell (Windows)

```powershell
.\scripts\commit_push.ps1
```

## Scripts

- **`commit_push.sh`** - Bash script for Linux/macOS
- **`commit_push.ps1`** - PowerShell script for Windows

## Features

- ✅ Formatting & linting (pre-commit, ruff, mypy)
- ✅ Testing (pytest, smoke tests)
- ✅ Documentation generation (pdoc, pipeline graph)
- ✅ Git operations (add, commit, push)
- ✅ Tag creation (optional, with GPG signing)

## Documentation

See [docs/SCRIPTS_USAGE.md](../docs/SCRIPTS_USAGE.md) for complete usage guide.

## Examples

### Create Release Tag (Bash)

```bash
CREATE_TAG=true SIGN_TAG=true TAG_NAME=v1.0.0 ./scripts/commit_push.sh
```

### Create Release Tag (PowerShell)

```powershell
.\scripts\commit_push.ps1 -CreateTag:$true -SignTag:$true -TagName "v1.0.0"
```

### Dry Run (Test Without Push)

```bash
# Bash
DRY_RUN=true ./scripts/commit_push.sh

# PowerShell
.\scripts\commit_push.ps1 -DryRun:$true
```
