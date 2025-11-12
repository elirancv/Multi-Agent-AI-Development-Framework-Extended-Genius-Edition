"""Agent that refines prompts based on advisor feedback."""

from __future__ import annotations

from typing import Any, Dict, List
from src.core.base import BaseFunctionalAgent
from src.core.types import AgentOutput, Artifact, AgentMetadata


class PromptRefinerAgent(BaseFunctionalAgent):
    """
    Refines prompts based on advisor feedback and previous failures.
    Takes rejected output and advisor review to generate improved prompt.
    """

    name = "PromptRefinerAgent"
    min_advisor_score = 0.85  # Standard threshold

    def process(self, task: str, context: Dict[str, Any]) -> AgentOutput:
        """
        Synthesize a refined prompt from the last advisor review + original task.
        
        Expected context keys (if exist):
          - <stage>.last_review: AdvisorReview dict
          - <stage>.last_output: AgentOutput dict
        """
        # Heuristics: look for any "<stage>.last_review" keys
        last_review: Dict[str, Any] = {}
        for k, v in context.items():
            if k.endswith(".last_review") and isinstance(v, dict):
                last_review = v
                break

        issues: List[str] = (
            last_review.get("critical_issues", []) if last_review else []
        )
        suggestions: List[str] = (
            last_review.get("suggestions", []) if last_review else []
        )

        # Build refined prompt with structured sections
        refined_sections = [
            "# Refined Prompt",
            "## Objective",
            task.strip() or "Refine the previous task.",
            "## Must Address (from last review)",
        ]

        refined_sections.extend([f"- {i}" for i in issues] or ["- (none)"])

        refined_sections.extend(["## Improvements to Apply"])

        refined_sections.extend(
            [f"- {s}" for s in suggestions]
            or ["- Expand details and acceptance criteria."]
        )

        refined_sections.extend(
            [
                "## Output Expectations",
                "- Produce concise, unambiguous instructions.",
                "- Include Acceptance Criteria in Given/When/Then.",
                "- Include Non-Functional requirements if relevant.",
            ]
        )

        refined_task = "\n".join(refined_sections)

        content = refined_task

        artifacts = [
            Artifact(
                name="refined_prompt.md",
                type="markdown",
                content=refined_task,
                description="Refined prompt",
            )
        ]

        meta = AgentMetadata(
            agent_name=self.name,
            stage=context.get("stage", "prompt_refine"),
            input_summary=task[:200],
            extra={
                "issues_addressed": len(issues),
                "suggestions_applied": len(suggestions),
            },
        )

        return AgentOutput(content=content, artifacts=artifacts, metadata=meta)

