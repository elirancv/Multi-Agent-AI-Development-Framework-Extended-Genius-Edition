# Static Site Generator Pipeline

Generate a static website from markdown files.

## Use Case

Convert markdown documentation into a static HTML website suitable for GitHub Pages or similar hosting.

## Pipeline Overview

1. **Requirements** - Define requirements for markdown → HTML conversion
2. **Architecture** - Design generator architecture
3. **Documentation** - Create usage documentation

## Run This

```bash
python cli.py --pipeline pipeline/gallery/static-site/pipeline.yaml --preset mvp-fast
```

## Expected Output

- `docs/requirements.md` - Requirements specification
- `src/static_site_generator.py` - Generator implementation
- `docs/README.md` - Usage documentation

## Visualizations

- **Pipeline Graph**: `pipeline.dot` / `pipeline.png`
- **Execution Report**: `sample_report.md`

## Status

🟡 **Planned for v1.1.0**

This is a reference pipeline. Full implementation coming in v1.1.0.

