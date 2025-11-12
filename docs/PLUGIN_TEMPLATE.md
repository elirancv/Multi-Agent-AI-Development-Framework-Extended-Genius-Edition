# Plugin Template - Third-Party Package

Complete template for creating external Agents/Advisors plugins.

## Package Structure

```
my-multiagent-plugin/
├── my_pkg/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   └── custom_agent.py
│   └── advisors/
│       ├── __init__.py
│       └── custom_advisor.py
├── tests/
│   └── test_custom_agent.py
├── pyproject.toml
└── README.md
```

## 1. Agent Implementation

```python
# my_pkg/agents/custom_agent.py
from typing import Dict, Any
from src.core.types import AgentOutput, Artifact
from src.core.base import BaseFunctionalAgent


class CustomAgent(BaseFunctionalAgent):
    """Example external agent (preview)."""

    name: str = "CustomAgent"
    version: str = "0.1.0"
    min_advisor_score: float = 0.85

    def process(self, task: str, context: Dict[str, Any]) -> AgentOutput:
        """Process task and return structured output."""
        content = f"[CustomAgent] Task received: {task}"

        artifacts = [
            Artifact(
                name="custom_summary.md",
                mime_type="text/markdown",
                data=content.encode("utf-8"),
            )
        ]

        metadata = {
            "source": "custom-plugin",
            "len_task": len(task),
            "agent": "CustomAgent"
        }

        return AgentOutput(
            content=content,
            artifacts=artifacts,
            metadata=metadata
        )
```

## 2. Advisor Implementation

```python
# my_pkg/advisors/custom_advisor.py
from typing import Dict, Any
from src.core.types import AgentOutput, AdvisorReview
from src.core.base import BaseAdvisor


class CustomAdvisor(BaseAdvisor):
    """Example external advisor (preview)."""

    name: str = "CustomAdvisor"
    min_score: float = 0.80

    def review(
        self,
        output: AgentOutput,
        task: str,
        context: Dict[str, Any]
    ) -> AdvisorReview:
        """Review agent output and return structured review."""
        ok = bool(output.content and output.content.strip())
        score = 1.0 if ok else 0.0

        return {
            "score": score,
            "approved": score >= self.min_score,
            "critical_issues": [] if ok else ["Empty content"],
            "suggestions": [] if ok else ["Return non-empty content"],
            "summary": "Basic sanity review",
            "severity": "low" if ok else "critical",
        }
```

## 3. Package Configuration

```toml
# pyproject.toml
[project]
name = "my-multiagent-plugin"
version = "0.1.0"
description = "Custom agents and advisors for multi-agent framework"
requires-python = ">=3.8"
dependencies = [
    # Add framework as dependency (when published)
    # "multi-agent-system>=1.0.0",
]

[project.entry-points."multiagent.agents"]
my_org.CustomAgent = "my_pkg.agents.custom_agent:CustomAgent"

[project.entry-points."multiagent.advisors"]
my_org.CustomAdvisor = "my_pkg.advisors.custom_advisor:CustomAdvisor"

[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

## 4. Package Init Files

```python
# my_pkg/__init__.py
__version__ = "0.1.0"

# my_pkg/agents/__init__.py
from .custom_agent import CustomAgent
__all__ = ["CustomAgent"]

# my_pkg/advisors/__init__.py
from .custom_advisor import CustomAdvisor
__all__ = ["CustomAdvisor"]
```

## 5. Tests

```python
# tests/test_custom_agent.py
import pytest
from my_pkg.agents.custom_agent import CustomAgent
from my_pkg.advisors.custom_advisor import CustomAdvisor
from src.core.types import AgentOutput, AdvisorReview


def test_custom_agent():
    agent = CustomAgent()
    result = agent.process("test task", {})

    assert isinstance(result, AgentOutput)
    assert result.content
    assert len(result.artifacts) > 0


def test_custom_advisor():
    advisor = CustomAdvisor()
    output = AgentOutput(
        content="test content",
        artifacts=[],
        metadata={}
    )
    review = advisor.review(output, "test task", {})

    assert isinstance(review, dict)
    assert "score" in review
    assert "approved" in review
    assert review["score"] >= 0.0
    assert review["score"] <= 1.0
```

## 6. Installation & Discovery

### Install Locally (Development)
```bash
pip install -e .
```

### Verify Discovery
```bash
python - <<'PY'
from src.orchestrator.plugin_loader import load_plugins

agents = load_plugins("multiagent.agents")
advs = load_plugins("multiagent.advisors")

print("Agents:", list(agents.keys()))
print("Advisors:", list(advs.keys()))

# Should show: my_org.CustomAgent, my_org.CustomAdvisor
PY
```

## 7. Using in Pipeline

```yaml
# pipeline/custom_example.yaml
stages:
  - name: custom_stage
    category: codegen
    agent: my_org.CustomAgent          # Discovered via entry points
    advisor: my_org.CustomAdvisor
    task: "Generate a structured summary for: {{ product_idea }}"
    output: docs/custom_output.md
    min_score: 0.80
```

## 8. README Template

```markdown
# My Multi-Agent Plugin

Custom agents and advisors for the Multi-Agent AI Development Framework.

## Installation

```bash
pip install my-multiagent-plugin
```

## Usage

Register in your pipeline YAML:

```yaml
stages:
  - name: custom_stage
    agent: my_org.CustomAgent
    advisor: my_org.CustomAdvisor
    task: "Your task here"
```

## Development

```bash
git clone <repo>
cd my-multiagent-plugin
pip install -e .
```

## License

MIT
```

## See Also

- [Plugin API Documentation](PLUGIN_API.md)
- [Issue Template](.github/ISSUE_TEMPLATE/v1.1-plugin-api.md)
