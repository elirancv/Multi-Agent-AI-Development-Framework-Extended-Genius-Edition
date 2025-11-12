"""Test strict YAML loader with Pydantic validation."""

import pytest

from src.orchestrator.yaml_loader_strict import YAMLPipelineLoaderStrict


def test_load_valid_pipeline() -> None:
    """Test loading a valid pipeline with strict validation."""
    loader = YAMLPipelineLoaderStrict()
    steps, policy = loader.load("pipeline/example.yaml")

    assert len(steps) > 0
    assert isinstance(policy, dict)


def test_validate_unique_stage_names() -> None:
    """Test that duplicate stage names are rejected."""
    import tempfile

    import yaml

    invalid_yaml = {
        "stages": [
            {
                "name": "duplicate",
                "agent": "RequirementsDraftingAgent",
                "advisor": "RequirementsAdvisor",
                "task": "Test 1",
            },
            {
                "name": "duplicate",
                "agent": "RequirementsDraftingAgent",
                "advisor": "RequirementsAdvisor",
                "task": "Test 2",
            },
        ]
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(invalid_yaml, f)
        temp_path = f.name

    try:
        loader = YAMLPipelineLoaderStrict()
        with pytest.raises(ValueError, match="unique"):
            loader.load(temp_path)
    finally:
        import os

        os.unlink(temp_path)


def test_validate_max_retries_non_negative() -> None:
    """Test that negative max_retries is rejected."""
    import tempfile

    import yaml

    invalid_yaml = {
        "stages": [
            {
                "name": "test",
                "agent": "RequirementsDraftingAgent",
                "advisor": "RequirementsAdvisor",
                "task": "Test",
                "max_retries": -1,
            }
        ]
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(invalid_yaml, f)
        temp_path = f.name

    try:
        loader = YAMLPipelineLoaderStrict()
        with pytest.raises(ValueError, match=">= 0"):
            loader.load(temp_path)
    finally:
        import os

        os.unlink(temp_path)
