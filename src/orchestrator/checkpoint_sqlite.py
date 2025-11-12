"""SQLite-based checkpoint store for atomic operations and fast queries."""

from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path
from typing import List, Optional, Tuple

from src.core.resume import Checkpoint


class SQLiteCheckpointStore:
    """SQLite-based checkpoint store with atomic operations and fast queries."""

    def __init__(self, db_path: str = "out/checkpoints.db") -> None:
        """
        Initialize SQLite checkpoint store.

        Args:
            db_path: Path to SQLite database file
        """
        self.path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _init(self) -> None:
        """Initialize database schema."""
        with sqlite3.connect(self.path) as cx:
            cx.execute("PRAGMA journal_mode=WAL;")
            cx.executescript("""
                CREATE TABLE IF NOT EXISTS checkpoints (
                    run_id        TEXT NOT NULL,
                    step_index    INTEGER NOT NULL,
                    stage         TEXT NOT NULL,
                    created_at    INTEGER NOT NULL,
                    memory_json   TEXT NOT NULL,
                    extra_json    TEXT NOT NULL,
                    PRIMARY KEY (run_id, step_index)
                );

                CREATE INDEX IF NOT EXISTS idx_checkpoints_runid_created
                    ON checkpoints (run_id, created_at DESC);

                CREATE INDEX IF NOT EXISTS idx_checkpoints_stage
                    ON checkpoints (stage);
            """)
            cx.commit()

    def save(self, key: str, checkpoint: Checkpoint) -> None:
        """
        Save checkpoint atomically.

        Args:
            key: Checkpoint key (e.g., "run_id:step_index")
            checkpoint: Checkpoint object
        """
        run_id, step_index = self._split(key)
        # Use checkpoint timestamp if available, otherwise current time
        created_at_ms = int((checkpoint.timestamp or time.time()) * 1000)

        payload = (
            run_id,
            step_index,
            checkpoint.stage,
            created_at_ms,
            json.dumps(checkpoint.memory_snapshot, ensure_ascii=False),
            json.dumps(checkpoint.extra or {}, ensure_ascii=False),
        )

        with sqlite3.connect(self.path) as cx:
            cx.execute(
                """
                INSERT INTO checkpoints (run_id, step_index, stage, created_at, memory_json, extra_json)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(run_id, step_index) DO UPDATE SET
                    stage=excluded.stage,
                    created_at=excluded.created_at,
                    memory_json=excluded.memory_json,
                    extra_json=excluded.extra_json
            """,
                payload,
            )
            cx.commit()

    def load(self, key: str) -> Optional[Checkpoint]:
        """
        Load checkpoint by key.

        Args:
            key: Checkpoint key

        Returns:
            Checkpoint object or None if not found
        """
        run_id, step_index = self._split(key)

        with sqlite3.connect(self.path) as cx:
            row = cx.execute(
                """
                SELECT stage, created_at, memory_json, extra_json
                FROM checkpoints WHERE run_id=? AND step_index=?
            """,
                (run_id, step_index),
            ).fetchone()

        if not row:
            return None

        stage, created_at, mem_json, extra_json = row

        return Checkpoint(
            run_id=run_id,
            step_index=step_index,
            stage=stage,
            memory_snapshot=json.loads(mem_json),
            timestamp=created_at / 1000.0,  # Convert ms to seconds
            extra=json.loads(extra_json or "{}"),
        )

    def find_last_key(self, run_id: str) -> Optional[str]:
        """
        Find the latest checkpoint key for a given run_id.

        Args:
            run_id: Run ID to search for

        Returns:
            Latest checkpoint key or None if not found
        """
        with sqlite3.connect(self.path) as cx:
            row = cx.execute(
                """
                SELECT step_index FROM checkpoints
                WHERE run_id=? ORDER BY step_index DESC LIMIT 1
            """,
                (run_id,),
            ).fetchone()

        return f"{run_id}:{row[0]}" if row else None

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
        with sqlite3.connect(self.path) as cx:
            exists = cx.execute(
                "SELECT 1 FROM checkpoints WHERE run_id=? AND step_index=?", (run_id, step_index)
            ).fetchone()
            return key if exists else None

    def find_by_date_range(self, run_id: str, start_ms: int, end_ms: int) -> List[str]:
        """
        Find checkpoint keys within a date range (milliseconds).

        Args:
            run_id: Run ID to search for
            start_ms: Start timestamp in milliseconds
            end_ms: End timestamp in milliseconds

        Returns:
            List of checkpoint keys
        """
        with sqlite3.connect(self.path) as cx:
            rows = cx.execute(
                """
                SELECT step_index FROM checkpoints
                WHERE run_id=? AND created_at BETWEEN ? AND ?
                ORDER BY step_index ASC
            """,
                (run_id, start_ms, end_ms),
            ).fetchall()

        return [f"{run_id}:{r[0]}" for r in rows]

    @staticmethod
    def _split(key: str) -> Tuple[str, int]:
        """Split checkpoint key into run_id and step_index."""
        run_id, idx = key.split(":", 1)
        return run_id, int(idx)
