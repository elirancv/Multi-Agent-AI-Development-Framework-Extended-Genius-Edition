"""Plugin loader for external Agents/Advisors via entry points."""

from __future__ import annotations

import logging
from typing import Dict, Type, Optional

from src.core.base import BaseFunctionalAgent, BaseAdvisor

logger = logging.getLogger(__name__)

# Cache for loaded plugins
_AGENT_PLUGINS: Optional[Dict[str, Type[BaseFunctionalAgent]]] = None
_ADVISOR_PLUGINS: Optional[Dict[str, Type[BaseAdvisor]]] = None


def load_plugins(group: str) -> Dict[str, Type]:
    """
    Load plugins from entry points for a given group.
    
    Args:
        group: Entry point group name (e.g., "multiagent.agents")
    
    Returns:
        Dictionary mapping plugin names to their classes
    """
    loaded = {}
    
    try:
        from importlib.metadata import entry_points
        
        eps = entry_points().select(group=group)
        
        for ep in eps:
            try:
                plugin_class = ep.load()
                # Validate it's the right type
                if group == "multiagent.agents":
                    if not issubclass(plugin_class, BaseFunctionalAgent):
                        logger.warning(
                            f"Plugin {ep.name} does not inherit from BaseFunctionalAgent, skipping"
                        )
                        continue
                elif group == "multiagent.advisors":
                    if not issubclass(plugin_class, BaseAdvisor):
                        logger.warning(
                            f"Plugin {ep.name} does not inherit from BaseAdvisor, skipping"
                        )
                        continue
                
                loaded[ep.name] = plugin_class
                logger.info(f"Loaded plugin: {ep.name} from {ep.value}")
                
            except Exception as e:
                logger.warning(f"Failed to load plugin {ep.name}: {e}")
                continue
                
    except ImportError:
        # importlib.metadata not available (Python < 3.8)
        logger.debug("importlib.metadata not available, skipping plugin loading")
    except Exception as e:
        logger.warning(f"Error loading plugins from group {group}: {e}")
    
    return loaded


def get_agent_plugins() -> Dict[str, Type[BaseFunctionalAgent]]:
    """
    Get all registered agent plugins.
    
    Returns:
        Dictionary mapping plugin names to agent classes
    """
    global _AGENT_PLUGINS
    
    if _AGENT_PLUGINS is None:
        _AGENT_PLUGINS = load_plugins("multiagent.agents")
    
    return _AGENT_PLUGINS


def get_advisor_plugins() -> Dict[str, Type[BaseAdvisor]]:
    """
    Get all registered advisor plugins.
    
    Returns:
        Dictionary mapping plugin names to advisor classes
    """
    global _ADVISOR_PLUGINS
    
    if _ADVISOR_PLUGINS is None:
        _ADVISOR_PLUGINS = load_plugins("multiagent.advisors")
    
    return _ADVISOR_PLUGINS


def clear_plugin_cache() -> None:
    """Clear plugin cache (useful for testing)."""
    global _AGENT_PLUGINS, _ADVISOR_PLUGINS
    _AGENT_PLUGINS = None
    _ADVISOR_PLUGINS = None

