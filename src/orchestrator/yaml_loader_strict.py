"""Strict YAML loader with Pydantic validation."""

from __future__ import annotations

from typing import Dict, List, Tuple

import yaml

from .factory import CORE_ADVISORS, CORE_AGENTS
from .runner_parallel import PipelineStep
from .yaml_schema import PipelineModel


class YAMLPipelineLoaderStrict:
    """YAML loader with strict Pydantic validation."""

    def load(self, path: str) -> Tuple[List[PipelineStep], Dict[str, float]]:
        """
        Load pipeline from YAML file with strict validation.

        Args:
            path: Path to YAML file

        Returns:
            Tuple of (steps, score_thresholds dict)

        Raises:
            KeyError: If agent/advisor not registered
            ValueError: If validation fails
        """
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        # Validate with Pydantic
        model = PipelineModel(**data)

        # Validate agents/advisors exist
        for st in model.stages:
            if st.agent not in CORE_AGENTS:
                raise KeyError(f"Unknown agent: {st.agent}")
            if st.advisor not in CORE_ADVISORS:
                raise KeyError(f"Unknown advisor: {st.advisor}")

        # Convert to PipelineStep
        steps = [
            PipelineStep(
                stage=s.name,
                agent=s.agent,
                advisor=s.advisor,
                task=s.task,
                category=s.category,
                depends_on=s.depends_on,
                max_retries=s.max_retries,
            )
            for s in model.stages
        ]

        # Extract policy thresholds
        policy = model.policy.score_thresholds if model.policy else {}  # category -> threshold

        return steps, policy
