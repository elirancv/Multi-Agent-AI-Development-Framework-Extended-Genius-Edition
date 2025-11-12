"""Timeout utilities for safe agent/advisor execution."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from typing import Callable, TypeVar

T = TypeVar("T")

# Export FuturesTimeoutError for explicit catching
__all__ = ["run_with_timeout", "FutureTimeoutError"]


def run_with_timeout(fn: Callable[[], T], seconds: float) -> T:
    """
    Run a callable with a wall-clock timeout. Raises FutureTimeoutError if exceeded.

    Thread-based, so it won't kill C extensions, but unblocks orchestrator safely.

    Args:
        fn: Callable to execute
        seconds: Timeout in seconds

    Returns:
        Result of fn()

    Raises:
        FutureTimeoutError: If execution exceeds timeout
    """
    with ThreadPoolExecutor(max_workers=1) as ex:
        fut = ex.submit(fn)
        try:
            return fut.result(timeout=seconds)
        except FutureTimeoutError as e:
            raise FutureTimeoutError(f"Operation timed out after {seconds}s") from e

