"""Test parallel DAG execution."""

from src.orchestrator.runner_parallel import OrchestratorParallel, PipelineStep
from src.orchestrator.factory import agent_factory, advisor_factory


def test_parallel_waves_run() -> None:
    """Test that parallel waves execute correctly."""
    steps = [
        PipelineStep(
            stage="A",
            agent="RequirementsDraftingAgent",
            advisor="RequirementsAdvisor",
            task="PRD for {product_idea}",
            category="requirements",
        ),
        PipelineStep(
            stage="B",
            agent="PromptRefinerAgent",
            advisor="PromptRefinerAdvisor",
            task="Refine for {product_idea}",
            category="requirements",
            depends_on=["A"],
        ),
    ]

    orch = OrchestratorParallel(
        agent_factory,
        advisor_factory,
        max_workers=4,
        score_thresholds={"requirements": 0.80},
    )
    orch.memory.set("product_idea", "Demo")

    res = orch.run_waves(steps)

    assert {h["stage"] for h in res["history"]} == {"A", "B"}
    assert all(h["approved"] for h in res["history"])


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


def test_independent_steps_run_parallel() -> None:
    """Test that independent steps run in parallel."""
    steps = [
        PipelineStep(
            stage="step1",
            agent="RequirementsDraftingAgent",
            advisor="RequirementsAdvisor",
            task="Task 1",
            category="requirements",
        ),
        PipelineStep(
            stage="step2",
            agent="RequirementsDraftingAgent",
            advisor="RequirementsAdvisor",
            task="Task 2",
            category="requirements",
        ),
    ]

    orch = OrchestratorParallel(
        agent_factory, advisor_factory, max_workers=2, score_thresholds={}
    )
    orch.memory.set("product_idea", "Test")

    res = orch.run_waves(steps)

    assert len(res["history"]) == 2
    assert all(h["approved"] for h in res["history"])

