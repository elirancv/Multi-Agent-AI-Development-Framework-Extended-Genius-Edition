# Idea-to-ZIP Pipeline Guide

Complete guide for using and extending the "From Idea to ZIP" pipeline.

## Quick Start

### Basic Run

```bash
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline.yaml \
  --mem 'product_idea="A simple landing page for a coffee shop"' \
  --save-artifacts --output human
```

### With Design Variables

```bash
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline-with-design.yaml \
  --mem 'product_idea="Coffee shop" brand="BlueBean" primary_color="#0ea5e9" tone="minimal" font_family="Inter"' \
  --save-artifacts --output human
```

### With Preset

```bash
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline.yaml \
  --preset idea-to-zip \
  --mem 'product_idea="Demo site"' \
  --save-artifacts --output human
```

---

## E2E Testing Checklist

### 1. Dry-Run (Validation)

```bash
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline.yaml \
  --dry-run --export-graph out/pipeline.dot
```

**Expected**: Pipeline validates, graph exported.

### 2. Full Run

```bash
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline.yaml \
  --mem 'product_idea="A simple landing page for a coffee shop"' \
  --save-artifacts --output human
```

### 3. Verify Outputs

**Check Summary**:
```bash
cat out/<run_id>/SUMMARY.md
```

**Check ZIP**:
```bash
ls -lh out/<run_id>/Package\ ZIP/
```

**Extract & Test**:
```bash
unzip "out/<run_id>/Package ZIP/package.zip" -d out/demo/
python -m http.server -d out/demo 8000
# Open http://localhost:8000 in browser
```

---

## Sanity Checklist

After running, verify:

- ✅ `Code Skeleton/` contains `index.html`
- ✅ `Static Lint/` has non-empty report
- ✅ `Accessibility Audit/` has non-empty report
- ✅ `Documentation/README.md` exists
- ✅ `Package ZIP/package.zip` exists and is not empty
- ✅ ZIP opens without errors
- ✅ HTML loads in browser without console errors

---

## Design Variables

The enhanced pipeline (`pipeline-with-design.yaml`) supports:

- `brand` - Brand name (e.g., "BlueBean")
- `primary_color` - Hex color (e.g., "#0ea5e9")
- `tone` - Design tone (e.g., "minimal", "professional", "playful")
- `font_family` - Font name (e.g., "Inter", "Roboto")

**Example**:
```bash
--mem 'product_idea="Coffee shop" brand="BlueBean" primary_color="#0ea5e9" tone="minimal" font_family="Inter"'
```

These variables are available in Jinja2 templates via `{{ variable_name }}`.

---

## Quality Gates

### Fail-Fast on Quality Issues

Edit `policy.thresholds` in pipeline YAML:

```yaml
policy:
  thresholds:
    validation: 0.75  # Stricter - fail if lint/a11y score too low
```

### Stricter Council Weights

```yaml
advisors:
  council:
    - name: CodeReviewAdvisor
      weight: 2.0  # Higher weight = stricter quality gate
```

---

## Advanced Features

### Parallel Execution

```bash
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline.yaml \
  --parallel --max-workers 4 \
  --mem 'product_idea="Demo"' \
  --save-artifacts
```

**Benefit**: Faster execution when stages are independent.

### Resume with SQLite

```bash
# First run
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline.yaml \
  --checkpoint-store sqlite \
  --mem 'product_idea="Demo"' \
  --save-artifacts

# Resume if interrupted
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline.yaml \
  --checkpoint-store sqlite \
  --resume-run-id <run_id> \
  --save-artifacts
```

### Artifact Diff

Run twice with slight changes to see diffs:

```bash
# Run 1
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline.yaml \
  --mem 'product_idea="Coffee shop"' --save-artifacts

# Run 2 (slight change)
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline.yaml \
  --mem 'product_idea="Coffee shop with menu"' --save-artifacts

# Compare summaries
diff out/<run1>/SUMMARY.md out/<run2>/SUMMARY.md
```

---

## Extending the Pipeline

### Add Screenshot Stage

```yaml
stages:
  - name: Screenshots
    agent: ScreenshotAgent  # Would need to be implemented
    advisor: CodeReviewAdvisor
    input: src/index.html
    output: screenshots/preview.png
    category: validation
```

Then add to ZIP packaging stage `input` list.

### Add Template Switch

```yaml
stages:
  - name: Code Skeleton
    task: |
      Generate HTML/CSS with template: {{ template | default("minimal") }}
      Options: minimal, marketing, serif
```

Use with:
```bash
--mem 'product_idea="Demo" template="marketing"'
```

---

## Troubleshooting

### ZIP is Empty

**Fix**: Check that previous stages produced artifacts. Run with `--output human` to see stage outputs.

### "Agent not found"

**Fix**: Ensure `ZipPackagerAgent` is registered in `src/orchestrator/factory.py`.

### Design Variables Not Applied

**Fix**: Use `pipeline-with-design.yaml` which includes Jinja2 templates in tasks.

### Quality Gates Too Strict

**Fix**: Lower `policy.thresholds.validation` or adjust advisor weights.

---

## Integration Tests

Run automated tests:

```bash
pytest tests/test_idea_to_zip_integration.py -v
```

Tests verify:
- Pipeline runs successfully
- ZIP file is created
- ZIP contains expected files (HTML, README, MANIFEST)
- ZIP is not empty

---

**Last Updated**: 2025-01-12
