"""Contract tests for all Agents and Advisors."""

import inspect
import pkgutil
import importlib
from typing import Dict, Any

import pytest

from src.core.types import AgentOutput, AdvisorReview
from src.core.base import BaseFunctionalAgent, BaseAdvisor


def iter_subclasses(module_name: str, base_class):
    """Iterate over all subclasses of base_class in module_name."""
    try:
        m = importlib.import_module(module_name)
        if not hasattr(m, "__path__"):
            return
        
        for _, name, _ in pkgutil.iter_modules(m.__path__):
            try:
                mod = importlib.import_module(f"{module_name}.{name}")
                for _, cls in inspect.getmembers(mod, inspect.isclass):
                    if (
                        issubclass(cls, base_class)
                        and cls is not base_class
                        and cls.__module__.startswith(module_name)
                    ):
                        yield cls
            except (ImportError, AttributeError):
                continue
    except ImportError:
        pass


@pytest.mark.parametrize("agent_class", list(iter_subclasses("src.agents", BaseFunctionalAgent)))
def test_all_agents_contracts(agent_class):
    """Test that all agents return AgentOutput with correct structure."""
    agent = agent_class()
    
    # Test process method exists
    assert hasattr(agent, "process"), f"{agent_class.__name__} missing process method"
    
    # Test process returns AgentOutput
    output = agent.process(task="test task", context={"seed": 42})
    
    assert isinstance(output, AgentOutput), f"{agent_class.__name__} must return AgentOutput"
    assert isinstance(output.content, str), f"{agent_class.__name__} content must be str"
    assert isinstance(output.artifacts, list), f"{agent_class.__name__} artifacts must be list"
    # Metadata can be dict or dataclass (AgentMetadata)
    assert hasattr(output.metadata, '__dict__') or isinstance(output.metadata, dict), \
        f"{agent_class.__name__} metadata must be dict or dataclass"
    
    # Validate content is not empty
    assert output.content.strip(), f"{agent_class.__name__} content must not be empty"
    
    # Validate metadata contains agent name (check both dict and dataclass)
    metadata_dict = output.metadata if isinstance(output.metadata, dict) else output.metadata.__dict__
    assert "agent_name" in metadata_dict or "agent" in metadata_dict or "source" in metadata_dict, \
        f"{agent_class.__name__} metadata should include agent/source"


@pytest.mark.parametrize("advisor_class", list(iter_subclasses("src.advisors", BaseAdvisor)))
def test_all_advisors_contracts(advisor_class):
    """Test that all advisors return AdvisorReview with correct structure."""
    advisor = advisor_class()
    
    # Test review method exists
    assert hasattr(advisor, "review"), f"{advisor_class.__name__} missing review method"
    
    # Create dummy output
    dummy_output = AgentOutput(
        content="test content",
        artifacts=[],
        metadata={"agent": "TestAgent"}
    )
    
    # Test review returns AdvisorReview
    review = advisor.review(
        output=dummy_output,
        task="test task",
        context={}
    )
    
    assert isinstance(review, dict), f"{advisor_class.__name__} must return dict"
    
    # Validate required fields
    assert "score" in review, f"{advisor_class.__name__} missing score"
    assert "approved" in review, f"{advisor_class.__name__} missing approved"
    assert "critical_issues" in review, f"{advisor_class.__name__} missing critical_issues"
    assert "suggestions" in review, f"{advisor_class.__name__} missing suggestions"
    assert "summary" in review, f"{advisor_class.__name__} missing summary"
    assert "severity" in review, f"{advisor_class.__name__} missing severity"
    
    # Validate types
    assert isinstance(review["score"], (int, float)), f"{advisor_class.__name__} score must be numeric"
    assert 0.0 <= review["score"] <= 1.0, f"{advisor_class.__name__} score must be 0.0-1.0"
    assert isinstance(review["approved"], bool), f"{advisor_class.__name__} approved must be bool"
    assert isinstance(review["critical_issues"], list), f"{advisor_class.__name__} critical_issues must be list"
    assert isinstance(review["suggestions"], list), f"{advisor_class.__name__} suggestions must be list"
    assert isinstance(review["summary"], str), f"{advisor_class.__name__} summary must be str"
    assert review["severity"] in {"low", "medium", "high", "critical"}, \
        f"{advisor_class.__name__} severity must be one of: low, medium, high, critical"


def test_base_functional_agent_contract():
    """Test BaseFunctionalAgent abstract contract."""
    from src.core.base import BaseFunctionalAgent
    
    # Cannot instantiate abstract class
    with pytest.raises(TypeError):
        BaseFunctionalAgent()
    
    # Check required attributes
    assert hasattr(BaseFunctionalAgent, "name")
    assert hasattr(BaseFunctionalAgent, "min_advisor_score")
    assert hasattr(BaseFunctionalAgent, "version")


def test_base_advisor_contract():
    """Test BaseAdvisor abstract contract."""
    from src.core.base import BaseAdvisor
    
    # Cannot instantiate abstract class
    with pytest.raises(TypeError):
        BaseAdvisor()
    
    # Check required attributes
    assert hasattr(BaseAdvisor, "name")

