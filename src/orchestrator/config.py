"""Configuration via environment variables (12-factor app)."""

from __future__ import annotations

import os
from pathlib import Path

# Timeouts and retries
DEFAULT_TIMEOUT = float(os.getenv("ORCH_TIMEOUT", "60.0"))
DEFAULT_MAX_RETRIES = int(os.getenv("ORCH_MAX_RETRIES", "3"))

# Event log path
EVENTLOG_PATH = os.getenv("ORCH_EVENTLOG", "out/run_events.jsonl")

# Checkpoint path
CHECKPOINT_ROOT = os.getenv("ORCH_CHECKPOINT_ROOT", "out/checkpoints")

# OpenTelemetry
OTEL_ENDPOINT = os.getenv("ORCH_OTEL_ENDPOINT", "http://localhost:4318/v1/traces")
OTEL_SERVICE_NAME = os.getenv("ORCH_OTEL_SERVICE", "multi-agent")

# Cache
USE_CACHE = os.getenv("ORCH_USE_CACHE", "true").lower() == "true"

# Ensure directories exist
Path(EVENTLOG_PATH).parent.mkdir(parents=True, exist_ok=True)
Path(CHECKPOINT_ROOT).mkdir(parents=True, exist_ok=True)

