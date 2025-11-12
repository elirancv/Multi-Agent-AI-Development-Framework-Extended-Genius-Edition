# Using This Project as a Cursor Template

This project is designed to serve as a **reusable template** for Python development projects with Cursor AI. It includes comprehensive rules, project structure guidelines, and best practices.

## What's Included

### 1. Cursor Rules (`.cursor/rules/`)

Comprehensive rule files covering:
- **Project Structure** - Directory layout, file naming, repository hygiene
- **Code Style** - Python conventions, language rules, formatting
- **Multi-Agent Architecture** - Agent/advisor contracts, 1:1 mapping (if using multi-agent systems)
- **Pipeline Configuration** - YAML structure, dependencies, shared advisors
- **Testing** - Pytest patterns, coverage requirements
- **Orchestrator** - Validation rules, cross-cutting reviewers, project modes
- **File Type Rules** - CSS, HTML, JavaScript, SQL, Docker, YAML, JSON, TOML, env files

### 2. Project Structure

```
project_root/
├── README.md                # Project overview (root only)
├── .cursorrules             # Fallback rules (references .cursor/rules/)
├── .cursor/
│   └── rules/              # Detailed rules by topic (.mdc files)
├── docs/                    # All additional markdown docs
├── src/                     # Source code
├── tests/                   # Pytest-based tests
├── config/                  # Configuration files
└── pipeline/                # Pipeline definitions (.yaml)
```

## How to Use This Template

### Option 1: Copy the Rules Structure

1. Copy `.cursor/rules/` directory to your new project
2. Copy `.cursorrules` file to your new project root
3. Customize `README.md` for your project
4. Remove multi-agent specific rules if not needed:
   - `multi_agent.mdc` (if not using multi-agent systems)
   - `orchestrator.mdc` (if not using orchestrator)
   - `pipeline.mdc` (if not using pipelines)

### Option 2: Start Fresh with Rules

1. Create a new project
2. Copy `.cursor/rules/` directory
3. Copy `.cursorrules` file
4. Keep only the rules you need

## Customization

### For Non-Multi-Agent Projects

If you're not building a multi-agent system, you can remove:
- `multi_agent.mdc`
- `orchestrator.mdc`
- `pipeline.mdc` (unless you use pipelines for other purposes)
- `docs/agents_and_advisors.md`
- `docs/agent_instructions.md`

### For Different Languages

The rules include support for:
- Python (primary)
- JavaScript/TypeScript
- HTML/CSS
- SQL
- Shell scripts

Add language-specific rules as needed.

### For Different Project Types

The rules are designed to be flexible:
- **Web Applications** - Use HTML, CSS, JavaScript rules
- **API Services** - Use Python, YAML, Docker rules
- **Data Projects** - Use Python, SQL rules
- **CLI Tools** - Use Python, Shell script rules

## Key Features

### 1. Repository Hygiene Enforcement

Rules automatically enforce:
- No orphan files in root
- Proper file placement (code → `src/`, docs → `docs/`, etc.)
- Descriptive file names (no `file1.md`, `test2.py`)

### 2. Code Style Consistency

- Python: English only, PEP 8, type hints
- Markdown: Hebrew allowed for docs, emojis allowed
- Consistent naming conventions

### 3. Multi-Agent Support (Optional)

If using multi-agent systems:
- 1:1 agent-advisor mapping enforced
- Structured output contracts
- Pipeline validation rules

## Best Practices

1. **Keep Rules Updated** - Review `.cursor/rules/` periodically
2. **Document Custom Rules** - Add project-specific rules as needed
3. **Follow Structure** - Don't create files in root (except README.md)
4. **Use Descriptive Names** - Follow naming conventions in rules
5. **Test Rules** - Verify rules work with your workflow

## Troubleshooting

### Rules Not Applying

- Check `.cursor/rules/` files have correct frontmatter
- Verify `globs` patterns match your files
- Ensure `alwaysApply: true` if needed

### File Placement Issues

- Review `repository_hygiene.mdc`
- Check `project_structure.mdc`
- Ensure files are in correct directories

### Multi-Agent Errors

- Verify `multi_agent.mdc` rules are followed
- Check pipeline YAML has required fields
- Ensure agents have matching advisors

## See Also

- **[Setup Guide](SETUP_TEMPLATE.md)** - Step-by-step setup instructions
- **[Template Checklist](TEMPLATE_CHECKLIST.md)** - Setup checklist
- **[README Template](readme_template.md)** - Template for your project README
- **[Multi-Agent Example](example_multi_agent_readme.md)** - Example README for multi-agent projects
- `.cursor/rules/README.mdc` - Overview of rules directory
- `.cursorrules` - Fallback rules file
- `docs/agents_and_advisors.md` - Multi-agent catalog (if using multi-agent systems)

## Quick Start Checklist

Use the [Template Checklist](TEMPLATE_CHECKLIST.md) to ensure you've completed all setup steps.

---

**Note:** This template is designed for Python projects but can be adapted for other languages by modifying the relevant rule files.

