# Contributing Guide

Thank you for your interest in contributing to the Multi-Agent System! This guide will help you get started.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/AgentsSystemV2.git
   cd AgentsSystemV2
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"  # Install dev dependencies
   ```

4. **Run tests**
   ```bash
   pytest tests/ -v
   ```

5. **Run smoke tests**
   ```bash
   python scripts/smoke_test.py --skip-slow
   ```

## Code Style

### Python Code

- Follow PEP 8
- Use type hints
- Write docstrings for all public functions/classes
- Maximum line length: 100 characters
- Use `ruff` for linting and formatting

### Linting

```bash
ruff check .
ruff format .
```

### Type Checking

```bash
mypy src/
```

## Testing

### Unit Tests

- Write tests for all new features
- Tests should be in `tests/` directory
- Use `pytest` framework
- Aim for >80% code coverage

### Smoke Tests

- Run smoke tests before committing:
  ```bash
  python scripts/smoke_test.py --skip-slow
  ```
- All smoke tests must pass before PR submission

### Test Structure

```python
def test_feature_name():
    """Test description."""
    # Arrange
    # Act
    # Assert
    assert result == expected
```

## Commit Style

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

### Examples

```
feat: Add budget enforcement to orchestrator

Implement budget guard with time/stages/artifact limits.
Add Budget dataclass and enforce_budget() function.

Closes #123
```

```
fix: Fix checkpoint find_last_key to use step_index

Previously used mtime which was unreliable. Now uses
step_index for deterministic checkpoint selection.

Fixes #456
```

## Pull Request Process

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes**
   - Write code
   - Add tests
   - Update documentation
   - Run linting and tests

3. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: Add your feature"
   ```

4. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a pull request on GitHub.

5. **PR Requirements**
   - All tests pass
   - Smoke tests pass
   - Code is linted
   - Documentation updated
   - CHANGELOG.md updated (if applicable)

## Adding New Agents/Advisors

1. Create agent in `src/agents/`
2. Create advisor in `src/advisors/`
3. Add tests in `tests/`
4. Update `docs/agents_and_advisors.md`
5. Add example to pipeline YAML

## Documentation

- Update relevant docs in `docs/`
- Add examples where applicable
- Keep `docs/INDEX.md` updated

## Release Checklist

Before releasing a new version:

- [ ] All tests pass
- [ ] Smoke tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version bumped in `src/__init__.py` and `pyproject.toml`
- [ ] Tag created: `git tag v0.9.0`

## Questions?

- Open an issue for questions
- Check existing documentation in `docs/`
- Review existing code for patterns

Thank you for contributing! 🎉
