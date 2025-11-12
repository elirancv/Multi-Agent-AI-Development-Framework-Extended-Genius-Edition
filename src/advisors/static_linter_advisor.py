"""Advisor for static linter agent output."""

from __future__ import annotations

from typing import Any, Dict

from src.core.base import BaseAdvisor
from src.core.types import AgentOutput, AdvisorReview


class StaticLinterAdvisor(BaseAdvisor):
    """Advisor that reviews static linting results."""

    name = "StaticLinterAdvisor"

    def review(
        self, output: AgentOutput, task: str, context: Dict[str, Any]
    ) -> AdvisorReview:
        """
        Review linting output.

        Args:
            output: Agent output with linting results
            task: Original task
            context: Context dictionary

        Returns:
            AdvisorReview with score and feedback
        """
        issues = []
        suggestions = []

        # Check for lint report artifact
        has_report = any(
            a.name == "lint_report.md" for a in output.artifacts
        )

        if not has_report:
            issues.append("Missing lint_report.md artifact")

        # Check content quality
        if "No linting issues found" in output.content:
            suggestions.append("Consider running additional linting tools")

        # Score based on artifact presence and content quality
        score = 0.95 if has_report else 0.70
        if issues:
            score -= 0.15

        approved = score >= 0.85 and has_report
        severity = "high" if issues else "low"

        return {
            "score": round(score, 2),
            "approved": approved,
            "critical_issues": issues,
            "suggestions": suggestions,
            "summary": f"Linting review: {len(issues)} issues found",
            "severity": severity,
        }

