"""Factory functions for creating agents and advisors."""

from __future__ import annotations

from typing import Dict, Type
from src.core.base import BaseFunctionalAgent, BaseAdvisor
from src.agents.requirements_agent import RequirementsDraftingAgent
from src.agents.prompt_refiner_agent import PromptRefinerAgent
from src.agents.code_skeleton_agent import CodeSkeletonAgent
from src.agents.static_linter_agent import StaticLinterAgent
from src.agents.accessibility_audit_agent import AccessibilityAuditAgent
from src.advisors.requirements_advisor import RequirementsAdvisor
from src.advisors.prompt_refiner_advisor import PromptRefinerAdvisor
from src.advisors.code_review_advisor import CodeReviewAdvisor
from src.advisors.static_linter_advisor import StaticLinterAdvisor
from src.advisors.accessibility_audit_advisor import AccessibilityAuditAdvisor

AGENTS: Dict[str, Type[BaseFunctionalAgent]] = {
    "RequirementsDraftingAgent": RequirementsDraftingAgent,
    "PromptRefinerAgent": PromptRefinerAgent,
    "CodeSkeletonAgent": CodeSkeletonAgent,
    "StaticLinterAgent": StaticLinterAgent,
    "AccessibilityAuditAgent": AccessibilityAuditAgent,
    # TODO: register all 28 here
}

ADVISORS: Dict[str, Type[BaseAdvisor]] = {
    "RequirementsAdvisor": RequirementsAdvisor,
    "PromptRefinerAdvisor": PromptRefinerAdvisor,
    "CodeReviewAdvisor": CodeReviewAdvisor,
    "StaticLinterAdvisor": StaticLinterAdvisor,
    "AccessibilityAuditAdvisor": AccessibilityAuditAdvisor,
    # TODO: register all 15 here
}


def agent_factory(name: str) -> BaseFunctionalAgent:
    """Create an agent instance by name."""
    if name not in AGENTS:
        raise KeyError(f"Agent '{name}' not registered")
    return AGENTS[name]()


def advisor_factory(name: str) -> BaseAdvisor:
    """Create an advisor instance by name."""
    if name not in ADVISORS:
        raise KeyError(f"Advisor '{name}' not registered")
    return ADVISORS[name]()

