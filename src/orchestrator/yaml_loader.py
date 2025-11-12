"""YAML pipeline loader with validation, dependencies, and policy support."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml

from .factory import CORE_ADVISORS, CORE_AGENTS
from .runner import PipelineStep


class PipelineValidationError(Exception):
    """Raised when pipeline YAML validation fails."""

    pass


@dataclass
class Policy:
    """Policy configuration for pipeline execution."""

    version: int = 1  # Policy version for compatibility checking
    score_thresholds: Dict[str, float] = field(default_factory=dict)  # category -> min score
    advisors: Dict[str, Dict[str, Any]] = field(default_factory=dict)  # category -> advisor config
    timeouts: Dict[str, float] = field(default_factory=dict)  # category -> seconds
    retries: Dict[str, int] = field(default_factory=dict)  # category -> max retries
    budget: Optional[Dict[str, Any]] = None  # Budget configuration


class YAMLPipelineLoader:
    """Loads a pipeline from YAML with validation and dependency resolution."""

    def __init__(
        self,
        agent_registry: Optional[Dict[str, Any]] = None,
        advisor_registry: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Initialize loader with agent and advisor registries for validation.

        Args:
            agent_registry: Dict mapping agent names to classes/types (defaults to CORE_AGENTS)
            advisor_registry: Dict mapping advisor names to classes/types (defaults to CORE_ADVISORS)
        """
        self.agent_registry = agent_registry or CORE_AGENTS
        self.advisor_registry = advisor_registry or CORE_ADVISORS

    def load(self, yaml_content: str) -> Tuple[List[PipelineStep], Policy]:
        """
        Load pipeline from YAML string with dependencies and policy.

        Returns:
            Tuple of (steps in topological order, policy)
        """
        data = yaml.safe_load(yaml_content)
        if not data:
            raise PipelineValidationError("Empty YAML content")

        # Extract policy
        policy_section = data.get("policy") or {}
        policy_version = policy_section.get("version", 1)

        # Validate policy version
        if policy_version != 1:
            raise PipelineValidationError(
                f"Unsupported policy.version={policy_version}. Only version 1 is supported."
            )

        policy_data = policy_section.get("score_thresholds", {})
        advisors_data = policy_section.get("advisors", {})
        timeouts_data = policy_section.get("timeouts", {})
        retries_data = policy_section.get("retries", {})
        budget_data = policy_section.get("budget")

        # Convert advisors config to dict format
        advisors_dict: Dict[str, Dict[str, Any]] = {}
        for cat, cfg in advisors_data.items():
            if isinstance(cfg, dict):
                advisors_dict[str(cat)] = {
                    "decision": cfg.get("decision", "majority"),
                    "list": cfg.get("list", []),
                    "weights": cfg.get("weights"),  # Optional weights
                }

        policy = Policy(
            version=policy_version,
            score_thresholds={str(k): float(v) for k, v in policy_data.items()},
            advisors=advisors_dict,
            timeouts={str(k): float(v) for k, v in timeouts_data.items()},
            retries={str(k): int(v) for k, v in retries_data.items()},
            budget=budget_data if budget_data else None,
        )

        stages = data.get("stages") or []
        if not stages:
            raise PipelineValidationError("No stages defined in YAML")

        # Validate names unique and required fields
        names: Set[str] = set()
        stage_by_name: Dict[str, Dict[str, Any]] = {}

        for s in stages:
            name = s.get("name")
            if not name:
                raise PipelineValidationError("Stage missing 'name' field")
            if name in names:
                raise PipelineValidationError(f"Duplicate stage name: {name}")
            names.add(name)

            # Validate agent/advisor
            agent_name = s.get("agent")
            advisor_name = s.get("advisor")

            if not agent_name:
                raise PipelineValidationError(f"Stage '{name}': missing 'agent' field")
            if not advisor_name:
                raise PipelineValidationError(f"Stage '{name}': missing 'advisor' field")

            if agent_name not in self.agent_registry:
                raise PipelineValidationError(
                    f"Stage '{name}': agent '{agent_name}' not registered"
                )
            if advisor_name not in self.advisor_registry:
                raise PipelineValidationError(
                    f"Stage '{name}': advisor '{advisor_name}' not registered"
                )

            stage_by_name[name] = s

        # Build dependency graph and resolve topological order
        graph: Dict[str, List[str]] = {name: [] for name in names}
        indeg: Dict[str, int] = {name: 0 for name in names}

        for s in stages:
            name = s["name"]
            deps = s.get("depends_on") or []
            if not isinstance(deps, list):
                raise PipelineValidationError(f"Stage '{name}': 'depends_on' must be a list")

            for d in deps:
                if d not in names:
                    raise PipelineValidationError(f"Stage '{name}': unknown dependency '{d}'")
                graph[d].append(name)
                indeg[name] += 1

        # Topological sort
        order: List[str] = []
        queue = [n for n, deg in indeg.items() if deg == 0]

        while queue:
            n = queue.pop(0)
            order.append(n)
            for v in graph[n]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    queue.append(v)

        if len(order) != len(stages):
            raise PipelineValidationError("Cyclic dependency detected in stages")

        # Build PipelineStep list in topological order
        steps: List[PipelineStep] = []
        for n in order:
            s = stage_by_name[n]
            step = PipelineStep(
                stage=s["name"],
                agent=s["agent"],
                advisor=s["advisor"],
                task=str(s.get("task", "")),
                max_retries=int(s.get("max_retries", 1)),
                category=s.get("category"),  # Store category for policy lookup
            )
            steps.append(step)

        return steps, policy

    def load_from_file(self, filepath: str) -> Tuple[List[PipelineStep], Policy]:
        """Load pipeline from YAML file."""
        with open(filepath, encoding="utf-8") as f:
            return self.load(f.read())
