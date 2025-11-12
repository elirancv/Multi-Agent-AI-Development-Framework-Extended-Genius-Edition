# Copyright (c) 2025 Multi-Agent AI Development Framework Contributors
# Licensed under the MIT License

"""Shared memory for agent context and data exchange."""

from __future__ import annotations

import copy
from threading import RLock
from typing import Any, Dict, Optional


class SharedMemory:
    """Simple thread-safe shared memory for agents' context/data exchange."""

    def __init__(self) -> None:
        self._lock = RLock()
        self._store: Dict[str, Any] = {}

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        with self._lock:
            return copy.deepcopy(self._store.get(key, default))

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._store[key] = copy.deepcopy(value)

    def update(self, patch: Dict[str, Any]) -> None:
        with self._lock:
            for k, v in patch.items():
                self._store[k] = copy.deepcopy(v)

    def to_dict(self) -> Dict[str, Any]:
        with self._lock:
            return copy.deepcopy(self._store)
