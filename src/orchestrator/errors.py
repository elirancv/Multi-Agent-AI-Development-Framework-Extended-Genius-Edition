"""Orchestrator error taxonomy with reason codes."""

from __future__ import annotations


class OrchestratorError(Exception):
    """Base orchestrator error with reason code."""

    reason: str = "unknown"

    def __init__(self, message: str = "", reason: str | None = None) -> None:
        """
        Initialize orchestrator error.

        Args:
            message: Error message
            reason: Reason code (defaults to class reason)
        """
        super().__init__(message)
        if reason:
            self.reason = reason


class TimeoutOrchestratorError(OrchestratorError):
    """Agent/advisor execution timeout."""

    reason = "timeout"


class InvalidOutputError(OrchestratorError):
    """Agent output validation failed."""

    reason = "invalid_output"


class AdvisorRejectError(OrchestratorError):
    """Advisor rejected agent output."""

    reason = "advisor_reject"


class ExhaustedRetriesError(OrchestratorError):
    """All retry attempts exhausted."""

    reason = "exhausted_retries"

