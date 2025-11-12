# Project Name

> **Template Note:** This README is a template. Replace this content with your project-specific information.

## Overview

Brief description of your project.

## Features

- Feature 1
- Feature 2
- Feature 3

## Project Structure

```
project_root/
├── README.md                # Project overview (root only)
├── .cursorrules             # Cursor AI rules (fallback)
├── .cursor/
│   └── rules/              # Detailed Cursor rules (.mdc files)
├── docs/                    # Documentation
├── src/                     # Source code
├── tests/                   # Tests
├── config/                  # Configuration files
└── pipeline/                # Pipeline definitions (if applicable)
```

## Getting Started

### Prerequisites

- Python 3.8+
- (Add other dependencies)

### Installation

```bash
# Add installation steps
pip install -r requirements.txt
```

### Usage

```bash
# Add usage examples
python src/main.py
```

## Development

### Code Style

This project follows the rules defined in `.cursor/rules/`:
- Python code in English only
- PEP 8 compliance
- Type hints required
- Descriptive file names

### Testing

```bash
pytest tests/
```

### Documentation

Documentation is located in `docs/`. Only `README.md` should be in the project root.

## Cursor AI Rules

This project uses Cursor AI with comprehensive rules defined in `.cursor/rules/`. These rules enforce:
- Project structure and file placement
- Code style and conventions
- Repository hygiene
- Multi-agent architecture (if applicable)

See `docs/TEMPLATE_GUIDE.md` for details on using this as a template.

## Contributing

(Add contribution guidelines)

## License

(Add license information)

---

**Note:** This project uses Cursor AI rules. See `.cursor/rules/README.mdc` for rule documentation.
