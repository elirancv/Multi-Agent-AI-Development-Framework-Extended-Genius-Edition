# Copyright (c) 2025 Multi-Agent AI Development Framework Contributors
# Licensed under the MIT License

"""Checkpoint and resume functionality for pipeline execution."""

from __future__ import annotations

from typing import Any, Dict, Optional
from dataclasses import dataclass, field
import json
import time


@dataclass
class Checkpoint:
    """Serializable snapshot of orchestrator state."""

    run_id: str
    step_index: int
    stage: str
    memory_snapshot: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps(
            {
                "run_id": self.run_id,
                "step_index": self.step_index,
                "stage": self.stage,
                "memory_snapshot": self.memory_snapshot,
                "timestamp": self.timestamp,
                "extra": self.extra,
            }
        )


class CheckpointStore:
    """Interface for persisting/retrieving checkpoints. Replace with DB/S3 as needed."""

    def __init__(self) -> None:
        self._store: Dict[str, str] = {}

    def save(self, key: str, checkpoint: Checkpoint) -> None:
        self._store[key] = checkpoint.to_json()

    def load(self, key: str) -> Optional[Checkpoint]:
        raw = self._store.get(key)
        if not raw:
            return None
        data = json.loads(raw)
        return Checkpoint(**data)

