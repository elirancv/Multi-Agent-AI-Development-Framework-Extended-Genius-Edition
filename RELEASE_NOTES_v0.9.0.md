# Release Notes: v0.9.0 – Production-ready Orchestrator

**Release Date:** 2025-01-12  
**Status:** Stable

## Highlights

### 🎯 Orchestrator Advanced Features

- **DAG Parallel Execution**: Wave-based parallel execution with dependency resolution
- **Policy System**: Comprehensive policy configuration (thresholds, timeouts, retries, council with weights)
- **Hooks**: Post-step hooks including refine-on-fail for automatic prompt refinement
- **Cache & Checkpoint**: Filesystem-based checkpoint store with resume capability
- **Event Logging**: JSONL event log for observability and debugging

### 🛠️ Developer Experience & Reliability

- **Full CLI**: Complete command-line interface with 15+ flags
- **Jinja2 Templating**: Dynamic task rendering with template variables
- **JSONL Event Log**: Structured event logging for analysis
- **Markdown Reports**: Human-readable reports with artifact diffs and top suggestions
- **Artifact Sink**: Automatic artifact persistence with manifest generation

### ✅ Quality Gates

- **Pre-commit Hooks**: Ruff linting + mypy type checking
- **CI Matrix**: Multi-version testing (Python 3.8, 3.11, 3.13)
- **Smoke Suite**: Comprehensive smoke tests with JUnit XML + Markdown summaries
- **Test Coverage**: 87/87 tests passing, >80% code coverage

### 🔧 Operations & Observability

- **Structured JSON Logging**: CI-aware JSON logging for machine consumption
- **ENV Configuration**: 12-factor app pattern with environment variables
- **OpenTelemetry**: Distributed tracing integration
- **Budget Enforcement**: Runtime, stage, and artifact size limits

## New CLI Commands

### Core Commands
- `--version` - Print version and exit
- `--dry-run` - Validate pipeline without execution
- `--pipeline <file>` - Pipeline YAML file (required)

### Execution Modes
- `--parallel` - Enable parallel (wave-based) execution
- `--max-workers <N>` - Maximum parallel workers (default: 4)
- `--save-artifacts` - Persist artifacts to filesystem
- `--output {human|json}` - Output format (default: human)

### Control & Behavior
- `--fail-fast` - Stop on first rejection
- `--refine-on-fail` - Auto-run PromptRefiner on failed steps
- `--no-cache` - Disable agent output caching
- `--resume-run-id <id>` - Resume from checkpoint

### Observability
- `--export-graph <out.dot>` - Export pipeline graph (requires graphviz)
- `--otel-endpoint <url>` - OpenTelemetry OTLP endpoint
- `--otel-service <name>` - Service name for tracing
- `--top-suggestions` - Include top 5 suggestions in report

## Breaking Changes

**None** - This release is fully backward compatible with existing pipelines.

## Migration Guide

No migration required. Existing pipelines will work as-is. New features are opt-in via CLI flags or policy configuration.

## Configuration

### Environment Variables

See `docs/CONFIG.md` for full configuration options:

```bash
# Timeouts
export ORCH_TIMEOUT=120.0
export ORCH_MAX_RETRIES=5

# Paths
export ORCH_EVENTLOG=out/run_events.jsonl
export ORCH_CHECKPOINT_ROOT=out/checkpoints

# OpenTelemetry
export ORCH_OTEL_ENDPOINT=http://localhost:4318/v1/traces
export ORCH_OTEL_SERVICE=multi-agent

# Logging
export ORCH_JSON_LOG=true  # Enable JSON logging
export CI=true  # Auto-enables JSON logging
```

## Installation

```bash
# From source
git clone https://github.com/your-org/AgentsSystemV2.git
cd AgentsSystemV2
pip install -r requirements.txt

# Or install as package
pip install -e .

# Verify installation
python cli.py --version
# or
multiagent --version
```

## Quick Start

```bash
# Validate pipeline
python cli.py --pipeline pipeline/production.yaml --dry-run

# Run pipeline
python cli.py --pipeline pipeline/production.yaml

# Run with parallel execution
python cli.py --pipeline pipeline/production.yaml --parallel --max-workers 8

# Resume from checkpoint
python cli.py --pipeline pipeline/production.yaml --resume-run-id <run_id>
```

## Testing

```bash
# Run unit tests
pytest tests/ -v

# Run smoke tests
python scripts/smoke_test.py --skip-slow

# Run full smoke suite
python scripts/smoke_test.py --verbose
```

## Documentation

- **[Quickstart](docs/QUICKSTART.md)** - Get started in 5 minutes
- **[CLI Usage](docs/CLI_USAGE.md)** - Complete CLI reference
- **[Configuration](docs/CONFIG.md)** - Environment variables and config
- **[Index](docs/INDEX.md)** - Full documentation index

## Contributors

Thank you to all contributors who made this release possible!

## What's Next

See [v1.0 Roadmap](https://github.com/your-org/AgentsSystemV2/issues?q=is%3Aopen+label%3Av1.0) for planned features:

- API documentation generator
- Pipelines gallery with examples
- Council presets per category
- Artifact retention policies
- Performance optimizations

## Support

- **Issues**: [GitHub Issues](https://github.com/your-org/AgentsSystemV2/issues)
- **Security**: See [SECURITY.md](SECURITY.md)
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Full Changelog**: [CHANGELOG.md](CHANGELOG.md)

