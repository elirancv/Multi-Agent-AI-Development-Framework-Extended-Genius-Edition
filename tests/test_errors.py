"""Test orchestrator error taxonomy."""

from src.orchestrator.errors import (
    OrchestratorError,
    TimeoutOrchestratorError,
    InvalidOutputError,
    AdvisorRejectError,
    ExhaustedRetriesError,
)


def test_error_reasons() -> None:
    """Test that errors have correct reason codes."""

    assert TimeoutOrchestratorError.reason == "timeout"
    assert InvalidOutputError.reason == "invalid_output"
    assert AdvisorRejectError.reason == "advisor_reject"
    assert ExhaustedRetriesError.reason == "exhausted_retries"


def test_error_inheritance() -> None:
    """Test error inheritance."""

    assert issubclass(TimeoutOrchestratorError, OrchestratorError)
    assert issubclass(InvalidOutputError, OrchestratorError)


def test_error_instantiation() -> None:
    """Test error instantiation with custom message."""

    error = TimeoutOrchestratorError("Custom timeout message")
    assert str(error) == "Custom timeout message"
    assert error.reason == "timeout"

