"""Test policy version validation."""

import pytest
import yaml

from src.orchestrator.yaml_loader import YAMLPipelineLoader, PipelineValidationError


def test_policy_version_defaults_to_1() -> None:
    """Test that policy version defaults to 1."""
    loader = YAMLPipelineLoader()
    yaml_content = """
stages:
  - name: test
    agent: RequirementsDraftingAgent
    advisor: RequirementsAdvisor
    task: "test"
"""
    steps, policy = loader.load(yaml_content)
    assert policy.version == 1


def test_policy_version_validation() -> None:
    """Test that unsupported policy versions are rejected."""
    loader = YAMLPipelineLoader()
    yaml_content = """
policy:
  version: 2
stages:
  - name: test
    agent: RequirementsDraftingAgent
    advisor: RequirementsAdvisor
    task: "test"
"""
    with pytest.raises(PipelineValidationError, match="Unsupported policy.version"):
        loader.load(yaml_content)


def test_policy_version_1_accepted() -> None:
    """Test that policy version 1 is accepted."""
    loader = YAMLPipelineLoader()
    yaml_content = """
policy:
  version: 1
  score_thresholds:
    requirements: 0.85
stages:
  - name: test
    agent: RequirementsDraftingAgent
    advisor: RequirementsAdvisor
    task: "test"
"""
    steps, policy = loader.load(yaml_content)
    assert policy.version == 1
    assert policy.score_thresholds["requirements"] == 0.85

