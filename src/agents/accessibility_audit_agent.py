"""Accessibility audit agent."""

from __future__ import annotations

from typing import Any, Dict

from src.core.base import BaseFunctionalAgent
from src.core.types import AgentOutput, Artifact, AgentMetadata


class AccessibilityAuditAgent(BaseFunctionalAgent):
    """Agent that performs accessibility audits on HTML/CSS."""

    name = "AccessibilityAuditAgent"
    min_advisor_score = 0.90

    def process(self, task: str, context: Dict[str, Any]) -> AgentOutput:
        """
        Perform accessibility audit on HTML/CSS artifacts.

        Args:
            task: Audit task description
            context: Context with HTML/CSS artifacts

        Returns:
            AgentOutput with accessibility audit results
        """
        # Extract HTML/CSS artifacts
        html_content = ""
        css_content = ""

        for key, value in context.items():
            if isinstance(value, dict):
                artifacts = value.get("artifacts", [])
                for artifact in artifacts:
                    name = artifact.get("name", "")
                    content = str(artifact.get("content", ""))
                    if name.endswith(".html"):
                        html_content = content
                    elif name.endswith(".css"):
                        css_content = content

        # Simple accessibility checks
        violations = []
        if html_content:
            if 'alt=""' in html_content or 'alt=' not in html_content:
                violations.append("Missing or empty alt attributes on images")
            if '<header>' not in html_content:
                violations.append("Missing semantic <header> element")
            if '<main>' not in html_content:
                violations.append("Missing semantic <main> element")
            if 'lang=' not in html_content:
                violations.append("Missing lang attribute on <html>")

        if css_content:
            if "color:" in css_content and "background" not in css_content.lower():
                violations.append("Potential color contrast issues")

        audit_report = (
            "\n".join([f"- {v}" for v in violations])
            if violations
            else "No accessibility violations found."
        )

        artifacts = [
            Artifact(
                name="accessibility_audit.md",
                type="markdown",
                content=f"# Accessibility Audit\n\n## Violations\n\n{audit_report}",
                description="Accessibility audit results",
            )
        ]

        metadata = AgentMetadata(
            agent_name=self.name,
            stage=context.get("stage", "accessibility"),
            input_summary=task[:200],
        )

        return AgentOutput(
            content=f"Accessibility audit completed. Found {len(violations)} violations.",
            artifacts=artifacts,
            metadata=metadata,
        )

