"""Test that AdvisorCouncil has name attribute."""

from src.core.types import AgentMetadata, AgentOutput
from src.orchestrator.council import AdvisorCouncil
from src.orchestrator.factory import advisor_factory


def test_council_has_name_attribute() -> None:
    """Test that AdvisorCouncil has name attribute for logging."""
    council = AdvisorCouncil(
        advisor_factory=advisor_factory,
        advisors=["RequirementsAdvisor", "PromptRefinerAdvisor"],
        decision="majority",
        min_score=0.85,
    )

    assert hasattr(council, "name")
    assert council.name == "AdvisorCouncil"


def test_council_name_in_logging() -> None:
    """Test that council name can be used in logging without error."""
    council = AdvisorCouncil(
        advisor_factory=advisor_factory,
        advisors=["RequirementsAdvisor"],
        decision="majority",
    )

    # Should not raise AttributeError
    advisor_name = getattr(council, "name", "AdvisorCouncil")
    assert advisor_name == "AdvisorCouncil"

    # Test review still works
    output = AgentOutput(content="test", metadata=AgentMetadata(agent_name="TestAgent"))
    review = council.review(output=output, task="test", context={})
    assert "score" in review
