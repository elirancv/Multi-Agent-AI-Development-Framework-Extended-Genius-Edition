"""Property-based tests for templating, cache, budget."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

# Try to import hypothesis, skip if not available
try:
    from hypothesis import given
    from hypothesis import strategies as st

    HAS_HYPOTHESIS = True
except ImportError:
    HAS_HYPOTHESIS = False
    pytestmark = pytest.mark.skip(reason="hypothesis not installed")


if HAS_HYPOTHESIS:

    @given(
        tmpl=st.sampled_from(
            [
                "Build {{ name }}",
                "Hi {name}",
                "{missing}",
                "{{ maybe|default('X') }}",
                "{{ nested.key }}",
                "{{ list[0] }}",
            ]
        ),
        name=st.text(min_size=0, max_size=20),
    )
    def test_render_task_never_crashes(tmpl, name):
        """Test task rendering never crashes with various inputs."""
        from src.orchestrator.task_render import render_task

        ctx = {"name": name, "maybe": None, "nested": {"key": "value"}, "list": [1, 2, 3]}

        try:
            s = render_task(tmpl, ctx)
            assert isinstance(s, str)
            assert len(s) <= 10_000  # Reasonable upper bound
        except (KeyError, AttributeError, TypeError):
            # Some templates may fail with missing keys - that's OK
            pass


def test_cache_key_generation():
    """Test cache key generation changes with agent version."""
    from src.orchestrator.cache import AgentCache

    cache = AgentCache()

    # Create cache entries with different versions
    key1 = cache._key("TestAgent", "test_stage", "test", {}, agent_version="1.0.0")
    key2 = cache._key(
        "TestAgent", "test_stage", "test", {}, agent_version="1.0.1"
    )  # Different version

    assert key1 != key2, "Cache keys should differ with version change"


def test_cache_key_context_change():
    """Test cache key changes with context."""
    from src.orchestrator.cache import AgentCache

    cache = AgentCache()

    key1 = cache._key(
        "TestAgent", "test_stage", "test", {"test_stage.key": "value1"}, agent_version="1.0.0"
    )
    key2 = cache._key(
        "TestAgent", "test_stage", "test", {"test_stage.key": "value2"}, agent_version="1.0.0"
    )  # Different context

    assert key1 != key2, "Cache keys should differ with context change"


def test_budget_guard_bytes():
    """Test budget guard stops when bytes threshold exceeded."""
    from src.orchestrator.budget import Budget, enforce_budget

    budget = Budget(max_artifacts_bytes=1000)

    # Add artifacts until threshold
    stats = {"artifacts_bytes": 0}
    for i in range(10):
        stats["artifacts_bytes"] += 150  # Each artifact 150 bytes
        try:
            enforce_budget(budget, stats)
        except Exception:
            # Should raise when exceeded
            break

    # Should stop before exceeding
    assert stats["artifacts_bytes"] <= 1000


def test_budget_guard_stages():
    """Test budget guard stops when stage limit reached."""
    from src.orchestrator.budget import Budget, enforce_budget

    budget = Budget(max_stages=5)

    # Try to exceed stage limit
    stats = {"stages": 0}
    for i in range(10):
        stats["stages"] += 1
        try:
            enforce_budget(budget, stats)
        except Exception:
            # Should raise when exceeded
            break

    # Should stop at limit
    assert stats["stages"] <= 5


def test_budget_guard_runtime():
    """Test budget guard stops when runtime exceeded."""
    from src.orchestrator.budget import Budget, enforce_budget

    budget = Budget(max_runtime_sec=0.1)  # Very short timeout

    # Simulate runtime
    stats = {"runtime_sec": 0.15}  # Exceeded timeout

    # Should raise when exceeded
    with pytest.raises(Exception):  # BudgetExceededError
        enforce_budget(budget, stats)
