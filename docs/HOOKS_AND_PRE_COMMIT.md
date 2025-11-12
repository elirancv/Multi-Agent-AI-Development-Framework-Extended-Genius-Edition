# Hooks and Pre-Commit Setup

## Post-Step Hooks

The orchestrator supports post-step hooks that run after each pipeline step completes (whether approved or not). This enables automatic actions like prompt refinement on failure.

### Hook Interface

```python
from src.orchestrator.hooks import PostStepHook, PromptRefinerOnFailure

class PostStepHook(Protocol):
    def __call__(
        self,
        *,
        step_result: Dict[str, Any],
        shared_memory: SharedMemory,
    ) -> None:
        """Execute hook logic."""
        ...
```

### Built-in Hook: PromptRefinerOnFailure

Automatically runs `PromptRefinerAgent` when a step fails review, storing the refined prompt in memory for downstream steps.

**Usage:**

```python
from src.orchestrator.hooks import PromptRefinerOnFailure
from src.orchestrator.factory import agent_factory, advisor_factory

hook = PromptRefinerOnFailure(
    agent_factory=agent_factory,
    advisor_factory=advisor_factory,
    refiner_agent="PromptRefinerAgent",
    refiner_advisor="PromptRefinerAdvisor",
    min_score=0.85,
    task_template="Refine the prompt based on the last review for: {product_idea}",
)

# Add to orchestrator
orch = Orchestrator(
    agent_factory=agent_factory,
    advisor_factory=advisor_factory,
    post_step_hooks=[hook],
)
```

**CLI Usage:**

```bash
# Sequential with auto-refine on failure
python cli.py --pipeline pipeline/example.yaml --refine-on-fail

# Parallel with auto-refine
python cli.py --pipeline pipeline/with_codegen.yaml --parallel --max-workers 4 --refine-on-fail
```

**Memory Keys:**

When a step fails, the hook stores:
- `{stage}.refined_prompt.content` - Refined prompt content (if refiner passes)
- `{stage}.refined_prompt.artifacts` - Refined artifacts
- `{stage}.refined_prompt.review` - Refiner's review

If the refiner itself fails:
- `{stage}.refined_prompt_attempt.*` - Attempt results (for transparency)

### Custom Hooks

Create custom hooks by implementing the `PostStepHook` protocol:

```python
class MyCustomHook:
    def __call__(self, *, step_result: Dict[str, Any], shared_memory: SharedMemory) -> None:
        if step_result["approved"]:
            # Do something on success
            pass
        else:
            # Do something on failure
            pass
```

## Pre-Commit Setup

### Installation

```bash
pip install pre-commit
pre-commit install
```

### Configuration

The project uses:
- **Ruff** - Fast Python linter and formatter
- **MyPy** - Static type checker
- **Pre-commit hooks** - YAML validation, trailing whitespace, etc.

**Files:**
- `.pre-commit-config.yaml` - Pre-commit hook definitions
- `pyproject.toml` - Ruff configuration
- `mypy.ini` - MyPy configuration

### Running Manually

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run specific hook
pre-commit run ruff --all-files
pre-commit run mypy --all-files
```

### CI Integration

GitHub Actions automatically runs pre-commit hooks and tests on push/PR:

```yaml
# .github/workflows/ci.yml
- name: Run pre-commit
  run: pre-commit run --all-files

- name: Run tests
  run: pytest -q
```

## Ruff Configuration

Configured in `pyproject.toml`:

```toml
[tool.ruff]
target-version = "py38"
line-length = 100
lint.select = ["E", "F", "I", "B", "UP", "N", "S", "W", "RUF"]
lint.ignore = ["E203", "E266"]
exclude = ["venv", ".venv", "dist", "build", "__pycache__", ".git"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

## MyPy Configuration

Configured in `mypy.ini`:

```ini
[mypy]
python_version = 3.8
ignore_missing_imports = True
strict_optional = True
warn_return_any = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
```

## Best Practices

1. **Hooks run after checkpointing** - Safe to mutate memory for downstream steps
2. **Hooks are opt-in** - Use `--refine-on-fail` flag to enable
3. **Backward compatible** - Existing pipelines work without hooks
4. **Pre-commit runs automatically** - On git commit (if installed)
5. **CI enforces quality** - GitHub Actions runs pre-commit + tests

## Troubleshooting

**Pre-commit fails:**
```bash
# Update hooks
pre-commit autoupdate

# Skip hooks for one commit
git commit --no-verify
```

**MyPy errors:**
- Check `mypy.ini` for ignored imports
- Add type stubs: `pip install types-PyYAML`

**Ruff errors:**
- Auto-fix: `ruff check --fix .`
- Format: `ruff format .`
