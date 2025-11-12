"""Test pipeline graph generation."""

import pytest

from src.orchestrator.graph import GRAPHVIZ_AVAILABLE, pipeline_to_dot
from src.orchestrator.runner_parallel import PipelineStep


@pytest.mark.skipif(not GRAPHVIZ_AVAILABLE, reason="graphviz not installed")
def test_pipeline_to_dot() -> None:
    """Test generating DOT graph from pipeline steps."""
    steps = [
        PipelineStep(
            stage="stage1",
            agent="Agent1",
            advisor="Advisor1",
            task="task1",
            category="cat1",
        ),
        PipelineStep(
            stage="stage2",
            agent="Agent2",
            advisor="Advisor2",
            task="task2",
            depends_on=["stage1"],
        ),
    ]

    dot = pipeline_to_dot(steps)

    # Verify graph structure
    # dot.body is a list of strings, so check in the source string instead
    source_str = str(dot.source)
    assert "stage1" in source_str
    assert "stage2" in source_str
    assert "stage1 -> stage2" in source_str or "stage2 -> stage1" in source_str


def test_pipeline_to_dot_requires_graphviz() -> None:
    """Test that graph generation requires graphviz."""
    if not GRAPHVIZ_AVAILABLE:
        steps = [PipelineStep(stage="stage1", agent="Agent1", advisor="Advisor1", task="task1")]
        with pytest.raises(ImportError, match="graphviz"):
            pipeline_to_dot(steps)
