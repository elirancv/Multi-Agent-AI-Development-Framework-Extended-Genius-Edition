# Cursor AI Python Project Template

> **This is a reusable template** for Python development projects with Cursor AI. It includes comprehensive rules, project structure guidelines, and best practices.

## 🎯 What's This?

This template provides a **complete Cursor AI ruleset** for Python projects, including:

- ✅ **Comprehensive Rules** - Code style, project structure, repository hygiene
- ✅ **Multi-Agent Support** - Optional rules for multi-agent systems
- ✅ **File Type Rules** - Python, JavaScript, HTML, CSS, SQL, Docker, YAML, JSON, TOML
- ✅ **Best Practices** - Enforced through Cursor rules

## 🚀 Quick Start

### Using This Template

1. **Copy the rules structure:**
   ```bash
   # Copy to your new project
   cp -r .cursor/ your-new-project/
   cp .cursorrules your-new-project/
   cp .gitignore your-new-project/
   ```

2. **Customize for your project:**
   - Replace `README.md` with your project description (see `docs/readme_template.md`)
   - Remove multi-agent rules if not needed (see `docs/TEMPLATE_GUIDE.md`)
   - Adjust rules as needed

3. **Start coding:**
   - Cursor will automatically apply rules based on file types
   - Rules enforce structure, style, and best practices

## 📁 Project Structure

```
project_root/
├── README.md                # This file (project overview)
├── .cursorrules             # Cursor AI fallback rules
├── .cursor/
│   └── rules/              # Detailed rules by topic (.mdc files)
├── docs/                    # Documentation
│   ├── TEMPLATE_GUIDE.md   # How to use this template
│   ├── readme_template.md  # Template for your README
│   └── SETUP_TEMPLATE.md   # Step-by-step setup guide
├── src/                     # Source code (create when needed)
├── tests/                   # Tests (create when needed)
├── config/                  # Configuration files (create when needed)
└── pipeline/                # Pipeline definitions (optional)
```

## 📚 Documentation

- **[Template Guide](docs/TEMPLATE_GUIDE.md)** - Complete guide on using this template
- **[Setup Instructions](docs/SETUP_TEMPLATE.md)** - Step-by-step setup guide
- **[README Template](docs/readme_template.md)** - Template for your project README
- **[Multi-Agent Example](docs/example_multi_agent_readme.md)** - Example README for multi-agent projects

## 🎨 What Rules Are Included?

### Core Rules (Always Apply)
- **Project Structure** - Directory layout, file naming, repository hygiene
- **Code Style** - Python conventions, PEP 8, type hints, English only
- **Repository Hygiene** - File placement, no orphan files, clean structure

### Optional Rules (Apply Based on File Types)
- **Multi-Agent** - Agent/advisor contracts, 1:1 mapping, orchestrator validation
- **Pipeline** - YAML structure, dependencies, shared advisors
- **Testing** - Pytest patterns, coverage requirements
- **File Types** - CSS, HTML, JavaScript, SQL, Docker, YAML, JSON, TOML, env files

### Rule Files
See `.cursor/rules/README.mdc` for complete list of rule files.

## 🔧 Customization

### For Non-Multi-Agent Projects

If you're not building a multi-agent system, you can remove:
- `multi_agent.mdc`
- `orchestrator.mdc`
- `pipeline.mdc` (unless you use pipelines for other purposes)
- `docs/agents_and_advisors.md`
- `docs/agent_instructions.md`
- `docs/example_multi_agent_readme.md`

### For Different Languages

The template includes support for:
- Python (primary)
- JavaScript/TypeScript
- HTML/CSS
- SQL
- Shell scripts

Add language-specific rules as needed.

## 📖 Key Features

### 1. Repository Hygiene Enforcement

Rules automatically enforce:
- ✅ No orphan files in root (except `README.md`)
- ✅ Proper file placement (code → `src/`, docs → `docs/`, etc.)
- ✅ Descriptive file names (no `file1.md`, `test2.py`)

### 2. Code Style Consistency

- ✅ Python: English only, PEP 8, type hints
- ✅ Markdown: Hebrew allowed for docs, emojis allowed
- ✅ Consistent naming conventions

### 3. Multi-Agent Support (Optional)

If using multi-agent systems:
- ✅ 1:1 agent-advisor mapping enforced
- ✅ Structured output contracts
- ✅ Pipeline validation rules

## 🎓 Learning Resources

- [Cursor Rules Documentation](https://cursor.com/docs/context/rules)
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Project Structure Best Practices](docs/TEMPLATE_GUIDE.md)

## 📝 Next Steps

1. **Read the [Template Guide](docs/TEMPLATE_GUIDE.md)** for detailed instructions
2. **Follow [Setup Instructions](docs/SETUP_TEMPLATE.md)** to customize for your project
3. **Replace this README** with your project description (use `docs/readme_template.md`)
4. **Start coding** - Cursor will enforce the rules automatically

## 🤝 Contributing

This template is designed to be customized. Feel free to:
- Add project-specific rules
- Modify existing rules to fit your needs
- Share improvements back to the template

## 📄 License

(Add your license here)

---

**Note:** This template uses Cursor AI rules. See `.cursor/rules/README.mdc` for rule documentation.

**Template Version:** 2.0.0  
**Last Updated:** 2025-01-12
