"""Advisor for reviewing code skeleton quality."""

from __future__ import annotations

from typing import Any, Dict
from src.core.base import BaseAdvisor
from src.core.types import AgentOutput, AdvisorReview


class CodeReviewAdvisor(BaseAdvisor):
    """Reviews code skeletons for completeness and structure."""

    name = "CodeReviewAdvisor"

    def review(
        self, output: AgentOutput, task: str, context: Dict[str, Any]
    ) -> AdvisorReview:
        """Review code skeleton artifacts."""
        ok = (
            any(a.name.endswith(".html") for a in output.artifacts)
            and any(a.name.endswith(".css") for a in output.artifacts)
        )

        issues: list[str] = []
        sugg: list[str] = []

        if not ok:
            issues.append("Missing either index.html or styles.css.")
            sugg.append("Ensure both artifacts are returned.")

        # Basic heuristic
        text = "".join([str(a.content).lower() for a in output.artifacts])
        if "<header>" not in text or "<footer>" not in text:
            sugg.append(
                "Add <header> and <footer> landmarks for better structure."
            )

        score = 1.0 - 0.2 * len(issues)
        approved = ok and score >= 0.90

        severity: Literal["low", "medium", "high", "critical"] = (
            "medium" if issues else "low"
        )

        return {
            "score": round(max(score, 0.0), 2),
            "approved": approved,
            "critical_issues": issues,
            "suggestions": sugg,
            "summary": "Static code skeleton review.",
            "severity": severity,  # type: ignore[return-value]
        }

