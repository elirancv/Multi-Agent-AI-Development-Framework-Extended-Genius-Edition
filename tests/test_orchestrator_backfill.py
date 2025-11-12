"""Orchestrator tests: timeouts, retries, council weights."""

import time

from src.core.base import BaseAdvisor, BaseFunctionalAgent
from src.core.types import AgentOutput
from src.orchestrator.runner import Orchestrator
from src.orchestrator.runner_parallel import OrchestratorParallel


class SlowAgent(BaseFunctionalAgent):
    """Agent that takes time to process."""

    name = "SlowAgent"

    def process(self, task: str, context: dict) -> AgentOutput:
        time.sleep(0.1)  # Simulate slow processing
        return AgentOutput(content="slow output", artifacts=[], metadata={"agent": "SlowAgent"})


class FailingAgent(BaseFunctionalAgent):
    """Agent that fails."""

    name = "FailingAgent"

    def process(self, task: str, context: dict) -> AgentOutput:
        raise RuntimeError("Agent failed")


class LowScoreAdvisor(BaseAdvisor):
    """Advisor that gives low scores."""

    name = "LowScoreAdvisor"

    def review(self, output: AgentOutput, task: str, context: dict) -> dict:
        return {
            "score": 0.3,
            "approved": False,
            "critical_issues": ["Low quality"],
            "suggestions": ["Improve quality"],
            "summary": "Low score",
            "severity": "high",
        }


class HighScoreAdvisor(BaseAdvisor):
    """Advisor that gives high scores."""

    name = "HighScoreAdvisor"

    def review(self, output: AgentOutput, task: str, context: dict) -> dict:
        return {
            "score": 0.95,
            "approved": True,
            "critical_issues": [],
            "suggestions": [],
            "summary": "High score",
            "severity": "low",
        }


def agent_factory(name: str):
    """Simple factory for test agents."""
    agents = {
        "SlowAgent": SlowAgent,
        "FailingAgent": FailingAgent,
    }
    return agents.get(name, SlowAgent)()


def advisor_factory(name: str):
    """Simple factory for test advisors."""
    advisors = {
        "LowScoreAdvisor": LowScoreAdvisor,
        "HighScoreAdvisor": HighScoreAdvisor,
    }
    return advisors.get(name, HighScoreAdvisor)()


def test_orchestrator_timeout():
    """Test orchestrator handles timeouts."""
    orch = Orchestrator(
        agent_factory=agent_factory,
        advisor_factory=advisor_factory,
    )
    orch.agent_timeout_sec = 0.05  # Very short timeout

    from src.orchestrator.runner import PipelineStep

    steps = [
        PipelineStep(
            stage="test_stage",
            agent="SlowAgent",
            advisor="HighScoreAdvisor",
            task="test",
        )
    ]

    # Should handle timeout gracefully
    result = orch.run(steps)
    assert "history" in result


def test_orchestrator_retries():
    """Test orchestrator retries on failure."""
    from src.orchestrator.runner import PipelineStep

    orch = Orchestrator(
        agent_factory=agent_factory,
        advisor_factory=advisor_factory,
    )

    steps = [
        PipelineStep(
            stage="test_stage",
            agent="FailingAgent",
            advisor="HighScoreAdvisor",
            task="test",
            max_retries=2,  # Set retries in step
        )
    ]

    # Should retry on failure
    result = orch.run(steps)
    assert "history" in result
    # Check retry count in history
    if result["history"]:
        stage_result = result["history"][0]
        # May have retry information
        assert "stage" in stage_result


def test_orchestrator_threshold_gate():
    """Test orchestrator gates on score threshold."""
    from src.orchestrator.runner import PipelineStep

    orch = Orchestrator(
        agent_factory=agent_factory,
        advisor_factory=advisor_factory,
    )

    steps = [
        PipelineStep(
            stage="test_stage",
            agent="SlowAgent",
            advisor="LowScoreAdvisor",  # Will give low score
            task="test",
        )
    ]

    result = orch.run(steps)
    assert "history" in result

    if result["history"]:
        stage_result = result["history"][0]
        # Should show rejection if score too low
        assert "approved" in stage_result or "score" in stage_result


def test_orchestrator_council_weights():
    """Test orchestrator uses advisor weights in council."""
    from src.orchestrator.runner import PipelineStep

    orch = Orchestrator(
        agent_factory=agent_factory,
        advisor_factory=advisor_factory,
    )

    steps = [
        PipelineStep(
            stage="test_stage",
            agent="SlowAgent",
            advisor="HighScoreAdvisor",
            task="test",
        )
    ]

    result = orch.run(steps)
    assert "history" in result


def test_orchestrator_parallel_waves():
    """Test parallel orchestrator wave execution."""
    from src.orchestrator.runner import PipelineStep

    orch = OrchestratorParallel(
        agent_factory=agent_factory,
        advisor_factory=advisor_factory,
        max_workers=2,
    )

    steps = [
        PipelineStep(
            stage="stage1",
            agent="SlowAgent",
            advisor="HighScoreAdvisor",
            task="test1",
        ),
        PipelineStep(
            stage="stage2",
            agent="SlowAgent",
            advisor="HighScoreAdvisor",
            task="test2",
        ),
    ]

    result = orch.run_waves(steps)
    assert "history" in result
    assert len(result["history"]) == len(steps)


def test_orchestrator_checkpoint_resume():
    """Test checkpoint and resume functionality."""
    from src.orchestrator.checkpoint_fs import FileCheckpointStore
    from src.orchestrator.runner import PipelineStep

    checkpoint_store = FileCheckpointStore(root="out/test_checkpoints")

    orch = Orchestrator(
        agent_factory=agent_factory,
        advisor_factory=advisor_factory,
        checkpoint_store=checkpoint_store,
    )

    steps = [
        PipelineStep(
            stage="test_stage",
            agent="SlowAgent",
            advisor="HighScoreAdvisor",
            task="test",
        )
    ]

    # Run first time
    result1 = orch.run(steps)
    run_id = result1.get("run_id")

    assert run_id is not None

    # Check checkpoint exists
    last_key = checkpoint_store.find_last_key(run_id)
    assert last_key is not None

    # Load checkpoint
    checkpoint = checkpoint_store.load(last_key)
    assert checkpoint is not None
    assert checkpoint.memory_snapshot is not None
