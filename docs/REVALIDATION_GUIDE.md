# Re-Validation Guide - Turn YELLOW → GREEN

Quick guide to re-validate the project and turn status from YELLOW to GREEN.

---

## Quick Start

### Option 1: Using .env file (Recommended)

1. **Create `.env` file** (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env`** and set your values:
   ```env
   OWNER=myusername
   REPO=multiagent-framework
   ```

3. **Run re-validation**:

   **Bash**:
   ```bash
   chmod +x scripts/revalidate.sh
   ./scripts/revalidate.sh
   ```

   **PowerShell**:
   ```powershell
   .\scripts\revalidate.ps1
   ```

### Option 2: Using Environment Variables

**Bash**:
```bash
export OWNER=myusername
export REPO=multiagent-framework
./scripts/revalidate.sh
```

**PowerShell**:
```powershell
$env:OWNER = "myusername"
$env:REPO = "multiagent-framework"
.\scripts\revalidate.ps1
```

---

## What the Script Does

1. **Installs Optional Tools**:
   - `pdoc` - API documentation generator
   - `pre-commit` - Git hooks
   - `graphviz` - Graph visualization (Python package + system if available)
   - `coverage` - Code coverage

2. **Patches Badge URLs**:
   - Automatically replaces `your-org/AgentsSystemV2` → `<owner>/<repo>` in README.md
   - Only if OWNER and REPO are set

3. **Runs All Checks**:
   - Doctor diagnostics
   - Version check
   - Dry-run validation
   - Smoke tests
   - Coverage generation
   - Release dry-run

4. **Generates Reports**:
   - `out/validation/FINAL_VALIDATION.md` - Human-readable report
   - `out/validation/FINAL_VALIDATION.json` - Machine-readable summary

---

## Expected Output

**Status**: 🟢 **GREEN** (if all core checks pass)

**Key Results**:
- ✅ Version: 1.0.0
- ✅ Dry-run: PASSED
- ✅ Smoke tests: PASSED
- ✅ Badge URLs: Updated (if OWNER/REPO set)
- ✅ Optional tools: Installed

---

## Manual Badge Update (if not using script)

If you prefer to update badges manually:

1. Open `README.md`
2. Find and replace (4 instances):
   - `your-org/AgentsSystemV2` → `<owner>/<repo>`
3. Lines to check: 3, 4, 9, 77

---

## Troubleshooting

### Script Fails on Tool Installation

**Issue**: Some tools fail to install

**Fix**: Script continues anyway (tools are optional). Check warnings in report.

### Badge URLs Not Updated

**Issue**: OWNER/REPO not set

**Fix**: 
- Set in `.env` file, OR
- Set as environment variables, OR
- Update manually in README.md

### Graphviz System Command Not Found

**Issue**: `dot` command not available

**Fix**: 
- **Windows**: `choco install graphviz` or `scoop install graphviz`
- **Linux**: `sudo apt-get install graphviz`
- **macOS**: `brew install graphviz`

**Note**: Python package works for graph export, system command is optional.

---

## After Re-Validation

If status is **GREEN**:

**Bash**:
```bash
CREATE_TAG=true SIGN_TAG=true TAG_NAME=v1.0.0 ./scripts/commit_push.sh
```

**PowerShell**:
```powershell
.\scripts\commit_push.ps1 -CreateTag:$true -SignTag:$true -TagName "v1.0.0"
```

---

**Last Updated**: 2025-01-12

