# Test Plugin Specification - CI Validation

Specification for a minimal external test plugin to validate Plugin API in CI.

## Purpose

Create a lightweight test plugin package that:
1. Validates entry point discovery works
2. Tests plugin loading in CI
3. Guards against regressions
4. Serves as reference implementation

## Package Structure

```
test-plugin-multiagent/
├── test_plugin/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   └── test_agent.py
│   └── advisors/
│       ├── __init__.py
│       └── test_advisor.py
├── tests/
│   └── test_integration.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── pyproject.toml
├── tox.ini
└── README.md
```

## Implementation

### Test Agent

```python
# test_plugin/agents/test_agent.py
from src.core.types import AgentOutput
from src.core.base import BaseFunctionalAgent


class TestAgent(BaseFunctionalAgent):
    """Minimal test agent for CI validation."""
    
    name = "TestAgent"
    version = "0.1.0"
    
    def process(self, task: str, context: dict) -> AgentOutput:
        return AgentOutput(
            content=f"Test output for: {task}",
            artifacts=[],
            metadata={"test": True}
        )
```

### Test Advisor

```python
# test_plugin/advisors/test_advisor.py
from src.core.types import AgentOutput, AdvisorReview
from src.core.base import BaseAdvisor


class TestAdvisor(BaseAdvisor):
    """Minimal test advisor for CI validation."""
    
    name = "TestAdvisor"
    
    def review(self, output: AgentOutput, task: str, context: dict) -> AdvisorReview:
        return {
            "score": 1.0,
            "approved": True,
            "critical_issues": [],
            "suggestions": [],
            "summary": "Test review",
            "severity": "low"
        }
```

### Entry Points

```toml
# pyproject.toml
[project.entry-points."multiagent.agents"]
test.TestAgent = "test_plugin.agents.test_agent:TestAgent"

[project.entry-points."multiagent.advisors"]
test.TestAdvisor = "test_plugin.advisors.test_advisor:TestAdvisor"
```

## CI Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml
name: Test Plugin CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Checkout framework
        uses: actions/checkout@v4
        with:
          repository: your-org/AgentsSystemV2
          path: framework
          token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      
      - name: Install framework
        run: |
          cd framework
          pip install -e .
      
      - name: Install test plugin
        run: pip install -e .
      
      - name: Test plugin discovery
        run: |
          python -c "
          from src.orchestrator.plugin_loader import load_plugins
          agents = load_plugins('multiagent.agents')
          assert 'test.TestAgent' in agents, 'TestAgent not found'
          print('✅ Plugin discovery works')
          "
      
      - name: Test factory integration
        run: |
          python -c "
          from src.orchestrator.factory import agent_factory, advisor_factory
          agent = agent_factory('test.TestAgent')
          advisor = advisor_factory('test.TestAdvisor')
          print('✅ Factory integration works')
          "
```

### Tox Configuration

```ini
# tox.ini
[tox]
envlist = py311

[testenv]
deps =
    pytest>=7.0.0
commands =
    pytest tests/
```

## Integration Test

```python
# tests/test_integration.py
import pytest
from src.orchestrator.plugin_loader import load_plugins
from src.orchestrator.factory import agent_factory, advisor_factory
from test_plugin.agents.test_agent import TestAgent
from test_plugin.advisors.test_advisor import TestAdvisor


def test_plugin_discovery():
    """Test that plugin is discovered via entry points."""
    agents = load_plugins("multiagent.agents")
    assert "test.TestAgent" in agents
    assert agents["test.TestAgent"] == TestAgent


def test_factory_integration():
    """Test that factory can create plugin instances."""
    agent = agent_factory("test.TestAgent")
    assert isinstance(agent, TestAgent)
    
    advisor = advisor_factory("test.TestAdvisor")
    assert isinstance(advisor, TestAdvisor)


def test_plugin_functionality():
    """Test that plugin works end-to-end."""
    agent = agent_factory("test.TestAgent")
    output = agent.process("test task", {})
    
    assert output.content
    assert output.metadata.get("test") is True
    
    advisor = advisor_factory("test.TestAdvisor")
    review = advisor.review(output, "test task", {})
    
    assert review["approved"] is True
    assert review["score"] == 1.0
```

## Usage in Main Framework CI

Add to main framework's CI to validate plugin loading:

```yaml
# .github/workflows/plugin-test.yml
name: Plugin API Test

on:
  pull_request:
    paths:
      - "src/orchestrator/plugin_loader.py"
      - "src/orchestrator/factory.py"
      - "pyproject.toml"

jobs:
  test-plugin-loading:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install framework
        run: pip install -e .
      
      - name: Install test plugin
        run: |
          git clone <test-plugin-repo> test-plugin
          cd test-plugin
          pip install -e .
      
      - name: Validate plugin loading
        run: |
          python -c "
          from src.orchestrator.plugin_loader import load_plugins
          agents = load_plugins('multiagent.agents')
          assert len(agents) > 0, 'No plugins found'
          print(f'✅ Found {len(agents)} plugins')
          "
```

## Benefits

1. **Regression Testing**: Catches plugin loading breakages early
2. **Reference Implementation**: Shows how to create plugins
3. **CI Validation**: Ensures Plugin API works in automated tests
4. **Documentation**: Living example of plugin development

## Repository Setup

1. Create separate repository: `test-plugin-multiagent`
2. Use this spec as README
3. Add CI workflow
4. Link from main framework docs

## See Also

- [Plugin Template](PLUGIN_TEMPLATE.md)
- [Plugin API](PLUGIN_API.md)

