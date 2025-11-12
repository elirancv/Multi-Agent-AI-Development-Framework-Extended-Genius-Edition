"""Pydantic schema for YAML pipeline validation."""

from __future__ import annotations

from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field, field_validator


class AdvisorConfigModel(BaseModel):
    """Advisor council configuration for a category."""

    decision: Literal["majority", "average"] = "majority"
    list: List[str] = Field(..., min_length=1)
    weights: Optional[Dict[str, float]] = Field(default=None)  # Optional advisor weights


class BudgetModel(BaseModel):
    """Budget configuration model."""

    max_runtime_sec: Optional[float] = Field(default=None, gt=0)
    max_stages: Optional[int] = Field(default=None, gt=0)
    max_artifacts_bytes: Optional[int] = Field(default=None, gt=0)


class PolicyModel(BaseModel):
    """Policy configuration model."""

    version: int = Field(default=1, ge=1, le=1)  # Only version 1 supported
    score_thresholds: Dict[str, float] = Field(default_factory=dict)
    advisors: Dict[str, AdvisorConfigModel] = Field(default_factory=dict)
    timeouts: Dict[str, float] = Field(default_factory=dict)
    retries: Dict[str, int] = Field(default_factory=dict)
    budget: Optional[BudgetModel] = None


class StageModel(BaseModel):
    """Stage configuration model."""

    name: str
    category: Optional[str] = None
    agent: str
    advisor: str
    task: str
    max_retries: int = 0
    depends_on: List[str] = Field(default_factory=list)

    @field_validator("max_retries")
    @classmethod
    def non_negative(cls, v: int) -> int:
        """Ensure max_retries is non-negative."""
        if v < 0:
            raise ValueError("max_retries must be >= 0")
        return v


class PipelineModel(BaseModel):
    """Complete pipeline configuration model."""

    project_mode: Optional[str] = None
    policy: Optional[PolicyModel] = None
    stages: List[StageModel]

    @field_validator("stages")
    @classmethod
    def unique_names(cls, v: List[StageModel]) -> List[StageModel]:
        """Ensure stage names are unique."""
        names = [s.name for s in v]
        if len(names) != len(set(names)):
            raise ValueError("Stage names must be unique")
        return v
