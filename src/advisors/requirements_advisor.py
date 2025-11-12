"""Advisor for reviewing requirements documents."""

from __future__ import annotations

from typing import Any, Dict
from src.core.base import BaseAdvisor
from src.core.types import AgentOutput, AdvisorReview


class RequirementsAdvisor(BaseAdvisor):
    """Reviews requirements documents for completeness and quality."""

    name = "RequirementsAdvisor"

    def review(
        self, output: AgentOutput, task: str, context: Dict[str, Any]
    ) -> AdvisorReview:
        """Review requirements document quality."""
        content = output.content.strip().lower()

        issues: list[str] = []
        suggestions: list[str] = []

        # Simple rubric
        if "acceptance criteria" not in content:
            issues.append("Missing explicit Acceptance Criteria section.")
            suggestions.append("Add 'Given/When/Then' criteria per feature.")

        if "non-functional" not in content:
            issues.append("Missing Non-Functional Requirements.")
            suggestions.append("Include performance/security/reliability targets.")

        if len(content) < 300:
            suggestions.append(
                "Expand functional requirements to at least 5 concrete bullets."
            )

        severity: Literal["low", "medium", "high", "critical"] = (
            "medium" if issues else "low"
        )
        score = max(0.0, 1.0 - 0.15 * len(issues))
        approved = (
            score >= 0.80
            and "acceptance criteria" in content
            and "non-functional" in content
        )

        return {
            "score": round(score, 2),
            "approved": approved,
            "critical_issues": issues,
            "suggestions": suggestions,
            "summary": "Initial PRD draft quality assessment.",
            "severity": severity,
        }

