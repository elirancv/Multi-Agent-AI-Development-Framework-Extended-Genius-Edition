# Release with Assets Guide

Complete guide for creating GitHub Releases with production demo assets.

## Quick Release

### Bash

```bash
chmod +x scripts/create_release_with_assets.sh
./scripts/create_release_with_assets.sh v1.0.0
```

### PowerShell

```powershell
.\scripts\create_release_with_assets.ps1 -Tag "v1.0.0"
```

### With Custom Title/Notes

```bash
./scripts/create_release_with_assets.sh v1.0.0 "Release v1.0.0" docs/GITHUB_RELEASE_BODY_v1.0.0.md
```

---

## What It Does

1. **Finds Latest Run**: Automatically finds the most recent production demo run
2. **Runs Pipeline** (if needed): If no runs found, runs production demo pipeline
3. **Collects Assets**: Finds ZIP, summary, and screenshot
4. **Creates Release**: Uses GitHub CLI to create release with assets attached

---

## Assets Attached

- ✅ `package.zip` - Complete demo package
- ✅ `SUMMARY.md` - Full execution report
- ✅ `preview.png` - Screenshot preview

---

## Prerequisites

1. **GitHub CLI**: `gh auth login`
2. **Production Demo Run**: Either run manually first, or script will run it
3. **Write Permissions**: Must have write access to repository

---

## Troubleshooting

### "Tag already exists"

**Fix**: Delete tag first:
```bash
gh release delete v1.0.0 --yes
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
```

### "No runs found"

**Fix**: Script will run pipeline automatically, or run manually:
```bash
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline-production-demo.yaml \
  --mem 'product_idea="Demo" brand="Test" primary_color="#0ea5e9" tone="minimal"' \
  --save-artifacts
```

### "GitHub CLI not authenticated"

**Fix**: Authenticate:
```bash
gh auth login
```

---

## Manual Release (Alternative)

If you prefer manual control:

1. **Run Pipeline**:
   ```bash
   python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline-production-demo.yaml \
     --mem 'product_idea="Coffee shop" brand="BlueBean" primary_color="#0ea5e9" tone="minimal"' \
     --save-artifacts --output human
   ```

2. **Find Assets**:
   ```bash
   LATEST_RUN=$(ls -t out/ | grep -v "^\." | head -1)
   ZIP_PATH="out/$LATEST_RUN/Package ZIP/package.zip"
   SUMMARY_PATH="out/$LATEST_RUN/SUMMARY.md"
   SCREENSHOT_PATH="out/$LATEST_RUN/Screenshot/preview.png"
   ```

3. **Create Release**:
   ```bash
   gh release create v1.0.0 \
     --title "Release v1.0.0" \
     --notes-file docs/GITHUB_RELEASE_SHORT_v1.0.0.md \
     -a "$ZIP_PATH" \
     -a "$SUMMARY_PATH" \
     -a "$SCREENSHOT_PATH"
   ```

---

**Last Updated**: 2025-01-12
