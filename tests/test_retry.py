"""Test retry utilities."""

import pytest

from src.orchestrator.retry import BackoffPolicy, retry


def test_retry_succeeds_on_second_attempt() -> None:
    """Test that retry succeeds after initial failure."""

    calls = {"n": 0}

    def flaky() -> str:
        calls["n"] += 1
        if calls["n"] < 2:
            raise RuntimeError("boom")
        return "ok"

    assert retry(BackoffPolicy(max_attempts=3, base=0.01), flaky) == "ok"
    assert calls["n"] == 2


def test_retry_raises_after_max_attempts() -> None:
    """Test that retry raises after max attempts."""

    def always_fails() -> str:
        raise ValueError("always fails")

    with pytest.raises(ValueError, match="always fails"):
        retry(BackoffPolicy(max_attempts=2, base=0.01), always_fails)


def test_retry_succeeds_immediately() -> None:
    """Test that retry succeeds on first attempt."""

    def succeeds() -> str:
        return "ok"

    result = retry(BackoffPolicy(max_attempts=3, base=0.01), succeeds)
    assert result == "ok"


def test_backoff_policy_sleep() -> None:
    """Test that backoff policy sleeps correctly."""
    import time

    policy = BackoffPolicy(max_attempts=3, base=0.1, factor=2.0, jitter=0.0)

    start = time.time()
    policy.sleep(1)
    elapsed = time.time() - start

    # Should sleep approximately base * factor^(attempt-1) = 0.1 * 2^0 = 0.1
    assert 0.09 <= elapsed <= 0.15
