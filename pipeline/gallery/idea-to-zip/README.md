# Pipeline: From Idea to ZIP

**Complete end-to-end workflow** that takes a product idea and produces a distributable ZIP package.

## What It Does

1. **Product Definition** - Creates PRD from idea
2. **Code Skeleton** - Generates HTML/CSS files
3. **Static Lint** - Validates code quality
4. **Accessibility Audit** - Checks A11y compliance
5. **Documentation** - Generates README
6. **Package ZIP** - Creates distributable ZIP with all artifacts

## Quick Start

```bash
# Basic run
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline.yaml \
  --mem 'product_idea="A simple landing page for a coffee shop"' \
  --save-artifacts --output human

# Marketing-first (with hero, features, testimonials)
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline-marketing-first.yaml \
  --mem 'product_idea="Coffee shop" brand="BlueBean" primary_color="#0ea5e9" tone="minimal"' \
  --save-artifacts --output human

# Production demo (strict quality gates + screenshot)
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline-production-demo.yaml \
  --mem 'product_idea="Coffee shop" brand="BlueBean" primary_color="#0ea5e9" tone="minimal"' \
  --save-artifacts --output human

# With parallel execution
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline.yaml \
  --mem 'product_idea="A simple landing page for a coffee shop"' \
  --save-artifacts --output human --parallel --max-workers 4

# Dry-run first (validation + graph)
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline.yaml \
  --dry-run --export-graph out/idea-to-zip.dot
```

## Output Structure

After running, you'll find:

```
out/<run_id>/
├── Product Definition/
│   └── product_definition.md
├── Code Skeleton/
│   └── index.html
├── Static Lint/
│   └── lint_report.md
├── Accessibility Audit/
│   └── a11y_report.md
├── Documentation/
│   └── README.md
├── Package ZIP/
│   ├── package.zip          # ← Your distributable package!
│   └── MANIFEST.txt
└── SUMMARY.md               # Full run report
```

## The ZIP Package

The final ZIP contains:
- `index.html` - Generated HTML
- `README.md` - Project documentation
- `lint_report.md` - Code quality report
- `a11y_report.md` - Accessibility audit
- `MANIFEST.txt` - Package contents manifest

## Extract and Use

```bash
# Extract the ZIP
unzip out/<run_id>/Package\ ZIP/package.zip -d my-project/

# Or use Python
python -c "import zipfile; zipfile.ZipFile('out/<run_id>/Package ZIP/package.zip').extractall('my-project/')"
```

## Customization

### Change Input Idea

```bash
--mem 'product_idea="Your custom idea here"'
```

### Adjust Policy Thresholds

Edit `pipeline.yaml`:
```yaml
policy:
  thresholds:
    overall: 0.70  # Lower for faster iteration
```

### Add More Stages

Add stages to `pipeline.yaml`:
```yaml
stages:
  - name: Your Stage
    agent: YourAgent
    advisor: YourAdvisor
    # ...
```

## Troubleshooting

### "Agent not found"
**Fix**: Ensure `ZipPackagerAgent` is registered in `src/orchestrator/factory.py`

### ZIP is empty
**Fix**: Check that previous stages produced artifacts. Run with `--output human` to see stage outputs.

### "File not found during packaging"
**Fix**: Artifacts from previous stages must exist. Check `out/<run_id>/` for stage outputs.

---

**Last Updated**: 2025-01-12
