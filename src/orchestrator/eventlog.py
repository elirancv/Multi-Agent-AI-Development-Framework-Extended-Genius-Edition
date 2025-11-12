"""JSONL event log for pipeline tracing."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict


class JsonlEventLog:
    """Event logger that writes JSONL format for easy parsing."""

    def __init__(self, path: str = "out/run_events.jsonl") -> None:
        """
        Initialize event log.

        Args:
            path: Path to JSONL file (will create parent directories)
        """
        self._p = Path(path)
        self._p.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, event: str, **data: Any) -> None:
        """
        Emit an event to the log.

        Args:
            event: Event name (e.g., "step_start", "step_result")
            **data: Additional event data
        """
        rec: Dict[str, Any] = {
            "ts": time.time(),
            "event": event,
        }
        rec.update(data)
        with self._p.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

