"""Filesystem artifact persistence for pipeline runs."""

from __future__ import annotations

import base64
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Union

from src.core.memory import SharedMemory


def _safe_name(name: str) -> str:
    """Sanitize filename to be filesystem-safe."""
    # Replace non-alphanumeric (except dots, dashes, underscores, spaces) with underscore
    name = re.sub(r"[^\w\-. ]+", "_", name)
    # Limit length to avoid filesystem issues
    return name[:120] or "artifact.bin"


def persist_artifacts(
    result_or_memory: Union[Dict[str, Any], SharedMemory], out_dir: str = "out"
) -> int:
    """
    Persist artifacts from orchestrator memory to filesystem.

    Args:
        result_or_memory: Either result dict with run_id/memory or SharedMemory object
        out_dir: Output directory root

    Returns:
        Number of artifacts saved
    """
    # Handle both result dict and SharedMemory
    if isinstance(result_or_memory, SharedMemory):
        run_id = "unknown"
        mem = result_or_memory.to_dict()
    else:
        run_id = result_or_memory.get("run_id", "unknown")
        mem = result_or_memory.get("memory", {})
    base = Path(out_dir) / str(run_id)
    base.mkdir(parents=True, exist_ok=True)

    saved_count = 0
    manifest = []

    # Walk stages present in memory by suffix convention
    stages = {k.split(".")[0] for k in mem.keys() if "." in k}
    for stage in stages:
        arts: List[Dict[str, Any]] = mem.get(f"{stage}.artifacts") or []
        stage_dir = base / stage
        if not arts:
            continue
        stage_dir.mkdir(parents=True, exist_ok=True)
        for a in arts:
            raw_name = a.get("name") or "artifact"
            name = _safe_name(str(raw_name))
            content = a.get("content", "")
            art_type = a.get("type", "text")
            p = stage_dir / name

            # Determine content bytes for manifest
            content_bytes = b""

            # Support binary artifacts
            if isinstance(content, bytes):
                p.write_bytes(content)
                content_bytes = content
            else:
                # Try to decode base64 if it looks like base64 string
                if isinstance(content, str) and len(content) > 0:
                    try:
                        decoded = base64.b64decode(content, validate=True)
                        # If decoding succeeds and produces reasonable binary, save as binary
                        if len(decoded) > 0:
                            p.write_bytes(decoded)
                            content_bytes = decoded
                            saved_count += 1
                            # Add to manifest
                            sha256 = hashlib.sha256(content_bytes).hexdigest()
                            manifest.append(
                                {
                                    "stage": stage,
                                    "name": raw_name,
                                    "safe_name": name,
                                    "type": art_type,
                                    "bytes": len(content_bytes),
                                    "sha256": sha256,
                                }
                            )
                            continue
                    except Exception:
                        pass  # Fall through to text handling

                # Default: save as text
                p.write_text(str(content), encoding="utf-8")
                content_bytes = str(content).encode("utf-8")

            saved_count += 1

            # Add to manifest
            sha256 = hashlib.sha256(content_bytes).hexdigest()
            manifest.append(
                {
                    "stage": stage,
                    "name": raw_name,
                    "safe_name": name,
                    "type": art_type,
                    "bytes": len(content_bytes),
                    "sha256": sha256,
                }
            )

    # Write manifest.json
    manifest_path = base / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8"
    )

    # Also drop a short SUMMARY.md
    (base / "SUMMARY.md").write_text(
        f"# Run `{run_id}`\n\nArtifacts stored under stage folders.\n",
        encoding="utf-8",
    )
    return saved_count
