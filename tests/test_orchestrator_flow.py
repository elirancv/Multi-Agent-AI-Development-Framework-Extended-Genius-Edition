"""Test orchestrator pipeline execution."""

from src.orchestrator.runner import Orchestrator, PipelineStep
from src.orchestrator.factory import agent_factory, advisor_factory


def test_pipeline_approves_requirements() -> None:
    """Test that pipeline execution works and approves valid requirements."""
    orch = Orchestrator(agent_factory=agent_factory, advisor_factory=advisor_factory)
    orch.memory.set("product_idea", "Test product")
    orch.memory.set("stage", "requirements")

    steps = [
        PipelineStep(
            stage="requirements",
            agent="RequirementsDraftingAgent",
            advisor="RequirementsAdvisor",
            task="Create PRD for: {product_idea}",
            max_retries=0,
        )
    ]

    res = orch.run(steps)
    hist = res["history"][0]

    assert hist["approved"] is True
    assert hist["score"] >= 0.80

