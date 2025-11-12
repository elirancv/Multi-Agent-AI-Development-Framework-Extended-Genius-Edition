"""Artifact cleanup utility with retention policies."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def parse_duration(duration_str: str) -> int:
    """Parse duration string (e.g., '7d', '24h', '3600s') to seconds."""
    duration_str = duration_str.lower().strip()
    multipliers = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    
    for unit, multiplier in multipliers.items():
        if duration_str.endswith(unit):
            return int(float(duration_str[:-len(unit)]) * multiplier)
    
    # Assume seconds if no unit
    return int(duration_str)


def parse_size(size_str: str) -> int:
    """Parse size string (e.g., '2GB', '500MB') to bytes."""
    size_str = size_str.upper().strip()
    multipliers = {"KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}
    
    for unit, multiplier in multipliers.items():
        if size_str.endswith(unit):
            return int(float(size_str[:-len(unit)]) * multiplier)
    
    # Assume bytes if no unit
    return int(size_str)


def format_size(bytes: int) -> str:
    """Format bytes to human-readable string."""
    for unit, multiplier in [("TB", 1024**4), ("GB", 1024**3), ("MB", 1024**2), ("KB", 1024)]:
        if bytes >= multiplier:
            return f"{bytes / multiplier:.2f}{unit}"
    return f"{bytes}B"


def get_artifact_size(path: Path) -> int:
    """Get total size of artifact directory or file."""
    if path.is_file():
        return path.stat().st_size
    elif path.is_dir():
        total = 0
        for item in path.rglob("*"):
            if item.is_file():
                total += item.stat().st_size
        return total
    return 0


def find_artifacts(artifacts_root: Path) -> List[Tuple[Path, datetime, int]]:
    """Find all artifact directories with their creation time and size."""
    artifacts = []
    
    if not artifacts_root.exists():
        return artifacts
    
    for run_dir in artifacts_root.iterdir():
        if run_dir.is_dir() and run_dir.name.startswith("run_"):
            # Try to extract timestamp from directory name or use mtime
            try:
                # Format: run_<run_id>_<timestamp> or run_<run_id>
                parts = run_dir.name.split("_")
                if len(parts) >= 3:
                    timestamp = datetime.fromtimestamp(float(parts[-1]))
                else:
                    timestamp = datetime.fromtimestamp(run_dir.stat().st_mtime)
            except (ValueError, IndexError):
                timestamp = datetime.fromtimestamp(run_dir.stat().st_mtime)
            
            size = get_artifact_size(run_dir)
            artifacts.append((run_dir, timestamp, size))
    
    return sorted(artifacts, key=lambda x: x[1], reverse=True)  # Newest first


def clean_artifacts(
    artifacts_root: str = "out",
    older_than: Optional[str] = None,
    max_size: Optional[str] = None,
    keep_latest: Optional[int] = None,
    dry_run: bool = False,
) -> Tuple[int, int, List[Dict[str, Any]]]:
    """
    Clean artifacts based on retention policies.

    Returns:
        Tuple of (deleted_count, freed_bytes)
    """
    root = Path(artifacts_root)
    artifacts = find_artifacts(root)
    
    if not artifacts:
        if not dry_run:
            print("No artifacts found.")
        return 0, 0, []
    
    to_delete: List[Tuple[Path, int]] = []
    deleted_files: List[Dict[str, Any]] = []
    now = datetime.now()
    max_size_bytes = parse_size(max_size) if max_size else None
    older_than_seconds = parse_duration(older_than) if older_than else None
    
    # Apply retention policies in order: keep-latest → older-than → max-size
    kept_paths: set[Path] = set()
    
    # 1. Keep latest N (always applied first)
    if keep_latest:
        kept_paths = {p for p, _, _ in artifacts[:keep_latest]}
    
    # 2. Filter by age (skip kept paths)
    if older_than_seconds:
        cutoff = now - timedelta(seconds=older_than_seconds)
        for artifact_path, timestamp, size in artifacts:
            if artifact_path not in kept_paths and timestamp < cutoff:
                to_delete.append((artifact_path, size))
    
    # 3. Filter by size (keep latest until limit, skip kept paths)
    if max_size_bytes:
        total_size = 0
        for artifact_path, timestamp, size in sorted(artifacts, key=lambda x: x[1], reverse=True):
            if artifact_path in kept_paths:
                continue  # Always keep latest N
            if artifact_path in [p for p, _ in to_delete]:
                continue  # Already marked for deletion
            if total_size + size > max_size_bytes:
                to_delete.append((artifact_path, size))
            else:
                total_size += size
    
    # 4. Apply keep-latest after other filters (remove older ones beyond keep_latest)
    if keep_latest:
        kept = [p for p, _, _ in artifacts[:keep_latest]]
        for artifact_path, _, size in artifacts[keep_latest:]:
            if artifact_path not in kept_paths and artifact_path not in [p for p, _ in to_delete]:
                to_delete.append((artifact_path, size))
    
    # Remove duplicates
    to_delete_dict = {p: s for p, s in to_delete}
    to_delete = list(to_delete_dict.items())
    
    # Calculate freed bytes (even in dry-run)
    freed_bytes = sum(size for _, size in to_delete)
    
    # Delete
    deleted_count = 0
    
    if dry_run:
        print(f"\n[DRY RUN] Would delete {len(to_delete)} artifacts:")
        for artifact_path, size in to_delete:
            print(f"  - {artifact_path.name} ({format_size(size)})")
            deleted_files.append({
                "path": str(artifact_path),
                "size_bytes": size,
                "size": format_size(size),
            })
    else:
        print(f"\nDeleting {len(to_delete)} artifacts...")
        for artifact_path, size in to_delete:
            try:
                if artifact_path.is_dir():
                    import shutil
                    shutil.rmtree(artifact_path)
                else:
                    artifact_path.unlink()
                deleted_count += 1
                print(f"  ✓ Deleted {artifact_path.name} ({format_size(size)})")
                deleted_files.append({
                    "path": str(artifact_path),
                    "size_bytes": size,
                    "size": format_size(size),
                    "deleted": True,
                })
            except Exception as e:
                print(f"  ✗ Failed to delete {artifact_path.name}: {e}")
                deleted_files.append({
                    "path": str(artifact_path),
                    "size_bytes": size,
                    "size": format_size(size),
                    "deleted": False,
                    "error": str(e),
                })
    
    return deleted_count, freed_bytes, deleted_files


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Clean artifacts with retention policies")
    parser.add_argument(
        "--artifacts-root",
        type=str,
        default="out",
        help="Root directory for artifacts (default: out)",
    )
    parser.add_argument(
        "--older-than",
        type=str,
        help="Delete artifacts older than duration (e.g., '7d', '24h', '3600s')",
    )
    parser.add_argument(
        "--max-size",
        type=str,
        help="Maximum total size (e.g., '2GB', '500MB')",
    )
    parser.add_argument(
        "--keep-latest",
        type=int,
        help="Keep latest N runs",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without actually deleting",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )
    
    args = parser.parse_args()
    
    if not any([args.older_than, args.max_size, args.keep_latest]):
        parser.error("At least one retention policy must be specified")
    
    deleted_count, freed_bytes, deleted_files = clean_artifacts(
        artifacts_root=args.artifacts_root,
        older_than=args.older_than,
        max_size=args.max_size,
        keep_latest=args.keep_latest,
        dry_run=args.dry_run,
    )
    
    if args.json:
        result = {
            "deleted_count": deleted_count,
            "freed_bytes": freed_bytes,
            "freed_size": format_size(freed_bytes),
            "dry_run": args.dry_run,
            "deleted_files": deleted_files,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Summary:")
        print(f"  Deleted: {deleted_count} artifacts")
        print(f"  Freed: {format_size(freed_bytes)}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

