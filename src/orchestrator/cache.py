"""Agent output cache by input signature."""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict


class AgentCache:
    """In-memory cache for agent outputs by input signature."""

    def __init__(self) -> None:
        """Initialize empty cache."""
        self._store: Dict[str, Dict[str, Any]] = {}

    @staticmethod
    def _key(
        agent: str,
        stage: str,
        task: str,
        context: Dict[str, Any],
        agent_version: str = "0.1.0",
    ) -> str:
        """
        Generate cache key from agent, stage, task, context, and agent version.

        Args:
            agent: Agent name
            stage: Stage name
            task: Task string
            context: Context dictionary
            agent_version: Agent version (default: "0.1.0")

        Returns:
            SHA256 hash of normalized input
        """
        # Keep context small: stage-related keys only
        ctx_light = {k: v for k, v in context.items() if k.startswith(f"{stage}.")}
        raw = json.dumps(
            {"a": agent, "v": agent_version, "s": stage, "t": task, "c": ctx_light},
            sort_keys=True,
            default=str,
        )
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def get(
        self,
        agent: str,
        stage: str,
        task: str,
        context: Dict[str, Any],
        agent_version: str = "0.1.0",
    ) -> Dict[str, Any] | None:
        """
        Get cached output if available.

        Args:
            agent: Agent name
            stage: Stage name
            task: Task string
            context: Context dictionary
            agent_version: Agent version (default: "0.1.0")

        Returns:
            Cached output dict or None
        """
        return self._store.get(self._key(agent, stage, task, context, agent_version))

    def put(
        self,
        agent: str,
        stage: str,
        task: str,
        context: Dict[str, Any],
        agent_output_dict: Dict[str, Any],
        agent_version: str = "0.1.0",
    ) -> None:
        """
        Store agent output in cache.

        Args:
            agent: Agent name
            stage: Stage name
            task: Task string
            context: Context dictionary
            agent_output_dict: Agent output as dictionary
            agent_version: Agent version (default: "0.1.0")
        """
        self._store[self._key(agent, stage, task, context, agent_version)] = agent_output_dict
