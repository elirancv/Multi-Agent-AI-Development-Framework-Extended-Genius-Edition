"""Budget enforcement for pipeline execution."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Budget:
    """Execution budget limits."""

    max_runtime_sec: Optional[float] = None
    max_stages: Optional[int] = None
    max_artifacts_bytes: Optional[int] = None


class BudgetExceededError(RuntimeError):
    """Raised when budget limits are exceeded."""

    pass


def enforce_budget(budget: Budget, stats: Dict[str, Any]) -> None:
    """
    Enforce budget limits against current stats.

    Args:
        budget: Budget configuration
        stats: Current execution statistics

    Raises:
        BudgetExceededError: If any budget limit is exceeded
    """
    if budget.max_stages is not None:
        stages = stats.get("stages", 0)
        if stages > budget.max_stages:
            raise BudgetExceededError(
                f"Stage budget exceeded: {stages} > {budget.max_stages}"
            )

    if budget.max_artifacts_bytes is not None:
        artifacts_bytes = stats.get("artifacts_bytes", 0)
        if artifacts_bytes > budget.max_artifacts_bytes:
            raise BudgetExceededError(
                f"Artifacts size budget exceeded: {artifacts_bytes} > {budget.max_artifacts_bytes}"
            )

    if budget.max_runtime_sec is not None:
        runtime_sec = stats.get("runtime_sec", 0.0)
        if runtime_sec > budget.max_runtime_sec:
            raise BudgetExceededError(
                f"Runtime budget exceeded: {runtime_sec:.1f}s > {budget.max_runtime_sec}s"
            )

