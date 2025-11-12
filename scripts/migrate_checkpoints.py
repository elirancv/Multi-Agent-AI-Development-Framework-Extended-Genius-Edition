"""Migration utility: FS checkpoints → SQLite."""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path
from typing import Tuple

DDL = """
CREATE TABLE IF NOT EXISTS checkpoints (
  run_id      TEXT NOT NULL,
  step_index  INTEGER NOT NULL,
  stage       TEXT NOT NULL,
  created_at  INTEGER NOT NULL,
  memory_json TEXT NOT NULL,
  extra_json  TEXT NOT NULL,
  PRIMARY KEY (run_id, step_index)
);
CREATE INDEX IF NOT EXISTS idx_checkpoints_runid_created ON checkpoints (run_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_checkpoints_stage ON checkpoints (stage);
"""


def parse_fs_key(stem: str) -> Tuple[str, int]:
    """
    Parse filesystem checkpoint key to run_id and step_index.

    Format: "<run_id>__<step_index>"
    """
    parts = stem.split("__", 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid checkpoint key format: {stem}")
    run_id, step_idx = parts
    return run_id, int(step_idx)


def migrate(fs_root: str, sqlite_path: str) -> int:
    """
    Migrate filesystem checkpoints to SQLite database.

    Args:
        fs_root: Root directory containing FS checkpoint files
        sqlite_path: Path to SQLite database file

    Returns:
        Number of checkpoints migrated
    """
    root = Path(fs_root)
    if not root.exists():
        print(f"[WARN] FS root not found: {root}")
        return 0

    conn = sqlite3.connect(sqlite_path)
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.executescript(DDL)

        count = 0
        skipped = 0

        for ck_file in root.glob("*.json"):
            try:
                data = json.loads(ck_file.read_text(encoding="utf-8"))
                run_id, step_index = parse_fs_key(ck_file.stem)

                # Extract fields with fallbacks
                stage = data.get("stage") or data.get("metadata", {}).get("stage", "unknown")

                # Handle timestamp (can be seconds or milliseconds)
                timestamp = (
                    data.get("timestamp")
                    or data.get("created_at")
                    or data.get("metadata", {}).get("created_at")
                    or 0
                )
                if timestamp < 10000000000:  # Likely seconds, convert to ms
                    created_at = int(timestamp * 1000)
                else:  # Already milliseconds
                    created_at = int(timestamp)

                memory_json = json.dumps(
                    data.get("memory_snapshot") or data.get("memory") or {}, ensure_ascii=False
                )
                extra_json = json.dumps(
                    data.get("extra") or data.get("metadata") or {}, ensure_ascii=False
                )

                conn.execute(
                    """
                    INSERT INTO checkpoints(run_id, step_index, stage, created_at, memory_json, extra_json)
                    VALUES(?,?,?,?,?,?)
                    ON CONFLICT(run_id, step_index) DO UPDATE SET
                        stage=excluded.stage,
                        created_at=excluded.created_at,
                        memory_json=excluded.memory_json,
                        extra_json=excluded.extra_json
                """,
                    (run_id, step_index, stage, created_at, memory_json, extra_json),
                )
                count += 1
            except Exception as e:
                print(f"[SKIP] {ck_file.name}: {e}", file=sys.stderr)
                skipped += 1

        conn.commit()
        print(f"[OK] Migrated {count} checkpoints → {sqlite_path}")
        if skipped > 0:
            print(f"[WARN] Skipped {skipped} checkpoints due to errors")
        return count
    finally:
        conn.close()


def main() -> int:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Migrate FS checkpoints to SQLite")
    parser.add_argument(
        "fs_root", nargs="?", default="out/checkpoints", help="FS checkpoint root directory"
    )
    parser.add_argument(
        "sqlite_path", nargs="?", default="out/checkpoints.db", help="SQLite database path"
    )

    args = parser.parse_args()

    print(f"Migrating checkpoints from {args.fs_root} to {args.sqlite_path}...")
    count = migrate(args.fs_root, args.sqlite_path)
    return 0 if count >= 0 else 1


if __name__ == "__main__":
    sys.exit(main())
