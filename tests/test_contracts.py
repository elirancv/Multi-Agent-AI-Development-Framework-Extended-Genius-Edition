"""Test agent output contracts."""

from src.core.types import Artifact, AgentMetadata, AgentOutput


def test_agent_output_contract() -> None:
    """Test that AgentOutput follows the required contract."""
    meta = AgentMetadata(agent_name="X")
    art = Artifact(name="file.md", type="markdown", content="# Hello")
    out = AgentOutput(content="ok", artifacts=[art], metadata=meta)

    as_dict = out.to_dict()

    assert "content" in as_dict and isinstance(as_dict["content"], str)
    assert (
        isinstance(as_dict["artifacts"], list)
        and as_dict["artifacts"][0]["name"] == "file.md"
    )
    assert as_dict["metadata"]["agent_name"] == "X"

