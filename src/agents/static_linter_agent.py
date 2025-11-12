"""Static code linter agent."""

from __future__ import annotations

from typing import Any, Dict

from src.core.base import BaseFunctionalAgent
from src.core.types import AgentOutput, Artifact, AgentMetadata


class StaticLinterAgent(BaseFunctionalAgent):
    """Agent that performs static code analysis."""

    name = "StaticLinterAgent"
    min_advisor_score = 0.90

    def process(self, task: str, context: Dict[str, Any]) -> AgentOutput:
        """
        Perform static linting on code artifacts.

        Args:
            task: Linting task description
            context: Context with code artifacts

        Returns:
            AgentOutput with linting results
        """
        # Extract code artifacts from context
        code_artifacts = []
        for key, value in context.items():
            if isinstance(value, dict) and "artifacts" in key:
                code_artifacts.extend(value.get("artifacts", []))

        # Simple linting simulation
        issues = []
        for artifact in code_artifacts:
            content = str(artifact.get("content", ""))
            if "TODO" in content:
                issues.append(f"Found TODO in {artifact.get('name', 'unknown')}")
            if len(content) > 10000:
                issues.append(f"Large file: {artifact.get('name', 'unknown')}")

        lint_report = "\n".join(issues) if issues else "No linting issues found."

        artifacts = [
            Artifact(
                name="lint_report.md",
                type="markdown",
                content=f"# Linting Report\n\n{lint_report}",
                description="Static code analysis results",
            )
        ]

        metadata = AgentMetadata(
            agent_name=self.name,
            stage=context.get("stage", "linting"),
            input_summary=task[:200],
        )

        return AgentOutput(
            content=f"Linting completed. Found {len(issues)} issues.",
            artifacts=artifacts,
            metadata=metadata,
        )

