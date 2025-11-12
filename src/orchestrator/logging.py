"""Structured logging configuration for orchestrator."""

from __future__ import annotations

import json
import logging
import os
import sys
import time
from typing import Any, Dict


# Auto-detect JSON logging: explicit OR in CI
USE_JSON = os.getenv("ORCH_JSON_LOG", "auto") == "true" or os.getenv("CI") == "true"


class JsonFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        payload: Dict[str, Any] = {
            "ts": time.time(),
            "level": record.levelname,
            "msg": record.getMessage(),
            "logger": record.name,
        }
        
        # Add extra fields if present
        if hasattr(record, "extra") and record.extra:
            payload.update(record.extra)
        
        # Add run_id, stage, agent if present in record
        for attr in ["run_id", "stage", "agent", "ts"]:
            if hasattr(record, attr):
                payload[attr] = getattr(record, attr)
        
        return json.dumps(payload, ensure_ascii=False)


def setup_logging() -> None:
    """Setup logging with JSON or standard formatter based on environment."""
    handler = logging.StreamHandler(sys.stdout)
    
    if USE_JSON:
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(logging.INFO)

