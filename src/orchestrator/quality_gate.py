"""Quality gates for pipeline validation."""

from __future__ import annotations

from typing import Any, Dict


class QualityGate:
    """Simple gate: enforce presence of artifacts and non-empty content."""

    def check(self, step_result: Dict[str, Any]) -> bool:
        """Check if step result meets quality criteria."""
        review = step_result.get("review") or {}
        if review.get("approved") is not True:
            return False
        artifacts = step_result.get("artifacts") or []
        return len(artifacts) > 0
