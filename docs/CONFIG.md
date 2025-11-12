# Configuration

This document describes how to configure the multi-agent system via environment variables (12-factor app pattern).

## Environment Variables

### Timeouts and Retries

- `ORCH_TIMEOUT` - Default timeout for agent execution in seconds (default: `60.0`)
- `ORCH_MAX_RETRIES` - Maximum number of retries for failed steps (default: `3`)

Example:
```bash
export ORCH_TIMEOUT=120.0
export ORCH_MAX_RETRIES=5
```

### Paths

- `ORCH_EVENTLOG` - Path to event log file (default: `out/run_events.jsonl`)
- `ORCH_CHECKPOINT_ROOT` - Root directory for checkpoints (default: `out/checkpoints`)

Example:
```bash
export ORCH_EVENTLOG=/var/log/orchestrator/events.jsonl
export ORCH_CHECKPOINT_ROOT=/var/checkpoints
```

### OpenTelemetry

- `ORCH_OTEL_ENDPOINT` - OpenTelemetry OTLP HTTP endpoint (default: `http://localhost:4318/v1/traces`)
- `ORCH_OTEL_SERVICE` - Service name for OpenTelemetry (default: `multi-agent`)

Example:
```bash
export ORCH_OTEL_ENDPOINT=http://jaeger:4318/v1/traces
export ORCH_OTEL_SERVICE=my-pipeline
```

### Cache

- `ORCH_USE_CACHE` - Enable/disable agent output caching (default: `true`)

Example:
```bash
export ORCH_USE_CACHE=false  # Disable caching
```

### Logging

- `ORCH_JSON_LOG` - Enable JSON structured logging (default: `auto` - enabled in CI)
- `CI` - When set to `true`, automatically enables JSON logging

Example:
```bash
export ORCH_JSON_LOG=true  # Force JSON logging
export CI=true  # Also enables JSON logging
```

## Using .env File

Create a `.env` file in the project root:

```env
# Timeouts
ORCH_TIMEOUT=120.0
ORCH_MAX_RETRIES=5

# Paths
ORCH_EVENTLOG=out/run_events.jsonl
ORCH_CHECKPOINT_ROOT=out/checkpoints

# OpenTelemetry
ORCH_OTEL_ENDPOINT=http://localhost:4318/v1/traces
ORCH_OTEL_SERVICE=multi-agent

# Cache
ORCH_USE_CACHE=true

# Logging
ORCH_JSON_LOG=auto
```

**Note:** The `.env` file is not automatically loaded. Use a tool like `python-dotenv` or load it manually in your scripts.

## Configuration Priority

1. CLI arguments (highest priority)
2. Environment variables
3. Default values (lowest priority)

## Example: Production Setup

```bash
# Production environment
export ORCH_TIMEOUT=300.0
export ORCH_MAX_RETRIES=3
export ORCH_EVENTLOG=/var/log/orchestrator/events.jsonl
export ORCH_CHECKPOINT_ROOT=/var/checkpoints
export ORCH_OTEL_ENDPOINT=http://jaeger:4318/v1/traces
export ORCH_OTEL_SERVICE=production-pipeline
export ORCH_USE_CACHE=true
export CI=true  # Enables JSON logging
```

