# Production Demo Checklist - Idea-to-ZIP

## 48-Hour Goal: Perfect Production Demo

### Step 1: Run Production Pipeline

```bash
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline-production-demo.yaml \
  --mem 'product_idea="Coffee shop" brand="BlueBean" primary_color="#0ea5e9" tone="minimal" font_family="Inter"' \
  --save-artifacts --output human
```

### Step 2: Verify Outputs

**Check ZIP Contents**:
```bash
unzip -l "out/<run_id>/Package ZIP/package.zip"
```

**Expected Files**:
- ✅ `index.html`
- ✅ `README.md`
- ✅ `lint_report.md`
- ✅ `a11y_report.md`
- ✅ `preview.png` (screenshot)
- ✅ `MANIFEST.txt`

### Step 3: Test Multiple Variations

Run with different design variables:

```bash
# Variation 1: Minimal
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline-production-demo.yaml \
  --mem 'product_idea="Coffee shop" brand="BlueBean" primary_color="#0ea5e9" tone="minimal"' \
  --save-artifacts

# Variation 2: Professional
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline-production-demo.yaml \
  --mem 'product_idea="Coffee shop" brand="BlueBean" primary_color="#1e40af" tone="professional"' \
  --save-artifacts

# Variation 3: Playful
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline-production-demo.yaml \
  --mem 'product_idea="Coffee shop" brand="BlueBean" primary_color="#f59e0b" tone="playful"' \
  --save-artifacts
```

### Step 4: Run Integration Tests

```bash
pytest tests/test_idea_to_zip_integration.py -v
```

**Expected**: All tests pass ✅

### Step 5: Prepare Release Assets

```bash
# Copy best ZIP to release directory
cp "out/<best_run_id>/Package ZIP/package.zip" release-assets/demo-package.zip
cp "out/<best_run_id>/SUMMARY.md" release-assets/demo-summary.md
```

### Step 6: Add to GitHub Release

1. Go to: https://github.com/elirancv/Multi-Agent-AI-Development-Framework-Extended-Genius-Edition/releases
2. Edit release v1.0.0
3. Attach files:
   - `demo-package.zip`
   - `demo-summary.md`

---

## Definition of Done

- ✅ ZIP includes all required files (HTML, README, reports, screenshot, manifest)
- ✅ Pipeline passes E2E with 3+ different design variations
- ✅ Integration tests pass (`pytest tests/test_idea_to_zip_integration.py`)
- ✅ ZIP extracts and HTML loads in browser without errors
- ✅ Release assets uploaded to GitHub Release

---

## Troubleshooting

### Screenshot is placeholder

**Fix**: Install screenshot tools:
```bash
pip install playwright
playwright install chromium
```

### Quality gates too strict

**Fix**: Lower thresholds in `pipeline-production-demo.yaml`:
```yaml
thresholds:
  validation: 0.70  # Lower from 0.75
```

### ZIP missing files

**Fix**: Check that previous stages produced artifacts. Run with `--output human` to debug.

---

**Last Updated**: 2025-01-12
