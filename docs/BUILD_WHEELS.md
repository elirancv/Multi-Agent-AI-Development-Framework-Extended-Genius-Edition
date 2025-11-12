# Building Distribution Packages (Wheels)

This guide explains how to build distribution packages (wheels and source distributions) for PyPI or local distribution.

## Prerequisites

```bash
pip install --upgrade build twine
```

## Building Packages

### Build Both Wheel and Source Distribution

```bash
python -m build
```

This creates:
- `dist/*.whl` - Built wheel (binary distribution)
- `dist/*.tar.gz` - Source distribution

### Build Only Wheel

```bash
python -m build --wheel
```

### Build Only Source Distribution

```bash
python -m build --sdist
```

## Verification

### Check Package Contents

```bash
# List files in wheel
python -m zipfile -l dist/*.whl

# List files in source distribution
tar -tzf dist/*.tar.gz | head -20
```

### Validate Package

```bash
twine check dist/*
```

This checks:
- Package metadata validity
- File structure
- README formatting
- License file presence

## Local Testing

### Install from Local Wheel

```bash
pip install dist/*.whl --force-reinstall
```

### Install from Source Distribution

```bash
pip install dist/*.tar.gz --force-reinstall
```

## PyPI Publishing

### Test on TestPyPI First

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ your-package-name
```

### Publish to PyPI

```bash
# Upload to PyPI (requires PYPI_TOKEN)
twine upload dist/*
```

Or use the automated GitHub Actions workflow (`.github/workflows/publish-pypi.yml`).

## pyproject.toml Requirements

Ensure `pyproject.toml` includes:

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "multiagent-orchestrator"
version = "1.0.0"
description = "Multi-Agent AI Development Framework"
readme = "README.md"
requires-python = ">=3.11"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

[project.scripts]
multiagent = "src.cli:main"
```

## CI/CD Integration

The `.github/workflows/publish-pypi.yml` workflow automatically:
1. Builds packages on tag push (`v*`)
2. Validates packages
3. Publishes to PyPI (if `PYPI_TOKEN` is configured)

## Troubleshooting

### Build Fails

- Check `pyproject.toml` syntax
- Ensure all required files are included
- Verify `MANIFEST.in` if using setuptools

### Upload Fails

- Verify `PYPI_TOKEN` is set correctly
- Check package name doesn't conflict with existing packages
- Ensure version number is incremented

## References

- [Python Packaging Guide](https://packaging.python.org/)
- [Build Documentation](https://pypa-build.readthedocs.io/)
- [Twine Documentation](https://twine.readthedocs.io/)

