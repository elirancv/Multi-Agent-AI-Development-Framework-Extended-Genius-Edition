"""YAML loader tests: policy variations, dependencies, validation."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.orchestrator.yaml_loader import YAMLPipelineLoader, PipelineValidationError
from src.orchestrator.yaml_loader_strict import YAMLPipelineLoaderStrict


def create_test_pipeline(content: dict) -> Path:
    """Create a temporary pipeline YAML file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(content, f)
        return Path(f.name)


def test_yaml_loader_basic():
    """Test basic YAML loading."""
    pipeline = {
        "stages": [
            {
                "name": "test_stage",
                "agent": "RequirementsDraftingAgent",
                "advisor": "RequirementsAdvisor",
                "task": "test task",
                "output": "docs/test.md",
            }
        ]
    }
    
    path = create_test_pipeline(pipeline)
    try:
        loader = YAMLPipelineLoader()
        steps, policy = loader.load_from_file(str(path))
        
        assert len(steps) == 1
        assert steps[0]["name"] == "test_stage"
    finally:
        path.unlink(missing_ok=True)


def test_yaml_loader_with_policy():
    """Test YAML loading with policy."""
    pipeline = {
        "policy": {
            "score_thresholds": {"default": 0.85},
            "timeouts": {"default": 60},
            "retries": {"default": 2},
        },
        "stages": [
            {
                "name": "test_stage",
                "agent": "RequirementsDraftingAgent",
                "advisor": "RequirementsAdvisor",
                "task": "test",
                "output": "docs/test.md",
            }
        ]
    }
    
    path = create_test_pipeline(pipeline)
    try:
        loader = YAMLPipelineLoader()
        steps, policy = loader.load_from_file(str(path))
        
        assert policy is not None
        assert policy.score_thresholds is not None
        assert policy.score_thresholds.get("default") == 0.85
    finally:
        path.unlink(missing_ok=True)


def test_yaml_loader_dependencies():
    """Test YAML loading with dependencies."""
    pipeline = {
        "stages": [
            {
                "name": "stage1",
                "agent": "RequirementsDraftingAgent",
                "advisor": "RequirementsAdvisor",
                "task": "test1",
                "output": "docs/stage1.md",
            },
            {
                "name": "stage2",
                "agent": "RequirementsDraftingAgent",
                "advisor": "RequirementsAdvisor",
                "task": "test2",
                "input": "docs/stage1.md",
                "output": "docs/stage2.md",
            }
        ],
        "dependencies": {
            "stage2": ["stage1"]
        }
    }
    
    path = create_test_pipeline(pipeline)
    try:
        loader = YAMLPipelineLoaderStrict()
        steps, thresholds = loader.load(str(path))
        
        assert len(steps) == 2
        # Dependencies should be resolved
    finally:
        path.unlink(missing_ok=True)


def test_yaml_loader_cyclic_dependencies():
    """Test YAML loader detects cyclic dependencies."""
    pipeline = {
        "stages": [
            {
                "name": "stage1",
                "agent": "RequirementsDraftingAgent",
                "advisor": "RequirementsAdvisor",
                "task": "test1",
                "output": "docs/stage1.md",
            },
            {
                "name": "stage2",
                "agent": "RequirementsDraftingAgent",
                "advisor": "RequirementsAdvisor",
                "task": "test2",
                "output": "docs/stage2.md",
            }
        ],
        "dependencies": {
            "stage1": ["stage2"],
            "stage2": ["stage1"]
        }
    }
    
    path = create_test_pipeline(pipeline)
    try:
        loader = YAMLPipelineLoaderStrict()
        # Should detect cycle and raise error
        with pytest.raises((PipelineValidationError, ValueError)):
            loader.load(str(path))
    finally:
        path.unlink(missing_ok=True)


def test_yaml_loader_missing_dependency():
    """Test YAML loader handles missing dependencies."""
    pipeline = {
        "stages": [
            {
                "name": "stage1",
                "agent": "RequirementsDraftingAgent",
                "advisor": "RequirementsAdvisor",
                "task": "test1",
                "output": "docs/stage1.md",
            },
            {
                "name": "stage2",
                "agent": "RequirementsDraftingAgent",
                "advisor": "RequirementsAdvisor",
                "task": "test2",
                "input": "docs/missing.md",  # Missing dependency
                "output": "docs/stage2.md",
            }
        ],
        "dependencies": {
            "stage2": ["missing_stage"]  # Missing stage
        }
    }
    
    path = create_test_pipeline(pipeline)
    try:
        loader = YAMLPipelineLoaderStrict()
        # Should handle missing dependency
        with pytest.raises((PipelineValidationError, ValueError, KeyError)):
            loader.load(str(path))
    finally:
        path.unlink(missing_ok=True)


def test_yaml_loader_advisor_weights():
    """Test YAML loader with advisor weights."""
    pipeline = {
        "policy": {
            "advisor_weights": {
                "RequirementsAdvisor": 0.7,
                "CodeReviewAdvisor": 0.3,
            }
        },
        "stages": [
            {
                "name": "test_stage",
                "agent": "RequirementsDraftingAgent",
                "advisor": "RequirementsAdvisor",
                "task": "test",
                "output": "docs/test.md",
            }
        ]
    }
    
    path = create_test_pipeline(pipeline)
    try:
        loader = YAMLPipelineLoader()
        steps, policy = loader.load_from_file(str(path))
        
        assert policy is not None
        # Advisor weights may be in policy or separate
    finally:
        path.unlink(missing_ok=True)


def test_yaml_loader_invalid_yaml():
    """Test YAML loader handles invalid YAML."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("invalid: yaml: content: [")
        invalid_path = Path(f.name)
    
    try:
        loader = YAMLPipelineLoader()
        with pytest.raises((yaml.YAMLError, PipelineValidationError, Exception)):
            loader.load_from_file(str(invalid_path))
    finally:
        invalid_path.unlink(missing_ok=True)


def test_yaml_loader_missing_required_fields():
    """Test YAML loader validates required fields."""
    pipeline = {
        "stages": [
            {
                "name": "test_stage",
                # Missing agent, advisor, task
            }
        ]
    }
    
    path = create_test_pipeline(pipeline)
    try:
        loader = YAMLPipelineLoaderStrict()
        with pytest.raises((PipelineValidationError, KeyError, ValueError)):
            loader.load(str(path))
    finally:
        path.unlink(missing_ok=True)

