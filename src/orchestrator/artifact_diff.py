"""Artifact diff utilities for text comparison."""

from __future__ import annotations

import difflib
from typing import Tuple


def diff_text(old: str, new: str, context: int = 2) -> str:
    """
    Generate unified diff between two text strings.

    Args:
        old: Old text content
        new: New text content
        context: Number of context lines around changes

    Returns:
        Unified diff string
    """
    d = difflib.unified_diff(
        old.splitlines(keepends=False),
        new.splitlines(keepends=False),
        lineterm="",
        n=context,
    )
    return "\n".join(d)


def diff_summary(old: str, new: str) -> Tuple[int, int]:
    """
    Get summary statistics for diff.

    Args:
        old: Old text content
        new: New text content

    Returns:
        Tuple of (lines_added, lines_removed)
    """
    diff_lines = diff_text(old, new).splitlines()
    added = sum(1 for line in diff_lines if line.startswith("+") and not line.startswith("+++"))
    removed = sum(1 for line in diff_lines if line.startswith("-") and not line.startswith("---"))
    return added, removed
