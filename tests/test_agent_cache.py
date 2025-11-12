"""Test agent cache."""

from src.orchestrator.cache import AgentCache


def test_cache_roundtrip() -> None:
    """Test cache put and get."""

    c = AgentCache()
    ctx = {"requirements.content": "X"}

    c.put(
        "A",
        "S",
        "T",
        ctx,
        {"content": "ok", "artifacts": [], "metadata": {"agent_name": "A"}},
    )

    result = c.get("A", "S", "T", ctx)
    assert result is not None
    assert result["content"] == "ok"


def test_cache_miss_on_different_context() -> None:
    """Test that cache misses on different context."""

    c = AgentCache()
    # Use stage name that matches context key prefix
    ctx1 = {"s1.content": "X"}
    ctx2 = {"s1.content": "Y"}

    c.put("A", "s1", "T", ctx1, {"content": "ok"})

    assert c.get("A", "s1", "T", ctx1) is not None
    assert c.get("A", "s1", "T", ctx2) is None


def test_cache_miss_on_different_task() -> None:
    """Test that cache misses on different task."""

    c = AgentCache()
    ctx = {"requirements.content": "X"}

    c.put("A", "S", "T1", ctx, {"content": "ok"})

    assert c.get("A", "S", "T1", ctx) is not None
    assert c.get("A", "S", "T2", ctx) is None


def test_cache_filters_context() -> None:
    """Test that cache only uses stage-related context keys."""

    c = AgentCache()
    ctx_full = {
        "requirements.content": "X",
        "other_stage.content": "Y",
        "global_key": "Z",
    }
    ctx_filtered = {"requirements.content": "X"}

    c.put("A", "requirements", "T", ctx_full, {"content": "ok"})

    # Should match because cache filters to stage-related keys
    result = c.get("A", "requirements", "T", ctx_filtered)
    assert result is not None
    assert result["content"] == "ok"
