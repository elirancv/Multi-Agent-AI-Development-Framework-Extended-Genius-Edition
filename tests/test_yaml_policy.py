"""Test YAML loader with policy and dependencies."""

import pytest
from src.orchestrator.yaml_loader import (
    YAMLPipelineLoader,
    PipelineValidationError,
    Policy,
)
from src.orchestrator.factory import CORE_AGENTS, CORE_ADVISORS


def test_load_policy() -> None:
    """Test loading pipeline with policy thresholds."""
    yaml_content = """
policy:
  score_thresholds:
    requirements: 0.80
    codegen: 0.90

stages:
  - name: requirements
    category: requirements
    agent: RequirementsDraftingAgent
    advisor: RequirementsAdvisor
    task: "Test"
"""
    loader = YAMLPipelineLoader()
    steps, policy = loader.load(yaml_content)

    assert len(steps) == 1
    assert steps[0].category == "requirements"
    assert policy.score_thresholds["requirements"] == 0.80
    assert policy.score_thresholds["codegen"] == 0.90


def test_load_dependencies() -> None:
    """Test loading pipeline with dependencies."""
    yaml_content = """
stages:
  - name: step1
    agent: RequirementsDraftingAgent
    advisor: RequirementsAdvisor
    task: "First"

  - name: step2
    depends_on: [step1]
    agent: PromptRefinerAgent
    advisor: PromptRefinerAdvisor
    task: "Second"
"""
    loader = YAMLPipelineLoader()
    steps, _ = loader.load(yaml_content)

    assert len(steps) == 2
    assert steps[0].stage == "step1"
    assert steps[1].stage == "step2"


def test_cyclic_dependency() -> None:
    """Test that cyclic dependencies are detected."""
    yaml_content = """
stages:
  - name: step1
    depends_on: [step2]
    agent: RequirementsDraftingAgent
    advisor: RequirementsAdvisor
    task: "First"

  - name: step2
    depends_on: [step1]
    agent: PromptRefinerAgent
    advisor: PromptRefinerAdvisor
    task: "Second"
"""
    loader = YAMLPipelineLoader()

    with pytest.raises(PipelineValidationError, match="Cyclic"):
        loader.load(yaml_content)


def test_unknown_dependency() -> None:
    """Test that unknown dependencies are detected."""
    yaml_content = """
stages:
  - name: step1
    depends_on: [nonexistent]
    agent: RequirementsDraftingAgent
    advisor: RequirementsAdvisor
    task: "First"
"""
    loader = YAMLPipelineLoader()

    with pytest.raises(PipelineValidationError, match="unknown dependency"):
        loader.load(yaml_content)

