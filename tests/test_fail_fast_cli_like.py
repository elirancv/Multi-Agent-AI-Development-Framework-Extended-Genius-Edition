"""Test fail-fast behavior similar to CLI."""

from src.orchestrator.runner_parallel import OrchestratorParallel, PipelineStep
from src.orchestrator.factory import agent_factory, advisor_factory


def test_fail_fast_detection() -> None:
    """Test that we can detect failures for fail-fast logic."""
    # Create a step that will likely fail (very high threshold)
    step = PipelineStep(
        stage="high_threshold",
        agent="RequirementsDraftingAgent",
        advisor="RequirementsAdvisor",
        task="Test",
        category="strict",
        max_retries=0,
    )

    orch = OrchestratorParallel(
        agent_factory,
        advisor_factory,
        score_thresholds={"strict": 0.99},  # Very high threshold
    )
    orch.memory.set("product_idea", "Test")

    res = orch.run_waves([step])

    h = res["history"][0]
    # With threshold 0.99, should pass if score >= 0.99, fail otherwise
    # The test verifies that the threshold is correctly applied
    if h["approved"]:
        assert h["score"] >= 0.99, "Approved step must meet threshold"
    else:
        assert h["score"] < 0.99, "Failed step must be below threshold"


def test_policy_thresholds_override() -> None:
    """Test that policy thresholds override agent defaults."""
    step = PipelineStep(
        stage="req",
        agent="RequirementsDraftingAgent",
        advisor="RequirementsAdvisor",
        task="PRD",
        category="requirements",
    )

    orch = OrchestratorParallel(
        agent_factory,
        advisor_factory,
        score_thresholds={"requirements": 0.80},
    )
    orch.memory.set("product_idea", "X")

    res = orch.run_waves([step])

    h = next(x for x in res["history"] if x["stage"] == "req")
    assert h["approved"] is True
    assert h["score"] >= 0.80

