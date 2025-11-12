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

### 1. Static Site Generator
Generate a static website from markdown files.

**Run this**:
```bash
python cli.py --pipeline pipeline/gallery/static-site/pipeline.yaml --preset mvp-fast
```

[View details](static-site/README.md)

### 2. REST API Service
Create a FastAPI service with OpenAPI documentation.

**Run this**:
```bash
python cli.py --pipeline pipeline/gallery/api-service/pipeline.yaml --preset production
```

[View details](api-service/README.md)

### 3. ETL Pipeline
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

