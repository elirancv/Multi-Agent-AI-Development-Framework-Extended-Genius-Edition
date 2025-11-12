# Copyright (c) 2025 Multi-Agent AI Development Framework Contributors
# Licensed under the MIT License

"""Base classes for agents and advisors."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict
from .types import AgentOutput, AdvisorReview


class BaseFunctionalAgent(ABC):
    """
    Every functional agent implements `process`.
    Must return AgentOutput with the canonical structure.
    """

    name: str = "BaseFunctionalAgent"
    min_advisor_score: float = 0.85  # can be overridden per agent
    version: str = "0.1.0"  # Agent version for cache invalidation

    @abstractmethod
    def process(self, task: str, context: Dict[str, Any]) -> AgentOutput:
        """Produce structured output for the given task and context."""
        raise NotImplementedError

    def validate_output(self, output: AgentOutput) -> None:
        if not isinstance(output, AgentOutput):
            raise TypeError(f"{self.name} must return AgentOutput")
        if not isinstance(output.content, str) or not output.content.strip():
            raise ValueError(f"{self.name} produced empty content")
        # artifacts + metadata are validated at serialization time

    def describe(self) -> str:
        return f"{self.name} (min_advisor_score={self.min_advisor_score})"


class BaseAdvisor(ABC):
    """Each agent must have a 1:1 matching advisor that reviews the output."""

    name: str = "BaseAdvisor"

    @abstractmethod
    def review(
        self, output: AgentOutput, task: str, context: Dict[str, Any]
    ) -> AdvisorReview:
        """
        Return an AdvisorReview dict with the required fields.
        Implementers should ensure score ∈ [0,1] and severity is coherent with issues.
        """
        raise NotImplementedError

    def gate(self, review: AdvisorReview, min_score: float) -> bool:
        """Convenience: decide pass/fail by score and approval flag."""
        return review["approved"] and review["score"] >= min_score

