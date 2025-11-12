# Copyright (c) 2025 Multi-Agent AI Development Framework Contributors
# Licensed under the MIT License

"""Type definitions and data structures for agent contracts."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, TypedDict, Literal
import json

ArtifactType = Literal["text", "markdown", "json", "python", "binary", "image"]


@dataclass
class Artifact:
    """Represents a produced artifact by an agent (code, doc, etc.)."""

    name: str
    type: ArtifactType
    content: Any
    description: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "name": self.name,
            "type": self.type,
            "content": self.content,
        }
        if self.description:
            payload["description"] = self.description
        return payload


@dataclass
class AgentMetadata:
    """Operational/trace metadata attached to agent outputs."""

    agent_name: str
    version: str = "0.1.0"
    stage: Optional[str] = None
    input_summary: Optional[str] = None
    timing_ms: Optional[int] = None
    retries: int = 0
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        base = asdict(self)
        # Ensure JSON-serializable
        try:
            json.dumps(base)
        except Exception:
            base["extra"] = {k: str(v) for k, v in self.extra.items()}
        return base


@dataclass
class AgentOutput:
    """
    Canonical structured output for every agent:
    - content: primary human-readable content
    - artifacts: machine-usable assets (code/files/specs)
    - metadata: trace info
    """

    content: str
    artifacts: List[Artifact] = field(default_factory=list)
    metadata: AgentMetadata = field(
        default_factory=lambda: AgentMetadata(agent_name="unknown")
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "artifacts": [a.to_dict() for a in self.artifacts],
            "metadata": self.metadata.to_dict(),
        }


class AdvisorReview(TypedDict):
    """Advisor review contract (as requested)."""

    score: float  # 0.0 - 1.0
    approved: bool
    critical_issues: List[str]
    suggestions: List[str]
    summary: str
    severity: Literal["low", "medium", "high", "critical"]

