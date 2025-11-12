"""Advisor for reviewing prompt refinement quality."""

from __future__ import annotations

from typing import Any, Dict
from src.core.base import BaseAdvisor
from src.core.types import AgentOutput, AdvisorReview


class PromptRefinerAdvisor(BaseAdvisor):
    """Reviews refined prompts to ensure they address feedback properly."""

    name = "PromptRefinerAdvisor"

    def review(
        self, output: AgentOutput, task: str, context: Dict[str, Any]
    ) -> AdvisorReview:
        """Review refined prompt quality."""
        text = output.content.lower()

        issues: list[str] = []
        sugg: list[str] = []

        if "acceptance criteria" not in text:
            issues.append(
                "Refined prompt still lacks explicit Acceptance Criteria section."
            )
            sugg.append(
                "Add a dedicated Acceptance Criteria section with Given/When/Then."
            )

        if "non-functional" not in text and "nonfunctional" not in text:
            sugg.append("Add Non-Functional expectations (performance, security).")

        severity: Literal["low", "medium", "high", "critical"] = (
            "medium" if issues else "low"
        )
        base_score = 1.0 - 0.2 * len(issues)
        score = max(0.0, round(base_score, 2))
        approved = score >= 0.85 and "acceptance criteria" in text

        return {
            "score": score,
            "approved": approved,
            "critical_issues": issues,
            "suggestions": sugg,
            "summary": "Assessment of refined prompt completeness.",
            "severity": severity,  # type: ignore[return-value]
        }

