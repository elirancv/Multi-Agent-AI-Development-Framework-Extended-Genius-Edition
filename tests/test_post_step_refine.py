"""Test post-step hooks, especially PromptRefinerOnFailure."""

from src.orchestrator.runner import Orchestrator, PipelineStep
from src.orchestrator.factory import agent_factory, advisor_factory
from src.orchestrator.hooks import PromptRefinerOnFailure


def test_prompt_refiner_runs_on_failure() -> None:
    """Test that PromptRefiner hook runs when step fails."""
    # Create a strict advisor that always fails
    from src.advisors.requirements_advisor import RequirementsAdvisor

    class StrictRequirementsAdvisor(RequirementsAdvisor):
        """Advisor that always rejects to test failure hook."""

        def review(self, output, task, context):
            r = super().review(output, task, context)
            r["approved"] = False  # force failure
            r["score"] = 0.5
            return r

    # Create custom advisor factory
    def strict_advisor_factory(name: str):
        if name == "RequirementsAdvisor":
            return StrictRequirementsAdvisor()
        return advisor_factory(name)

    # Create orchestrator with hook
    orch = Orchestrator(
        agent_factory=agent_factory,
        advisor_factory=strict_advisor_factory,
        post_step_hooks=[
            PromptRefinerOnFailure(
                agent_factory=agent_factory, advisor_factory=advisor_factory
            )
        ],
    )

    orch.memory.set("product_idea", "Demo")

    steps = [
        PipelineStep(
            stage="requirements",
            agent="RequirementsDraftingAgent",
            advisor="RequirementsAdvisor",
            task="PRD for {product_idea}",
        )
    ]

    res = orch.run(steps)

    # On failure, refined prompt should be present
    assert res["history"][0]["approved"] is False
    assert orch.memory.get("requirements.refined_prompt.content") is not None


def test_prompt_refiner_skips_on_success() -> None:
    """Test that hook doesn't run when step succeeds."""
    orch = Orchestrator(
        agent_factory=agent_factory,
        advisor_factory=advisor_factory,
        post_step_hooks=[
            PromptRefinerOnFailure(
                agent_factory=agent_factory, advisor_factory=advisor_factory
            )
        ],
    )

    orch.memory.set("product_idea", "Demo")

    steps = [
        PipelineStep(
            stage="requirements",
            agent="RequirementsDraftingAgent",
            advisor="RequirementsAdvisor",
            task="PRD for {product_idea}",
        )
    ]

    res = orch.run(steps)

    # On success, no refined prompt should be created
    assert res["history"][0]["approved"] is True
    assert orch.memory.get("requirements.refined_prompt.content") is None

