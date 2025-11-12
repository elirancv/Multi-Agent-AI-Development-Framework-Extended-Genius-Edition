# General Agent Instructions

This file provides general instructions for all AI agents working on this multi-agent development project.

## Your Role

You are an AI assistant helping develop a **multi-agent system** where:

- **Functional Agents** produce deliverables (specs, code, docs)
- **Expert Advisors** review deliverables with domain expertise
- **CEO Orchestrator** makes decisions (proceed/rerun/rollback)
- **Meta Coordinator** orchestrates the entire pipeline

## Key Principles

### 1. Consistency
- Follow project conventions
- Use established patterns
- Maintain code style

### 2. Quality
- Produce structured outputs
- Include proper error handling
- Write clear, maintainable code

### 3. Collaboration
- Build on previous agent outputs
- Use shared memory for context
- Follow feedback loops

## Output Format

### Agents Must Return:
```python
{
    "content": "Main output as string",
    "artifacts": ["docs/output.md"],
    "metadata": {
        "stage": "requirements",
        "agent": "ProductManager",
    },
}
```

### Advisors Must Return:
```python
{
    "score": 0.87,                    # float 0.0–1.0
    "approved": True,                  # bool
    "critical_issues": [],            # list[str]
    "suggestions": ["Add examples"],  # list[str]
    "feedback": [],                   # list[dict]
    "summary": "Solid draft.",
    "severity": "medium",             # "low" | "medium" | "high"
}
```

## Rules

- **Language:** Python code in English only, no Hebrew, no emojis
- **Structure:** Follow project directory structure
- **Testing:** Include tests for new code
- **Documentation:** Document your changes

## When in Doubt

- Check `.cursor/rules/` for specific guidelines
- Follow patterns from existing code
- Ask for clarification if needed

---

**See Also:**
- `.cursor/rules/` - Detailed rules by topic
- `agents/<agent>/AGENTS.md` - Agent-specific instructions

