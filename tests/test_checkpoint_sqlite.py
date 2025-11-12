"""Tests for SQLite checkpoint store."""

import time
from pathlib import Path

from src.core.resume import Checkpoint
from src.orchestrator.checkpoint_sqlite import SQLiteCheckpointStore


def test_sqlite_checkpoint_save_load(tmp_path: Path) -> None:
    """Test saving and loading checkpoint."""
    db = tmp_path / "cp.db"
    store = SQLiteCheckpointStore(str(db))

    ck = Checkpoint(
        run_id="r1",
        step_index=2,
        stage="requirements",
        memory_snapshot={"requirements.content": "ok"},
        extra={"duration_ms": 123},
    )

    store.save("r1:2", ck)
    out = store.load("r1:2")

    assert out is not None
    assert out.run_id == "r1"
    assert out.step_index == 2
    assert out.stage == "requirements"
    assert out.memory_snapshot["requirements.content"] == "ok"
    assert out.extra["duration_ms"] == 123


def test_sqlite_find_last_key(tmp_path: Path) -> None:
    """Test finding last checkpoint key."""
    db = tmp_path / "cp.db"
    store = SQLiteCheckpointStore(str(db))

    for i in range(3):
        ck = Checkpoint(
            run_id="runX",
            step_index=i,
            stage=f"s{i}",
            memory_snapshot={"k": i},
            extra={},
        )
        store.save(f"runX:{i}", ck)

    assert store.find_last_key("runX") == "runX:2"
    assert store.find_last_key("nonexistent") is None


def test_sqlite_date_range(tmp_path: Path) -> None:
    """Test finding checkpoints by date range."""
    db = tmp_path / "cp.db"
    store = SQLiteCheckpointStore(str(db))

    now_ms = int(time.time() * 1000)

    # Create checkpoints with different timestamps
    ck0 = Checkpoint("r", 0, "s0", {"a": 1}, {})
    ck0.timestamp = (now_ms - 2000) / 1000.0
    store.save("r:0", ck0)

    ck1 = Checkpoint("r", 1, "s1", {"b": 2}, {})
    ck1.timestamp = (now_ms - 1000) / 1000.0
    store.save("r:1", ck1)

    ck2 = Checkpoint("r", 2, "s2", {"c": 3}, {})
    ck2.timestamp = now_ms / 1000.0
    store.save("r:2", ck2)

    keys = store.find_by_date_range("r", now_ms - 1500, now_ms + 10)
    assert keys == ["r:1", "r:2"]


def test_sqlite_find_key(tmp_path: Path) -> None:
    """Test finding specific checkpoint key."""
    db = tmp_path / "cp.db"
    store = SQLiteCheckpointStore(str(db))

    ck = Checkpoint("r1", 5, "stage5", {"data": "test"}, {})
    store.save("r1:5", ck)

    assert store.find_key("r1", 5) == "r1:5"
    assert store.find_key("r1", 10) is None
    assert store.find_key("r2", 5) is None


def test_sqlite_atomic_save(tmp_path: Path) -> None:
    """Test atomic save operations."""
    db = tmp_path / "cp.db"
    store = SQLiteCheckpointStore(str(db))

    # Save same key twice - should update, not duplicate
    ck1 = Checkpoint("r1", 1, "stage1", {"v": 1}, {})
    ck2 = Checkpoint("r1", 1, "stage1_updated", {"v": 2}, {})

    store.save("r1:1", ck1)
    store.save("r1:1", ck2)

    loaded = store.load("r1:1")
    assert loaded is not None
    assert loaded.memory_snapshot["v"] == 2
