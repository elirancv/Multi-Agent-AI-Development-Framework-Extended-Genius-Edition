# Pipelines Gallery

Reference pipelines showcasing the Multi-Agent AI Development Framework capabilities.

## Quick Start

Each pipeline includes:
- **pipeline.yaml** - Complete working pipeline
- **README.md** - Documentation and usage
- **pipeline.dot** - Graph visualization (DOT)
- **pipeline.png** - Rendered graph
- **sample_report.md** - Sample execution report

## Available Pipelines

### 1. Idea-to-ZIP (Featured)
Complete end-to-end workflow from product idea to distributable ZIP package.

**Run this**:
```bash
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline.yaml \
  --mem 'product_idea="A coffee shop landing page"' \
  --save-artifacts --output human
```

**With design variables**:
```bash
python cli.py --pipeline pipeline/gallery/idea-to-zip/pipeline-with-design.yaml \
  --mem 'product_idea="Coffee shop" brand="BlueBean" primary_color="#0ea5e9" tone="minimal"' \
  --save-artifacts --output human
```

[View details](idea-to-zip/README.md) | [Full Guide](../../docs/IDEA_TO_ZIP_GUIDE.md)

### 2. Static Site Generator
Generate a static website from markdown files.

**Run this**:
```bash
python cli.py --pipeline pipeline/gallery/static-site/pipeline.yaml --preset mvp-fast
```

[View details](static-site/README.md)

### 3. REST API Service
Create a FastAPI service with OpenAPI documentation.

**Run this**:
```bash
python cli.py --pipeline pipeline/gallery/api-service/pipeline.yaml --preset production
```

[View details](api-service/README.md)

### 4. ETL Pipeline
Build an ETL pipeline for data processing.

**Run this**:
```bash
python cli.py --pipeline pipeline/gallery/etl-pipeline/pipeline.yaml --preset mvp-fast
```

[View details](etl-pipeline/README.md)

## Status

**Current**: 🟡 **Planned for v1.1.0**

See `.github/ISSUE_TEMPLATE/v1.1-pipelines-gallery.md` for full specification.

## Contributing

Want to add a pipeline to the gallery? See `docs/PLUGIN_TEMPLATE.md` for guidelines.
