"""Post-step hooks for orchestrator execution."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Protocol

from src.core.base import BaseAdvisor, BaseFunctionalAgent
from src.core.memory import SharedMemory
from src.core.types import AgentOutput


class PostStepHook(Protocol):
    """
    Called after each step executes (approved or not).
    Implementations may mutate shared memory or emit additional artifacts.
    """

    def __call__(
        self,
        *,
        step_result: Dict[str, Any],
        shared_memory: SharedMemory,
    ) -> None:
        """Execute hook logic."""
        ...


@dataclass
class PromptRefinerOnFailure:
    """
    When a step fails review, run a PromptRefinerAgent + Advisor to produce a
    refined prompt and store it into memory as `<failed_stage>.refined_prompt`.
    """

    agent_factory: Callable[[str], BaseFunctionalAgent]
    advisor_factory: Callable[[str], BaseAdvisor]
    refiner_agent: str = "PromptRefinerAgent"
    refiner_advisor: str = "PromptRefinerAdvisor"
    min_score: float = 0.85
    task_template: str = "Refine the prompt based on the last review for: {product_idea}"

    def __call__(self, *, step_result: Dict[str, Any], shared_memory: SharedMemory) -> None:
        """Execute prompt refinement hook on step failure."""
        if step_result.get("approved", True):
            return  # only act on failures

        stage = step_result["stage"]

        # Expect that the orchestrator stored the last review/output in memory keys:
        #   f"{stage}.last_review" and f"{stage}.last_output"
        # If not present, still try to run with the global context.
        agent = self.agent_factory(self.refiner_agent)
        advisor = self.advisor_factory(self.refiner_advisor)

        # Render a simple task using the memory snapshot
        task = self._render(self.task_template, shared_memory.to_dict())

        output: AgentOutput = agent.process(task=task, context=shared_memory.to_dict())
        agent.validate_output(output)

        review = advisor.review(output=output, task=task, context=shared_memory.to_dict())

        if advisor.gate(review, self.min_score):
            # Persist refined prompt and artifacts
            shared_memory.update(
                {
                    f"{stage}.refined_prompt.content": output.content,
                    f"{stage}.refined_prompt.artifacts": [a.to_dict() for a in output.artifacts],
                    f"{stage}.refined_prompt.review": review,
                }
            )
        else:
            # Even if refiner didn't pass, keep results for transparency
            shared_memory.update(
                {
                    f"{stage}.refined_prompt_attempt.content": output.content,
                    f"{stage}.refined_prompt_attempt.artifacts": [
                        a.to_dict() for a in output.artifacts
                    ],
                    f"{stage}.refined_prompt_attempt.review": review,
                }
            )

    @staticmethod
    def _render(template: str, mem: Dict[str, Any]) -> str:
        """Render template with memory values."""
        out = template
        for k, v in mem.items():
            token = "{" + k + "}"
            if token in out:
                out = out.replace(token, str(v))
        return out
