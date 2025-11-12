# Plugin API - External Agents/Advisors

This document describes how to create and register external Agents/Advisors as plugins (planned for v1.1+).

## Overview

The Plugin API allows third-party packages to extend the framework with custom Agents and Advisors without modifying core code. Plugins are discovered automatically via Python entry points.

## Quick Start

### 1. Create Your Plugin Package

```python
# my_package/agents/custom_agent.py
from src.core.base import BaseFunctionalAgent
from src.core.types import AgentOutput

class CustomAgent(BaseFunctionalAgent):
    name = "CustomAgent"
    min_advisor_score = 0.85
    
    def process(self, task: str, context: dict) -> AgentOutput:
        # Your implementation
        return AgentOutput(
            content="Custom output",
            artifacts=[],
            metadata={"agent": "CustomAgent"}
        )
```

### 2. Register Entry Point

In your `pyproject.toml`:

```toml
[project.entry-points."multiagent.agents"]
my_org.CustomAgent = "my_package.agents.custom_agent:CustomAgent"

[project.entry-points."multiagent.advisors"]
my_org.CustomAdvisor = "my_package.advisors.custom_advisor:CustomAdvisor"
```

### 3. Install and Use

```bash
pip install my-package
python cli.py --pipeline pipeline/my_pipeline.yaml
# CustomAgent will be automatically available
```

## Plugin Contracts

### Agent Contract

All agent plugins must:

1. Inherit from `BaseFunctionalAgent`
2. Implement `process(task: str, context: dict) -> AgentOutput`
3. Return `AgentOutput` with required fields:
   - `content: str` - Main output content
   - `artifacts: List[Artifact]` - Generated artifacts
   - `metadata: dict` - Agent metadata

### Advisor Contract

All advisor plugins must:

1. Inherit from `BaseAdvisor`
2. Implement `review(output: AgentOutput, task: str, context: dict) -> AdvisorReview`
3. Return `AdvisorReview` with required fields:
   - `score: float` (0.0-1.0)
   - `approved: bool`
   - `critical_issues: List[str]`
   - `suggestions: List[str]`
   - `summary: str`
   - `severity: str` ("low" | "medium" | "high")

## Entry Point Naming

Entry point names should follow this pattern:

```
<org>.<AgentName> = "<module.path>:<ClassName>"
```

Examples:
- `my_org.StaticLinterX = "my_pkg.agents.static_linter_x:StaticLinterX"`
- `acme.SecReviewX = "acme_pkg.advisors.sec_review_x:SecReviewX`

## Plugin Discovery

Plugins are automatically discovered when:

1. Package is installed (via `pip install`)
2. Entry points are registered in `pyproject.toml`
3. Framework loads agents/advisors via factory functions

## Plugin Loading Order

1. **Core agents/advisors** are loaded first
2. **Plugins** are loaded and merged
3. **Name conflicts**: Plugins override core (with warning)

## Example: Complete Plugin Package

```python
# my_package/__init__.py
__version__ = "1.0.0"

# my_package/agents/__init__.py
from .custom_agent import CustomAgent
__all__ = ["CustomAgent"]

# my_package/agents/custom_agent.py
from src.core.base import BaseFunctionalAgent
from src.core.types import AgentOutput

class CustomAgent(BaseFunctionalAgent):
    name = "CustomAgent"
    
    def process(self, task: str, context: dict) -> AgentOutput:
        return AgentOutput(
            content=f"Processed: {task}",
            artifacts=[],
            metadata={"agent": "CustomAgent"}
        )

# my_package/advisors/custom_advisor.py
from src.core.base import BaseAdvisor
from src.core.types import AgentOutput, AdvisorReview

class CustomAdvisor(BaseAdvisor):
    name = "CustomAdvisor"
    
    def review(self, output: AgentOutput, task: str, context: dict) -> AdvisorReview:
        return {
            "score": 0.9,
            "approved": True,
            "critical_issues": [],
            "suggestions": [],
            "summary": "Good output",
            "severity": "low"
        }
```

```toml
# pyproject.toml
[project]
name = "my-package"
version = "1.0.0"

[project.entry-points."multiagent.agents"]
my_org.CustomAgent = "my_package.agents.custom_agent:CustomAgent"

[project.entry-points."multiagent.advisors"]
my_org.CustomAdvisor = "my_package.advisors.custom_advisor:CustomAdvisor"
```

## Testing Plugins

```python
# tests/test_custom_agent.py
from my_package.agents.custom_agent import CustomAgent
from src.core.types import AgentOutput

def test_custom_agent():
    agent = CustomAgent()
    result = agent.process("test task", {})
    assert isinstance(result, AgentOutput)
    assert result.content
```

## Debugging

Enable debug logging to see plugin loading:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

You'll see messages like:
```
INFO: Loaded plugin: my_org.CustomAgent from my_package.agents.custom_agent:CustomAgent
```

## Status

**Current Status**: 🟡 **Preview** (v1.0.0)

**Full Support**: 🟢 **v1.1.0+**

The Plugin API infrastructure is in place, but full documentation and examples will be available in v1.1.0.

## See Also

- [Issue: Plugin API](.github/ISSUE_TEMPLATE/v1.1-plugin-api.md)
- [Base Classes](src/core/base.py)
- [Factory Functions](src/orchestrator/factory.py)
- [Plugin Loader](src/orchestrator/plugin_loader.py)

