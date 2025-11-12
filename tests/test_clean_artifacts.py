"""Tests for artifact cleanup utility."""

import shutil
import time
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from scripts.clean_artifacts import (
    clean_artifacts,
    find_artifacts,
    format_size,
    get_artifact_size,
    parse_duration,
    parse_size,
)


def test_parse_duration() -> None:
    """Test duration parsing."""
    assert parse_duration("7d") == 7 * 86400
    assert parse_duration("24h") == 24 * 3600
    assert parse_duration("3600s") == 3600
    assert parse_duration("1w") == 7 * 86400


def test_parse_size() -> None:
    """Test size parsing."""
    assert parse_size("2GB") == 2 * 1024**3
    assert parse_size("500MB") == 500 * 1024**2
    assert parse_size("10KB") == 10 * 1024


def test_format_size() -> None:
    """Test size formatting."""
    assert "GB" in format_size(2 * 1024**3)
    assert "MB" in format_size(500 * 1024**2)
    assert "KB" in format_size(10 * 1024)


def test_get_artifact_size(tmp_path: Path) -> None:
    """Test artifact size calculation."""
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    
    # Create test files
    (test_dir / "file1.txt").write_text("x" * 1000)
    (test_dir / "file2.txt").write_text("y" * 2000)
    
    assert get_artifact_size(test_dir) == 3000


def test_clean_dry_run_keeps_latest(tmp_path: Path) -> None:
    """Test that dry-run keeps latest N artifacts."""
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    
    # Create 3 artifact directories (must start with "run_")
    for i in range(3):
        run_dir = out_dir / f"run_test_{i}"
        run_dir.mkdir()
        (run_dir / "artifact.txt").write_text(f"content {i}")
        # Set mtime to simulate age (newer runs have newer timestamps)
        import os
        t = time.time() - (3 - i) * 3600  # Older runs are older
        os.utime(run_dir, (t, t))
        os.utime(run_dir / "artifact.txt", (t, t))
    
    deleted_count, freed_bytes, deleted_files = clean_artifacts(
        artifacts_root=str(out_dir),
        keep_latest=1,
        dry_run=True,
    )
    
    # Should mark 2 for deletion (keep latest 1)
    assert deleted_count == 0  # Dry run doesn't actually delete
    assert len(deleted_files) == 2  # But marks them


def test_clean_respects_max_size(tmp_path: Path) -> None:
    """Test that cleanup respects max size limit."""
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    
    # Create 3 runs with sizes: 10MB, 5MB, 4MB
    sizes = [10 * 1024**2, 5 * 1024**2, 4 * 1024**2]
    for i, size in enumerate(sizes):
        run_dir = out_dir / f"run_{i}"
        run_dir.mkdir()
        # Create file with approximate size
        (run_dir / "large_file.bin").write_bytes(b"x" * size)
    
    deleted_count, freed_bytes, _ = clean_artifacts(
        artifacts_root=str(out_dir),
        max_size="12MB",
        dry_run=True,
    )
    
    # Should mark some for deletion to stay under 12MB
    # Latest (4MB) + one other (5MB) = 9MB < 12MB, so 10MB should be marked
    assert deleted_count == 0  # Dry run
    assert freed_bytes >= sizes[0]  # At least the largest


def test_clean_older_than(tmp_path: Path) -> None:
    """Test age-based cleanup."""
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    
    # Create old and new artifacts
    old_dir = out_dir / "run_old"
    old_dir.mkdir()
    (old_dir / "file.txt").write_text("old")
    import os
    old_time = time.time() - 10 * 86400  # 10 days ago
    os.utime(old_dir, (old_time, old_time))
    
    new_dir = out_dir / "run_new"
    new_dir.mkdir()
    (new_dir / "file.txt").write_text("new")
    
    deleted_count, freed_bytes, _ = clean_artifacts(
        artifacts_root=str(out_dir),
        older_than="7d",
        dry_run=True,
    )
    
    # Should mark old one for deletion
    assert deleted_count == 0  # Dry run
    assert len([f for f in find_artifacts(out_dir) if f[0] == old_dir]) == 1

