"""Test artifact manifest generation."""

import json
from pathlib import Path

from src.core.memory import SharedMemory
from src.orchestrator.artifact_sink import persist_artifacts


def test_manifest_created(tmp_path: Path) -> None:
    """Test that manifest.json is created."""
    memory = SharedMemory()
    memory.update(
        {
            "stage1.artifacts": [
                {"name": "file1.md", "type": "markdown", "content": "Hello"},
                {"name": "file2.txt", "type": "text", "content": "World"},
            ]
        }
    )

    art_root = tmp_path / "artifacts"
    count = persist_artifacts(memory, str(art_root))

    assert count == 2

    # Check manifest exists (it's written to out_dir/run_id/manifest.json)
    manifest_path = art_root / "unknown" / "manifest.json"
    assert manifest_path.exists()

    # Load and verify manifest
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert len(manifest) == 2
    assert manifest[0]["stage"] == "stage1"
    assert manifest[0]["name"] == "file1.md"
    assert "sha256" in manifest[0]
    assert "bytes" in manifest[0]


def test_manifest_includes_all_fields(tmp_path: Path) -> None:
    """Test that manifest includes all required fields."""
    memory = SharedMemory()
    memory.update(
        {"stage1.artifacts": [{"name": "test.md", "type": "markdown", "content": "Test content"}]}
    )

    art_root = tmp_path / "artifacts"
    persist_artifacts(memory, str(art_root))

    manifest_path = art_root / "unknown" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert len(manifest) == 1
    entry = manifest[0]
    assert "stage" in entry
    assert "name" in entry
    assert "safe_name" in entry
    assert "type" in entry
    assert "bytes" in entry
    assert "sha256" in entry
