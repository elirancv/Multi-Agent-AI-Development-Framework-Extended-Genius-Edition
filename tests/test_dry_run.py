"""Test dry-run validation."""

from pathlib import Path

import pytest

from src.orchestrator.dryrun import validate_pipeline_file
from src.orchestrator.yaml_loader import PipelineValidationError


def test_dry_run_validates(tmp_path: Path) -> None:
    """Test dry-run validates valid pipeline."""

    yaml_text = """
stages:
  - name: s1
    agent: RequirementsDraftingAgent
    advisor: RequirementsAdvisor
    task: "T"
"""
    p = tmp_path / "p.yaml"
    p.write_text(yaml_text, encoding="utf-8")

    n, names = validate_pipeline_file(str(p))
    assert n == 1
    assert names == ["s1"]


def test_dry_run_validates_multiple_stages(tmp_path: Path) -> None:
    """Test dry-run validates multiple stages."""

    yaml_text = """
stages:
  - name: s1
    agent: RequirementsDraftingAgent
    advisor: RequirementsAdvisor
    task: "T1"
  - name: s2
    agent: PromptRefinerAgent
    advisor: PromptRefinerAdvisor
    task: "T2"
    depends_on: [s1]
"""
    p = tmp_path / "p.yaml"
    p.write_text(yaml_text, encoding="utf-8")

    n, names = validate_pipeline_file(str(p))
    assert n == 2
    assert names == ["s1", "s2"]


def test_dry_run_raises_on_invalid(tmp_path: Path) -> None:
    """Test dry-run raises on invalid pipeline."""

    yaml_text = """
stages:
  - name: s1
    agent: UnknownAgent
    advisor: RequirementsAdvisor
    task: "T"
"""
    p = tmp_path / "p.yaml"
    p.write_text(yaml_text, encoding="utf-8")

    with pytest.raises(PipelineValidationError):
        validate_pipeline_file(str(p))
