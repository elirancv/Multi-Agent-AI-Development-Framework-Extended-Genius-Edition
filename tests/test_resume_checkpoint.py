"""Test resume from checkpoint."""

from pathlib import Path

from src.core.resume import Checkpoint
from src.orchestrator.checkpoint_fs import FileCheckpointStore


def test_find_last_key(tmp_path: Path) -> None:
    """Test finding last checkpoint key for a run_id."""
    store = FileCheckpointStore(root=str(tmp_path / "checkpoints"))

    # Create multiple checkpoints for same run_id
    run_id = "test_run_123"
    checkpoint1 = Checkpoint(
        run_id=run_id, step_index=0, stage="stage1", memory_snapshot={"key1": "value1"}
    )
    checkpoint2 = Checkpoint(
        run_id=run_id, step_index=1, stage="stage2", memory_snapshot={"key2": "value2"}
    )

    store.save(f"{run_id}:0", checkpoint1)
    store.save(f"{run_id}:1", checkpoint2)

    # Find latest
    last_key = store.find_last_key(run_id)
    assert last_key is not None
    assert "1" in last_key  # Should be the later checkpoint

    # Load and verify
    loaded = store.load(last_key)
    assert loaded is not None
    assert loaded.stage == "stage2"


def test_find_last_key_nonexistent(tmp_path: Path) -> None:
    """Test finding last key for non-existent run_id."""
    store = FileCheckpointStore(root=str(tmp_path / "checkpoints"))
    last_key = store.find_last_key("nonexistent")
    assert last_key is None

