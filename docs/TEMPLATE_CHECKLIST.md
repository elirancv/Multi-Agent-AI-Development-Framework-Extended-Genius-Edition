# Template Setup Checklist

Use this checklist when setting up a new project from this template.

## ✅ Initial Setup

- [ ] Copied `.cursor/rules/` directory to new project
- [ ] Copied `.cursorrules` file to new project root
- [ ] Copied `.gitignore` file to new project root
- [ ] Read `docs/TEMPLATE_GUIDE.md` for overview
- [ ] Read `docs/SETUP_TEMPLATE.md` for detailed steps

## ✅ Project Customization

- [ ] Replaced `README.md` with project-specific content (use `docs/readme_template.md`)
- [ ] Updated `.cursorrules` with project-specific information (if needed)
- [ ] Customized `.gitignore` for project-specific ignores

## ✅ Multi-Agent System (Optional)

If **NOT** using multi-agent system:
- [ ] Removed `.cursor/rules/multi_agent.mdc`
- [ ] Removed `.cursor/rules/orchestrator.mdc`
- [ ] Removed `.cursor/rules/pipeline.mdc` (if not using pipelines)
- [ ] Removed `docs/agents_and_advisors.md`
- [ ] Removed `docs/agent_instructions.md`
- [ ] Removed `docs/example_multi_agent_readme.md`

If **USING** multi-agent system:
- [ ] Reviewed `docs/agents_and_advisors.md`
- [ ] Reviewed `docs/agent_instructions.md`
- [ ] Reviewed `docs/example_multi_agent_readme.md` for reference

## ✅ Project Structure

- [ ] Created `src/` directory (if needed)
- [ ] Created `tests/` directory (if needed)
- [ ] Created `config/` directory (if needed)
- [ ] Created `pipeline/` directory (if using pipelines)
- [ ] Verified no orphan files in root (except `README.md`)

## ✅ Python Setup (If Applicable)

- [ ] Created virtual environment
- [ ] Created `requirements.txt` or `pyproject.toml`
- [ ] Installed dependencies
- [ ] Verified Python version (3.8+)

## ✅ Git Setup (Optional)

- [ ] Initialized git repository
- [ ] Created initial commit
- [ ] Verified `.gitignore` is working
- [ ] Set up remote repository (if applicable)

## ✅ Rule Verification

- [ ] Created test Python file - rules applied correctly
- [ ] Created test markdown file - rules applied correctly
- [ ] Verified file placement rules work
- [ ] Verified code style rules work
- [ ] Tested Cursor AI suggestions

## ✅ Documentation

- [ ] Updated `README.md` with project description
- [ ] Created project-specific documentation in `docs/`
- [ ] Removed template-specific documentation (if not needed)
- [ ] Added project-specific documentation

## ✅ Final Checks

- [ ] All files follow repository hygiene rules
- [ ] No orphan files in root (except `README.md`)
- [ ] All markdown files (except `README.md`) are in `docs/`
- [ ] Code files are in `src/` or appropriate subdirectories
- [ ] Test files are in `tests/`
- [ ] Configuration files are in `config/`
- [ ] Pipeline files are in `pipeline/` (if applicable)

## ✅ Cleanup

- [ ] Removed template-specific files not needed for your project
- [ ] Removed example files
- [ ] Cleaned up any temporary files
- [ ] Verified `.gitignore` excludes temporary files

## 🎉 Ready to Code!

Once all items are checked, you're ready to start development with Cursor AI!

---

**Need Help?**
- See `docs/TEMPLATE_GUIDE.md` for detailed information
- See `docs/SETUP_TEMPLATE.md` for step-by-step instructions
- Check `.cursor/rules/README.mdc` for rule documentation
