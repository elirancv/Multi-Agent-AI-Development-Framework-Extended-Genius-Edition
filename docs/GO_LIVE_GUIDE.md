# GO-LIVE Guide - Complete Release Automation

One-command release automation for v1.0.0+ with full validation, asset generation, and GitHub release creation.

## Quick Start

### Bash (Linux/macOS)

```bash
chmod +x scripts/go_live.sh
./scripts/go_live.sh
```

### PowerShell (Windows)

```powershell
.\scripts\go_live.ps1
```

### Custom Configuration

```bash
# Bash
./scripts/go_live.sh "GrindLab" "#16a34a" "playful" "Poppins" "Coffee gear landing" "v1.0.0"

# PowerShell
.\scripts\go_live.ps1 -Brand "GrindLab" -Color "#16a34a" -Tone "playful" -Font "Poppins" -Product "Coffee gear landing" -Version "v1.0.0"
```

---

## What It Does (8 Steps)

1. **Update Badges** - Configures `.env` with owner/repo
2. **Install Screenshot Tools** - Installs Playwright + Chromium
3. **Run Production Demo** - Executes full pipeline with your brand/color/tone
4. **Integration Tests** - Validates ZIP, screenshot, HTML
5. **Smoke + Validation** - Quick sanity checks
6. **Verify Outputs** - Checks ZIP size, screenshot size (>30KB)
7. **Create GitHub Release** - Auto-finds assets and creates release
8. **Post-Release Bump** - Bumps version to `1.0.1-dev`

---

## Prerequisites

- **Python 3.8+** installed
- **Git** configured
- **GitHub CLI** (`gh`) authenticated: `gh auth login`
- **Write permissions** to repository

---

## Outputs

After successful run:

- ✅ **ZIP Package**: `out/<run_id>/Package ZIP/package.zip`
  - Contains: `index.html`, `README.md`, `lint_report.md`, `a11y_report.md`, `MANIFEST.txt`, `screenshot.png`
- ✅ **Screenshot**: `out/<run_id>/Screenshot/preview.png` (>30KB)
- ✅ **GitHub Release**: Created with all assets attached
- ✅ **Version Bump**: `src/__init__.py` updated to `1.0.1-dev`

---

## Manual Verification

### Test ZIP Locally

```bash
# Bash
unzip "out/<run_id>/Package ZIP/package.zip" -d out/demo/
python -m http.server -d out/demo 8000

# PowerShell
Expand-Archive "out/<run_id>/Package ZIP/package.zip" -DestinationPath out/demo/
python -m http.server -d out/demo 8000
```

Open: http://localhost:8000

---

## Troubleshooting

### Screenshot Too Small (<30KB)

**Fix**: Install Playwright
```bash
pip install playwright && playwright install chromium
```

### Release Creation Failed

**Fix**: Authenticate GitHub CLI
```bash
gh auth login
```

### Badges Not Updated

**Fix**: Manual `.env` edit
```bash
OWNER=elirancv
REPO=Multi-Agent-AI-Development-Framework-Extended-Genius-Edition
```

Then run: `./scripts/revalidate.sh`

### Pipeline Failed

**Check**:
- All dependencies installed: `pip install -r requirements.txt`
- Python version: `python --version` (3.8+)
- Disk space available

---

## Post-Release Steps

1. **Verify Release**: https://github.com/elirancv/Multi-Agent-AI-Development-Framework-Extended-Genius-Edition/releases
2. **Create v1.1 Issues**:
   ```bash
   ./scripts/create_v1.1_issues.sh
   ```
3. **Trigger Workflows**:
   ```bash
   gh workflow run production-demo.yml
   gh workflow run hard-tests-nightly.yml
   ```

---

## Marketing-First Showcase (Optional)

After main release, showcase marketing-first pipeline:

```bash
# Bash
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline-marketing-first.yaml \
  --mem 'product_idea="Coffee gear landing" brand="GrindLab" primary_color="#16a34a" tone="playful" font_family="Poppins"' \
  --save-artifacts --output human

# PowerShell
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline-marketing-first.yaml `
  --mem 'product_idea="Coffee gear landing" brand="GrindLab" primary_color="#16a34a" tone="playful" font_family="Poppins"' `
  --save-artifacts --output human
```

---

**Last Updated**: 2025-01-12
