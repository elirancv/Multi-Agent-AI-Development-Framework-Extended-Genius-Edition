# REST API Service Pipeline

Create a FastAPI service with OpenAPI documentation.

## Use Case

Generate a production-ready REST API service with automatic OpenAPI documentation, suitable for microservices or API-first applications.

## Pipeline Overview

1. **Requirements** - Define API requirements and endpoints
2. **API Design** - Design REST API schema and OpenAPI spec
3. **Implementation** - Implement FastAPI service
4. **Documentation** - Create API documentation

## Run This

```bash
python cli.py --pipeline pipeline/gallery/api-service/pipeline.yaml --preset production
```

## Expected Output

- `docs/requirements.md` - API requirements
- `src/api_schema.py` - OpenAPI schema
- `src/api_service.py` - FastAPI implementation
- `docs/API.md` - API documentation

## Visualizations

- **Pipeline Graph**: `pipeline.dot` / `pipeline.png`
- **Execution Report**: `sample_report.md`

## Status

🟡 **Planned for v1.1.0**

This is a reference pipeline. Full implementation coming in v1.1.0.
