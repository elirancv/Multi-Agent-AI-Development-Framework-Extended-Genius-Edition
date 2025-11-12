"""Factory functions for creating agents and advisors."""

from __future__ import annotations

import logging
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

logger = logging.getLogger(__name__)

# Core agents (built-in)
CORE_AGENTS: Dict[str, Type[BaseFunctionalAgent]] = {
    "RequirementsDraftingAgent": RequirementsDraftingAgent,
    "PromptRefinerAgent": PromptRefinerAgent,
    "CodeSkeletonAgent": CodeSkeletonAgent,
    "StaticLinterAgent": StaticLinterAgent,
    "AccessibilityAuditAgent": AccessibilityAuditAgent,
    # TODO: register all 28 here
}

# Core advisors (built-in)
CORE_ADVISORS: Dict[str, Type[BaseAdvisor]] = {
    "RequirementsAdvisor": RequirementsAdvisor,
    "PromptRefinerAdvisor": PromptRefinerAdvisor,
    "CodeReviewAdvisor": CodeReviewAdvisor,
    "StaticLinterAdvisor": StaticLinterAdvisor,
    "AccessibilityAuditAdvisor": AccessibilityAuditAdvisor,
    # TODO: register all 15 here
}


def _get_all_agents() -> Dict[str, Type[BaseFunctionalAgent]]:
    """Get all agents (core + plugins)."""
    from src.orchestrator.plugin_loader import get_agent_plugins
    
    agents = CORE_AGENTS.copy()
    plugins = get_agent_plugins()
    
    # Plugins override core agents if name conflicts
    for name, plugin_class in plugins.items():
        if name in agents:
            logger.warning(f"Plugin {name} overrides core agent")
        agents[name] = plugin_class
    
    return agents


def _get_all_advisors() -> Dict[str, Type[BaseAdvisor]]:
    """Get all advisors (core + plugins)."""
    from src.orchestrator.plugin_loader import get_advisor_plugins
    
    advisors = CORE_ADVISORS.copy()
    plugins = get_advisor_plugins()
    
    # Plugins override core advisors if name conflicts
    for name, plugin_class in plugins.items():
        if name in advisors:
            logger.warning(f"Plugin {name} overrides core advisor")
        advisors[name] = plugin_class
    
    return advisors


def agent_factory(name: str) -> BaseFunctionalAgent:
    """
    Create an agent instance by name.
    
    Checks core agents first, then plugins.
    """
    agents = _get_all_agents()
    
    if name not in agents:
        available = ", ".join(sorted(agents.keys()))
        raise KeyError(
            f"Agent '{name}' not found. Available agents: {available}"
        )
    
    return agents[name]()


def advisor_factory(name: str) -> BaseAdvisor:
    """
    Create an advisor instance by name.
    
    Checks core advisors first, then plugins.
    """
    advisors = _get_all_advisors()
    
    if name not in advisors:
        available = ", ".join(sorted(advisors.keys()))
        raise KeyError(
            f"Advisor '{name}' not found. Available advisors: {available}"
        )
    
    return advisors[name]()
