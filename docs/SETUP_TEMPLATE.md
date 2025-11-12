# Step-by-Step Template Setup Guide

This guide walks you through setting up a new project using this Cursor AI template.

## Prerequisites

- Cursor IDE installed
- Git installed (optional, for version control)
- Python 3.8+ (if building Python projects)

## Step 1: Copy Template Files

### Option A: Clone/Copy This Repository

```bash
# Clone this repository
git clone <template-repo-url> my-new-project
cd my-new-project

# Remove git history (if you want a fresh start)
rm -rf .git
git init
```

### Option B: Manual Copy

```bash
# Create new project directory
mkdir my-new-project
cd my-new-project

# Copy essential files
cp -r /path/to/template/.cursor .
cp /path/to/template/.cursorrules .
cp /path/to/template/.gitignore .
cp /path/to/template/README.md .
cp -r /path/to/template/docs .
```

## Step 2: Customize Project-Specific Files

### 2.1 Update README.md

Replace `README.md` with your project description:

```bash
# Option 1: Use the template
cp docs/readme_template.md README.md
# Then edit README.md with your project details

# Option 2: Start fresh
# Delete README.md and create your own
```

### 2.2 Remove Multi-Agent Files (If Not Needed)

If you're **not** building a multi-agent system:

```bash
# Remove multi-agent specific rules
rm .cursor/rules/multi_agent.mdc
rm .cursor/rules/orchestrator.mdc
rm .cursor/rules/pipeline.mdc  # Only if not using pipelines

# Remove multi-agent documentation
rm docs/agents_and_advisors.md
rm docs/agent_instructions.md
rm docs/example_multi_agent_readme.md
```

### 2.3 Update .cursorrules (Optional)

Edit `.cursorrules` if you want to customize the fallback rules:

```bash
# Open .cursorrules in your editor
# Update project-specific information
```

## Step 3: Create Project Structure

Create the basic directory structure:

```bash
# Create source directory
mkdir -p src

# Create tests directory
mkdir -p tests

# Create config directory (if needed)
mkdir -p config

# Create pipeline directory (if using pipelines)
mkdir -p pipeline
```

## Step 4: Initialize Python Project (If Applicable)

### 4.1 Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 4.2 Create requirements.txt

```bash
# Create requirements.txt
touch requirements.txt

# Add your dependencies
# Example:
# requests>=2.28.0
# pytest>=7.0.0
```

### 4.3 Create pyproject.toml (Optional)

```bash
# Create pyproject.toml for modern Python projects
cat > pyproject.toml << EOF
[project]
name = "my-project"
version = "0.1.0"
description = "My project description"
requires-python = ">=3.8"
dependencies = [
    "requests>=2.28.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=22.0.0",
    "ruff>=0.1.0",
]
EOF
```

## Step 5: Verify Rules Are Working

### 5.1 Test File Creation

Create a test file to verify rules are working:

```bash
# Create a Python file
cat > src/main.py << EOF
def hello_world():
    print("Hello, World!")

if __name__ == "__main__":
    hello_world()
EOF
```

Cursor should automatically:
- ✅ Suggest type hints
- ✅ Enforce English-only code
- ✅ Suggest proper structure

### 5.2 Test Documentation

Create a test documentation file:

```bash
# Create a doc file (should go to docs/)
cat > docs/getting_started.md << EOF
# Getting Started

This is a test documentation file.
EOF
```

Cursor should:
- ✅ Allow Hebrew in markdown docs
- ✅ Allow emojis in markdown
- ✅ Enforce proper file placement

## Step 6: Configure Git (Optional)

### 6.1 Initialize Git Repository

```bash
# Initialize git
git init

# Create initial commit
git add .
git commit -m "Initial commit: Template setup"
```

### 6.2 Create .gitignore

The template includes a `.gitignore` file. Review and customize as needed:

```bash
# Check .gitignore
cat .gitignore

# Add project-specific ignores if needed
```

## Step 7: Customize Rules (Optional)

### 7.1 Review Rule Files

Check which rules apply to your project:

```bash
# List all rule files
ls -la .cursor/rules/

# Read rule descriptions
cat .cursor/rules/README.mdc
```

### 7.2 Modify Rules

Edit rule files to match your project needs:

```bash
# Example: Modify code style rules
# Edit .cursor/rules/code_style.mdc

# Example: Modify project structure
# Edit .cursor/rules/project_structure.mdc
```

## Step 8: Test Everything

### 8.1 Create Test Files

```bash
# Create a Python module
mkdir -p src/my_module
cat > src/my_module/__init__.py << EOF
"""My module."""
EOF

# Create a test
cat > tests/test_my_module.py << EOF
import pytest
from my_module import something

def test_something():
    assert something() == expected
EOF
```

### 8.2 Verify Rules Apply

- ✅ Cursor suggests improvements
- ✅ Rules enforce structure
- ✅ File placement is correct

## Step 9: Start Development

You're ready to start coding!

```bash
# Create your first feature
# Cursor will guide you based on the rules

# Example workflow:
# 1. Create feature branch
git checkout -b feature/my-feature

# 2. Write code (Cursor enforces rules)
# 3. Write tests
# 4. Commit changes
git add .
git commit -m "Add my feature"
```

## Troubleshooting

### Rules Not Applying

**Problem:** Cursor rules not being applied

**Solutions:**
1. Check `.cursor/rules/` files have correct frontmatter
2. Verify `globs` patterns match your files
3. Ensure `alwaysApply: true` if needed
4. Restart Cursor IDE

### File Placement Issues

**Problem:** Files being created in wrong locations

**Solutions:**
1. Review `repository_hygiene.mdc` rules
2. Check `project_structure.mdc` rules
3. Manually move files to correct directories
4. Cursor will learn from your corrections

### Multi-Agent Errors

**Problem:** Errors about missing agents/advisors

**Solutions:**
1. Remove `multi_agent.mdc` if not using multi-agent
2. Remove `orchestrator.mdc` if not using orchestrator
3. Remove `pipeline.mdc` if not using pipelines

## Next Steps

- ✅ Read [Template Guide](TEMPLATE_GUIDE.md) for detailed information
- ✅ Review [README Template](readme_template.md) for your project README
- ✅ Check [Example Multi-Agent README](example_multi_agent_readme.md) if building multi-agent system
- ✅ Start coding with Cursor AI assistance!

## Quick Reference

### Essential Files to Keep
- `.cursor/rules/` - All rule files
- `.cursorrules` - Fallback rules
- `.gitignore` - Git ignore rules
- `README.md` - Your project README

### Files to Customize
- `README.md` - Replace with your project description
- `.cursor/rules/*.mdc` - Modify rules as needed
- `.gitignore` - Add project-specific ignores

### Files to Remove (If Not Needed)
- `multi_agent.mdc` - If not using multi-agent
- `orchestrator.mdc` - If not using orchestrator
- `pipeline.mdc` - If not using pipelines
- Multi-agent documentation files

---

**Need Help?** Check the [Template Guide](TEMPLATE_GUIDE.md) for more details.
