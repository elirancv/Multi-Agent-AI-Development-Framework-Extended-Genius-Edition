"""Smoke tests for artifact cleanup."""

import time
from pathlib import Path

import pytest

from scripts.clean_artifacts import clean_artifacts, find_artifacts


def _mkfile(p: Path, size_mb: int) -> None:
    """Create a file with specified size in MB."""
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "wb") as f:
        f.write(b"\0" * (size_mb * 1024 * 1024))


def test_clean_keeps_latest(tmp_path: Path) -> None:
    """Test that cleanup keeps latest N artifacts."""
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    
    # Create 3 runs (must start with "run_")
    r1 = out_dir / "run_A" / "SUMMARY.md"
    r2 = out_dir / "run_B" / "SUMMARY.md"
    r3 = out_dir / "run_C" / "SUMMARY.md"
    
    _mkfile(r1, 1)
    time.sleep(0.01)
    _mkfile(r2, 1)
    time.sleep(0.01)
    _mkfile(r3, 1)
    
    # Clean with keep_latest=1
    deleted_count, freed_bytes, deleted_files = clean_artifacts(
        artifacts_root=str(out_dir),
        keep_latest=1,
        dry_run=True,
    )
    
    # Should mark 2 for deletion (keep latest 1)
    assert deleted_count == 0  # Dry run
    assert len(deleted_files) == 2
    
    # Verify run_C is kept (newest)
    deleted_paths = [f["path"] for f in deleted_files]
    assert any("run_A" in p or "run_B" in p for p in deleted_paths)
    assert not any("run_C" in p for p in deleted_paths)


def test_clean_max_size(tmp_path: Path) -> None:
    """Test that cleanup respects max size limit."""
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    
    # Create runs with sizes: 10MB, 5MB, 4MB (must start with "run_")
    r1 = out_dir / "run_1" / "a.bin"
    r2 = out_dir / "run_2" / "a.bin"
    r3 = out_dir / "run_3" / "a.bin"
    
    _mkfile(r1, 10)
    time.sleep(0.01)
    _mkfile(r2, 5)
    time.sleep(0.01)
    _mkfile(r3, 4)
    
    # Clean with max_size=12MB
    deleted_count, freed_bytes, deleted_files = clean_artifacts(
        artifacts_root=str(out_dir),
        max_size="12MB",
        dry_run=True,
    )
    
    # Should mark at least the largest (10MB) for deletion
    assert deleted_count == 0  # Dry run
    assert freed_bytes >= 10 * 1024 * 1024  # At least 10MB


def test_clean_older_than(tmp_path: Path) -> None:
    """Test age-based cleanup."""
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    
    # Create old and new artifacts
    old_run = out_dir / "run_old" / "file.txt"
    new_run = out_dir / "run_new" / "file.txt"
    
    _mkfile(old_run, 1)
    import os
    old_time = time.time() - 10 * 86400  # 10 days ago
    os.utime(old_run.parent, (old_time, old_time))
    
    _mkfile(new_run, 1)
    
    # Clean with older_than=7d
    deleted_count, freed_bytes, deleted_files = clean_artifacts(
        artifacts_root=str(out_dir),
        older_than="7d",
        dry_run=True,
    )
    
    # Should mark old one for deletion
    assert deleted_count == 0  # Dry run
    deleted_paths = [f["path"] for f in deleted_files]
    assert any("run_old" in p for p in deleted_paths)


def test_find_artifacts(tmp_path: Path) -> None:
    """Test artifact discovery."""
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    
    # Create artifact directories (must start with "run_")
    run1 = out_dir / "run_1"
    run2 = out_dir / "run_2"
    run1.mkdir()
    run2.mkdir()
    (run1 / "file.txt").write_text("test")
    (run2 / "file.txt").write_text("test")
    (out_dir / "not_a_run").mkdir()  # Should be ignored
    
    artifacts = find_artifacts(out_dir)
    
    # Should find 2 runs
    assert len(artifacts) == 2
    assert all(p.name.startswith("run") for p, _, _ in artifacts)

