"""Test Advisor Council for multi-advisor reviews."""

from src.core.types import AgentOutput, Artifact, AgentMetadata
from src.orchestrator.council import AdvisorCouncil
from src.orchestrator.factory import advisor_factory


def dummy_output() -> AgentOutput:
    """Create a dummy agent output for testing."""
    meta = AgentMetadata(agent_name="X")
    art = Artifact(name="x.md", type="markdown", content="# hi")
    return AgentOutput(content="ok", artifacts=[art], metadata=meta)


def test_council_majority_passes() -> None:
    """Test council with majority decision mode."""
    council = AdvisorCouncil(
        advisor_factory=advisor_factory,
        advisors=["RequirementsAdvisor", "PromptRefinerAdvisor"],
        decision="majority",
        min_score=0.80,
    )
    review = council.review(output=dummy_output(), task="t", context={})
    assert "avg" in review["summary"]
    assert review["score"] >= 0.0
    assert isinstance(review["approved"], bool)
    assert isinstance(review["critical_issues"], list)
    assert isinstance(review["suggestions"], list)


def test_council_average_mode() -> None:
    """Test council with average decision mode."""
    council = AdvisorCouncil(
        advisor_factory=advisor_factory,
        advisors=["RequirementsAdvisor", "PromptRefinerAdvisor"],
        decision="average",
        min_score=0.80,
    )
    review = council.review(output=dummy_output(), task="t", context={})
    assert "average" in review["summary"].lower() or "avg" in review["summary"]
    assert review["score"] >= 0.0


def test_council_aggregates_issues() -> None:
    """Test that council aggregates issues and suggestions."""
    council = AdvisorCouncil(
        advisor_factory=advisor_factory,
        advisors=["RequirementsAdvisor", "PromptRefinerAdvisor"],
        decision="majority",
        min_score=0.80,
    )
    review = council.review(output=dummy_output(), task="t", context={})
    # Should have aggregated fields
    assert "critical_issues" in review
    assert "suggestions" in review
    assert "severity" in review

