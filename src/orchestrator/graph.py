"""Pipeline graph visualization."""

from __future__ import annotations

from typing import List

try:
    from graphviz import Digraph

    GRAPHVIZ_AVAILABLE = True
except ImportError:
    GRAPHVIZ_AVAILABLE = False

from .runner_parallel import PipelineStep


def pipeline_to_dot(steps: List[PipelineStep]) -> Digraph:
    """
    Generate Graphviz DOT graph from pipeline steps.

    Args:
        steps: List of pipeline steps

    Returns:
        Digraph object

    Raises:
        ImportError: If graphviz is not installed
    """
    if not GRAPHVIZ_AVAILABLE:
        raise ImportError(
            "graphviz is required for graph export. Install with: pip install graphviz"
        )

    g = Digraph("pipeline", graph_attr={"rankdir": "LR"})

    # Add nodes
    for s in steps:
        label = f"{s.stage}\n({s.category or 'default'})"
        g.node(s.stage, label=label)

    # Add edges from dependencies
    for s in steps:
        deps = getattr(s, "depends_on", []) or []
        for dep in deps:
            g.edge(dep, s.stage)

    return g
