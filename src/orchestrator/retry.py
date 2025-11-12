"""Retry utilities with backoff and jitter."""

from __future__ import annotations

import random
import time
from dataclasses import dataclass
from typing import Callable, TypeVar

T = TypeVar("T")


@dataclass
class BackoffPolicy:
    """Retry policy with exponential backoff and jitter."""

    max_attempts: int = 3
    base: float = 0.25  # seconds
    factor: float = 2.0
    jitter: float = 0.20  # 20%

    def sleep(self, attempt: int) -> None:
        """
        Sleep with exponential backoff and jitter.

        Args:
            attempt: Current attempt number (1-indexed)
        """
        delay = self.base * (self.factor ** max(0, attempt - 1))
        jitter_amount = delay * self.jitter * (2 * random.random() - 1.0)
        time.sleep(max(0.0, delay + jitter_amount))


def retry(policy: BackoffPolicy, fn: Callable[[], T]) -> T:
    """
    Retry a callable with backoff policy.

    Args:
        policy: Backoff policy configuration
        fn: Callable to retry

    Returns:
        Result of fn()

    Raises:
        Exception: Last exception if all attempts fail
    """
    last_exc: Exception | None = None
    for attempt in range(1, policy.max_attempts + 1):
        try:
            return fn()
        except Exception as e:
            last_exc = e
            if attempt == policy.max_attempts:
                raise
            policy.sleep(attempt)

    assert False, "unreachable"
