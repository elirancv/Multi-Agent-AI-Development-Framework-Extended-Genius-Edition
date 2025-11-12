"""Tests for weighted advisor council."""

import pytest

from src.core.types import AgentMetadata, AgentOutput
from src.orchestrator.council import AdvisorCouncil


class MockAdvisor:
    """Mock advisor for testing."""

    def __init__(self, name: str, score: float):
        self.name = name
        self._score = score

    def review(self, output, task, context):
        return {
            "score": self._score,
            "approved": self._score >= 0.85,
            "critical_issues": [],
            "suggestions": [f"Suggestion from {self.name}"],
            "summary": f"Review by {self.name}",
            "severity": "low",
        }


def test_weighted_average():
    """Test that weighted average works correctly."""

    def factory(name: str):
        if name == "Advisor1":
            return MockAdvisor("Advisor1", 0.9)
        elif name == "Advisor2":
            return MockAdvisor("Advisor2", 0.7)
        return MockAdvisor(name, 0.8)

    council = AdvisorCouncil(
        advisor_factory=factory,
        advisors=["Advisor1", "Advisor2"],
        decision="average",
        weights={"Advisor1": 2.0, "Advisor2": 1.0},  # Advisor1 has double weight
    )

    output = AgentOutput("test", metadata=AgentMetadata(agent_name="test"))
    review = council.review(output, "task", {})

    # Weighted average: (0.9 * 2.0 + 0.7 * 1.0) / (2.0 + 1.0) = 0.833...
    assert review["score"] == pytest.approx(0.83, abs=0.01)


def test_unweighted_average():
    """Test that unweighted average works when no weights provided."""

    def factory(name: str):
        if name == "Advisor1":
            return MockAdvisor("Advisor1", 0.9)
        elif name == "Advisor2":
            return MockAdvisor("Advisor2", 0.7)
        return MockAdvisor(name, 0.8)

    council = AdvisorCouncil(
        advisor_factory=factory,
        advisors=["Advisor1", "Advisor2"],
        decision="average",
        weights=None,  # No weights
    )

    output = AgentOutput("test", metadata=AgentMetadata(agent_name="test"))
    review = council.review(output, "task", {})

    # Simple average: (0.9 + 0.7) / 2 = 0.8
    assert review["score"] == pytest.approx(0.8, abs=0.01)


def test_weighted_majority():
    """Test that majority decision ignores weights."""

    def factory(name: str):
        if name == "Advisor1":
            return MockAdvisor("Advisor1", 0.9)
        elif name == "Advisor2":
            return MockAdvisor("Advisor2", 0.7)
        return MockAdvisor(name, 0.8)

    council = AdvisorCouncil(
        advisor_factory=factory,
        advisors=["Advisor1", "Advisor2"],
        decision="majority",
        weights={"Advisor1": 2.0, "Advisor2": 1.0},  # Weights ignored for majority
    )

    output = AgentOutput("test", metadata=AgentMetadata(agent_name="test"))
    review = council.review(output, "task", {})

    # Majority: Advisor1 approves (0.9 >= 0.85), Advisor2 rejects (0.7 < 0.85)
    # So 1/2 approvals, which is not > 1, so should be False
    assert review["approved"] is False
