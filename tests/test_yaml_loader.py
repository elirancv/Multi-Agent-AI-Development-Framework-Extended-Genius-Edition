"""Test YAML pipeline loader."""

import pytest
from src.orchestrator.yaml_loader import YAMLPipelineLoader, PipelineValidationError


def test_load_valid_pipeline() -> None:
    """Test loading a valid pipeline YAML."""
    yaml_content = """
stages:
  - name: requirements
    agent: RequirementsDraftingAgent
    advisor: RequirementsAdvisor
    task: "Create PRD for: {product_idea}"
    max_retries: 1
"""
    loader = YAMLPipelineLoader()
    steps, _ = loader.load(yaml_content)

    assert len(steps) == 1
    assert steps[0].stage == "requirements"
    assert steps[0].agent == "RequirementsDraftingAgent"
    assert steps[0].advisor == "RequirementsAdvisor"


def test_load_missing_agent() -> None:
    """Test that missing agent raises validation error."""
    yaml_content = """
stages:
  - name: requirements
    agent: NonExistentAgent
    advisor: RequirementsAdvisor
    task: "Test"
"""
    loader = YAMLPipelineLoader()

    with pytest.raises(PipelineValidationError, match="not registered"):
        loader.load(yaml_content)


def test_load_missing_advisor() -> None:
    """Test that missing advisor raises validation error."""
    yaml_content = """
stages:
  - name: requirements
    agent: RequirementsDraftingAgent
    advisor: NonExistentAdvisor
    task: "Test"
"""
    loader = YAMLPipelineLoader()

    with pytest.raises(PipelineValidationError, match="not registered"):
        loader.load(yaml_content)


def test_load_missing_required_fields() -> None:
    """Test that missing required fields raise validation error."""
    yaml_content = """
stages:
  - name: requirements
    agent: RequirementsDraftingAgent
"""
    loader = YAMLPipelineLoader()

    with pytest.raises(PipelineValidationError, match="missing"):
        loader.load(yaml_content)

