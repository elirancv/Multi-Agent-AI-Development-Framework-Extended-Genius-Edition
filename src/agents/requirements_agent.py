"""Requirements drafting agent for creating PRD documents."""

from __future__ import annotations

from typing import Any, Dict, List
from src.core.base import BaseFunctionalAgent
from src.core.types import AgentOutput, Artifact, AgentMetadata


class RequirementsDraftingAgent(BaseFunctionalAgent):
    """Creates PRD-like documents from natural language prompts."""

    name = "RequirementsDraftingAgent"
    min_advisor_score = 0.80  # slightly relaxed for specification drafts

    def process(self, task: str, context: Dict[str, Any]) -> AgentOutput:
        """Creates a concise PRD-like skeleton from a natural-language prompt."""
        sections: List[str] = [
            "# Product Requirements (Draft)",
            "## Goal",
            f"{task.strip()}",
            "## Scope",
            "- In scope: MVP features only\n- Out of scope: Integrations not listed",
            "## Key Personas",
            "- End User\n- Admin",
            "## Functional Requirements",
            "1. User can...\n2. System shall...",
            "## Non-Functional Requirements",
            "- Performance: < 200ms p95\n- Security: Role-based access",
            "## Acceptance Criteria",
            "- Given/When/Then bullets per feature",
        ]

        content = "\n\n".join(sections)

        artifacts = [
            Artifact(
                name="prd_draft.md",
                type="markdown",
                content=content,
                description="Initial PRD skeleton generated from task + context",
            )
        ]

        meta = AgentMetadata(
            agent_name=self.name,
            stage=context.get("stage", "requirements"),
            input_summary=task[:200],
        )

        return AgentOutput(content=content, artifacts=artifacts, metadata=meta)

