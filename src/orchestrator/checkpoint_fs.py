"""Filesystem-based checkpoint store."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from src.core.resume import Checkpoint


class FileCheckpointStore:
    """Filesystem-based checkpoint store for persistence across runs."""

    def __init__(self, root: str = "out/checkpoints") -> None:
        """
        Initialize filesystem checkpoint store.

        Args:
            root: Root directory for checkpoint files
        """
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, key: str) -> Path:
        """
        Convert checkpoint key to filesystem-safe path.

        Args:
            key: Checkpoint key (e.g., "run_id:stage")

        Returns:
            Path to checkpoint file
        """
        # Make key FS-safe: replace : with __
        safe = key.replace(":", "__")
        return self.root / f"{safe}.json"

    def save(self, key: str, checkpoint: Checkpoint) -> None:
        """
        Save checkpoint to filesystem.

        Args:
            key: Checkpoint key
            checkpoint: Checkpoint object
        """
        p = self._path(key)
        p.write_text(checkpoint.to_json(), encoding="utf-8")

    def load(self, key: str) -> Optional[Checkpoint]:
        """
        Load checkpoint from filesystem.

        Args:
            key: Checkpoint key

        Returns:
            Checkpoint object or None if not found
        """
        p = self._path(key)
        if not p.exists():
            return None
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            return Checkpoint(**data)
        except Exception:
            return None

    def find_last_key(self, run_id: str) -> Optional[str]:
        """
        Find the latest checkpoint key for a given run_id.

        Args:
            run_id: Run ID to search for

        Returns:
            Latest checkpoint key or None if not found
        """
        # Search for checkpoints matching run_id prefix
        # Keys are stored as run_id__step_index.json
        prefix = run_id.replace(":", "__")
        matches = list(self.root.glob(f"{prefix}__*.json"))
        if not matches:
            return None

        # Extract step_index from each match and find the maximum
        # Format: run_id__step_index.json -> extract step_index
        def extract_step_index(path: Path) -> int:
            stem = path.stem  # e.g., "test_run_123__1"
            parts = stem.split("__")
            if len(parts) >= 2:
                try:
                    return int(parts[-1])
                except ValueError:
                    return -1
            return -1

        # Sort by step_index (more reliable than mtime)
        latest = max(matches, key=extract_step_index)
        # Convert back to key format: run_id:step_index
        key = latest.stem.replace("__", ":")
        return key

    def find_key(self, run_id: str, step_index: int) -> Optional[str]:
        """
        Find a specific checkpoint key for a given run_id and step_index.

        Args:
            run_id: Run ID to search for
            step_index: Step index to find

        Returns:
            Checkpoint key if found, None otherwise
        """
        key = f"{run_id}:{step_index}"
        p = self._path(key)
        return key if p.exists() else None

