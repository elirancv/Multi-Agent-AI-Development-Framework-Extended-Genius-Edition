"""Dry-run validation for pipelines."""

from __future__ import annotations

from typing import List, Tuple

from .yaml_loader import YAMLPipelineLoader


def validate_pipeline_file(path: str) -> Tuple[int, List[str]]:
    """
    Validate pipeline YAML for structure & registries.

    Args:
        path: Path to pipeline YAML file

    Returns:
        Tuple of (number_of_stages, list_of_stage_names)

    Raises:
        PipelineValidationError: If validation fails
    """
    steps, policy = YAMLPipelineLoader().load_from_file(path)
    names = [s.stage for s in steps]
    return (len(names), names)
