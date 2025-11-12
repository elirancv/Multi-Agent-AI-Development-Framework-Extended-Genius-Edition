"""Test timeout utilities."""

import time

import pytest

from src.orchestrator.timeout import run_with_timeout


def test_timeout_raises() -> None:
    """Test that timeout raises TimeoutError when exceeded."""

    def slow() -> str:
        time.sleep(0.2)
        return "ok"

    with pytest.raises(TimeoutError):
        run_with_timeout(slow, 0.05)


def test_timeout_succeeds_within_limit() -> None:
    """Test that timeout succeeds when operation completes in time."""

    def fast() -> str:
        return "ok"

    result = run_with_timeout(fast, 1.0)
    assert result == "ok"


def test_timeout_with_computation() -> None:
    """Test timeout with actual computation."""

    def compute() -> int:
        total = 0
        for i in range(1000):
            total += i
        return total

    result = run_with_timeout(compute, 1.0)
    assert result == sum(range(1000))
