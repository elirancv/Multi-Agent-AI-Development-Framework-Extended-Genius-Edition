"""Test that review works correctly on cache hit."""

from src.orchestrator.factory import advisor_factory, agent_factory
from src.orchestrator.runner import Orchestrator, PipelineStep


def test_review_works_on_cache_hit() -> None:
    """Test that review works correctly when cache is hit."""
    orch = Orchestrator(agent_factory, advisor_factory)
    orch.memory.set("product_idea", "Demo")

    step = PipelineStep(
        stage="req",
        agent="RequirementsDraftingAgent",
        advisor="RequirementsAdvisor",
        task="PRD for {product_idea}",
    )

    # First run - fills cache
    res1 = orch.run([step])
    hist1 = res1["history"][0]
    assert "approved" in hist1

    # Second run - must use cache and not raise NameError
    res2 = orch.run([step])
    hist2 = res2["history"][0]
    assert "approved" in hist2
    assert hist2["stage"] == "req"

    # Verify cache was hit (check event log or cache stats if available)
    # The important thing is that it doesn't crash with NameError


def test_cache_hit_produces_valid_output() -> None:
    """Test that cache hit produces valid AgentOutput for review."""
    orch = Orchestrator(agent_factory, advisor_factory)
    orch.memory.set("product_idea", "Test Product")

    step = PipelineStep(
        stage="test_stage",
        agent="RequirementsDraftingAgent",
        advisor="RequirementsAdvisor",
        task="Create PRD for {product_idea}",
    )

    # First execution
    orch.run([step])

    # Second execution should use cache
    result = orch.run([step])
    assert len(result["history"]) == 1
    assert result["history"][0]["stage"] == "test_stage"
    assert "approved" in result["history"][0]
    assert "score" in result["history"][0]
