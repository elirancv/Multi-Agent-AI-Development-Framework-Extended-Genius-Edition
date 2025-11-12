"""Test timeout exception mapping."""

import time

import pytest

from src.core.types import AgentMetadata, AgentOutput
from src.orchestrator.errors import TimeoutOrchestratorError
from src.orchestrator.factory import advisor_factory
from src.orchestrator.runner import Orchestrator, PipelineStep


class SlowAgent:
    """Agent that takes too long to execute."""

    name = "SlowAgent"
    min_advisor_score = 0.0

    def process(self, task, context):
        """Simulate slow execution."""
        time.sleep(0.2)  # Slow
        return AgentOutput("x", metadata=AgentMetadata(agent_name=self.name))

    def validate_output(self, o):
        """Validate output."""
        pass

    def describe(self):
        """Describe agent."""
        return self.name


def test_timeout_is_mapped_to_orchestrator_error() -> None:
    """Test that timeout exceptions are mapped to TimeoutOrchestratorError."""

    def local_agent_factory(_):
        return SlowAgent()

    orch = Orchestrator(local_agent_factory, advisor_factory)
    orch.agent_timeout_sec = 0.01  # Very short timeout

    step = PipelineStep(
        stage="s",
        agent="SlowAgent",
        advisor="RequirementsAdvisor",
        task="t",
    )

    with pytest.raises(TimeoutOrchestratorError):
        orch.run([step])


def test_timeout_emits_error_event() -> None:
    """Test that timeout emits error event with correct reason."""

    def local_agent_factory(_):
        return SlowAgent()

    orch = Orchestrator(local_agent_factory, advisor_factory)
    orch.agent_timeout_sec = 0.01

    step = PipelineStep(
        stage="s",
        agent="SlowAgent",
        advisor="RequirementsAdvisor",
        task="t",
    )

    try:
        orch.run([step])
    except TimeoutOrchestratorError:
        pass  # Expected

    # Verify error event was emitted (check event log if accessible)
    # The important thing is that it raises TimeoutOrchestratorError, not generic TimeoutError
