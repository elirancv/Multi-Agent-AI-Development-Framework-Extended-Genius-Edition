"""Tests for budget enforcement."""

import pytest

from src.orchestrator.budget import Budget, BudgetExceededError, enforce_budget


def test_budget_no_limits():
    """Test that budget with no limits doesn't raise."""
    budget = Budget()
    stats = {"stages": 10, "artifacts_bytes": 1000, "runtime_sec": 50.0}
    enforce_budget(budget, stats)  # Should not raise


def test_budget_stages_exceeded():
    """Test that exceeding stage budget raises error."""
    budget = Budget(max_stages=5)
    stats = {"stages": 10, "artifacts_bytes": 1000, "runtime_sec": 50.0}

    with pytest.raises(BudgetExceededError, match="Stage budget exceeded"):
        enforce_budget(budget, stats)


def test_budget_artifacts_exceeded():
    """Test that exceeding artifacts budget raises error."""
    budget = Budget(max_artifacts_bytes=1000)
    stats = {"stages": 5, "artifacts_bytes": 2000, "runtime_sec": 50.0}

    with pytest.raises(BudgetExceededError, match="Artifacts size budget exceeded"):
        enforce_budget(budget, stats)


def test_budget_runtime_exceeded():
    """Test that exceeding runtime budget raises error."""
    budget = Budget(max_runtime_sec=30.0)
    stats = {"stages": 5, "artifacts_bytes": 1000, "runtime_sec": 60.0}

    with pytest.raises(BudgetExceededError, match="Runtime budget exceeded"):
        enforce_budget(budget, stats)


def test_budget_within_limits():
    """Test that stats within limits don't raise."""
    budget = Budget(max_stages=10, max_artifacts_bytes=5000, max_runtime_sec=100.0)
    stats = {"stages": 5, "artifacts_bytes": 2000, "runtime_sec": 50.0}
    enforce_budget(budget, stats)  # Should not raise
