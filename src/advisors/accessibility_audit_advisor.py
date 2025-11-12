"""Advisor for accessibility audit agent output."""

from __future__ import annotations

from typing import Any, Dict

from src.core.base import BaseAdvisor
from src.core.types import AgentOutput, AdvisorReview


class AccessibilityAuditAdvisor(BaseAdvisor):
    """Advisor that reviews accessibility audit results."""

    name = "AccessibilityAuditAdvisor"

    def review(
        self, output: AgentOutput, task: str, context: Dict[str, Any]
    ) -> AdvisorReview:
        """
        Review accessibility audit output.

        Args:
            output: Agent output with audit results
            task: Original task
            context: Context dictionary

        Returns:
            AdvisorReview with score and feedback
        """
        issues = []
        suggestions = []

        # Check for audit report artifact
        has_report = any(
            a.name == "accessibility_audit.md" for a in output.artifacts
        )

        if not has_report:
            issues.append("Missing accessibility_audit.md artifact")

        # Check content for violations
        if "violations" in output.content.lower():
            if "Found 0 violations" not in output.content:
                issues.append("Accessibility violations detected")

        # Score based on artifact presence and violations
        score = 0.95 if has_report else 0.70
        if issues:
            score -= 0.20

        approved = score >= 0.90 and has_report and len(issues) == 0
        severity = "high" if issues else "low"

        return {
            "score": round(score, 2),
            "approved": approved,
            "critical_issues": issues,
            "suggestions": suggestions,
            "summary": f"Accessibility audit review: {len(issues)} critical issues",
            "severity": severity,
        }

