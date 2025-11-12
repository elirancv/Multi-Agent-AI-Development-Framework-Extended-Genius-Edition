"""Test cache version invalidation."""

from src.orchestrator.cache import AgentCache


def test_cache_key_includes_version() -> None:
    """Test that cache key includes agent version."""
    cache = AgentCache()

    key1 = cache._key("Agent", "stage", "task", {}, agent_version="0.1.0")
    key2 = cache._key("Agent", "stage", "task", {}, agent_version="0.2.0")

    # Different versions should produce different keys
    assert key1 != key2


def test_cache_separates_by_version() -> None:
    """Test that cache separates entries by version."""
    cache = AgentCache()

    output_v1 = {"content": "v1", "artifacts": []}
    output_v2 = {"content": "v2", "artifacts": []}

    cache.put("Agent", "stage", "task", {}, output_v1, agent_version="0.1.0")
    cache.put("Agent", "stage", "task", {}, output_v2, agent_version="0.2.0")

    # Should retrieve correct version
    assert cache.get("Agent", "stage", "task", {}, agent_version="0.1.0") == output_v1
    assert cache.get("Agent", "stage", "task", {}, agent_version="0.2.0") == output_v2

