"""Test filesystem checkpoint store."""

from pathlib import Path

from src.core.resume import Checkpoint
from src.orchestrator.checkpoint_fs import FileCheckpointStore


def test_checkpoint_save_and_load(tmp_path: Path) -> None:
    """Test saving and loading checkpoints."""

    store = FileCheckpointStore(root=str(tmp_path / "checkpoints"))
    checkpoint = Checkpoint(
        run_id="test_run",
        step_index=0,
        stage="test_stage",
        memory_snapshot={"key": "value"},
    )

    store.save("test_run:0", checkpoint)

    loaded = store.load("test_run:0")
    assert loaded is not None
    assert loaded.run_id == "test_run"
    assert loaded.stage == "test_stage"
    assert loaded.memory_snapshot == {"key": "value"}


def test_checkpoint_load_nonexistent(tmp_path: Path) -> None:
    """Test loading non-existent checkpoint returns None."""

    store = FileCheckpointStore(root=str(tmp_path / "checkpoints"))
    loaded = store.load("nonexistent:0")
    assert loaded is None


def test_checkpoint_key_sanitization(tmp_path: Path) -> None:
    """Test that checkpoint keys are sanitized for filesystem."""

    store = FileCheckpointStore(root=str(tmp_path / "checkpoints"))
    checkpoint = Checkpoint(run_id="test", step_index=0, stage="stage")

    store.save("run:id:with:colons", checkpoint)

    # Should create file with __ instead of :
    assert (tmp_path / "checkpoints" / "run__id__with__colons.json").exists()
