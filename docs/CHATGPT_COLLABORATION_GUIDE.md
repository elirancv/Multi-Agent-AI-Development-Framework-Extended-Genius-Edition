# ChatGPT Collaboration Guide

**Purpose:** How to use ChatGPT effectively to help build this multi-agent system and communicate better with Cursor AI.

---

## 🎯 Strategy: ChatGPT + Cursor AI Together

### ChatGPT's Role
- **High-level planning** and architecture design
- **Code examples** and patterns
- **Problem-solving** complex logic
- **Documentation** and explanations
- **Learning** new concepts

### Cursor AI's Role (Me)
- **Project-specific** implementation
- **Following rules** and conventions
- **File placement** and structure
- **Repository hygiene** enforcement
- **Integration** with existing codebase

---

## 📋 Best Practices for ChatGPT Prompts

### 1. Architecture & Design Questions

**Good ChatGPT Prompts:**

```
"I'm building a multi-agent system where:
- Each agent inherits from BaseFunctionalAgent
- Agents return structured dicts: {content, artifacts, metadata}
- Each agent has a matching advisor that reviews output
- Advisors return: {score, approved, critical_issues, suggestions, summary, severity}

Help me design:
1. The BaseFunctionalAgent abstract class structure
2. How agents should handle context and shared memory
3. Error handling patterns for agent failures
4. How to structure the agent factory pattern"
```

**Why This Works:**
- Provides context about your project
- Asks for specific design patterns
- Gets reusable code examples
- Can be directly adapted to your codebase

### 2. Code Generation Requests

**Good ChatGPT Prompts:**

```
"Generate a Python class for ProductManagerAgent that:
- Inherits from BaseFunctionalAgent
- Implements process(context: dict[str, Any]) -> dict[str, Any]
- Takes user_prompt from context
- Returns structured dict with content, artifacts, metadata
- Follows PEP 8, uses type hints, English only
- Includes docstrings

Then generate the matching ProductManagerAdvisor that:
- Inherits from BaseAgent
- Implements review_output(shared_memory, agent_output, agent_name) -> dict
- Reviews the product manager's output
- Returns score (0.0-1.0), approved bool, critical_issues, suggestions, summary, severity"
```

**Why This Works:**
- Specific requirements
- Matches your project structure
- Gets code that follows your rules
- Can be copy-pasted and adapted

### 3. Problem-Solving Prompts

**Good ChatGPT Prompts:**

```
"I'm building an orchestrator that needs to:
- Load YAML pipeline files
- Validate that every agent has a matching advisor
- Execute stages in dependency order
- Handle failures and retries
- Support resume from checkpoints

What's the best architecture for this? Show me:
1. Pipeline loader class structure
2. Stage executor with dependency resolution
3. Error handling and retry logic
4. Checkpoint/resume mechanism"
```

**Why This Works:**
- Focuses on specific problems
- Gets architectural guidance
- Receives code examples
- Can be implemented step-by-step

### 4. Learning & Understanding Prompts

**Good ChatGPT Prompts:**

```
"Explain the difference between:
- Functional agents vs advisors vs cross-cutting agents
- How shared memory works in multi-agent systems
- The 1:1 agent-advisor mapping pattern
- When to use shared advisors vs primary advisors

Give me examples of each pattern."
```

**Why This Works:**
- Builds understanding
- Clarifies concepts
- Provides examples
- Helps you communicate better with Cursor AI

---

## 🔄 Workflow: ChatGPT → Cursor AI

### Step 1: Use ChatGPT for Planning

**Ask ChatGPT:**
```
"I need to build 28 functional agents for a multi-agent system.
Help me:
1. List all 28 agents by category
2. Design the base class structure
3. Create a template for agent implementation
4. Plan the testing strategy"
```

**Result:** Get architecture, templates, and planning

### Step 2: Bring to Cursor AI (Me)

**Say to me:**
```
"I got this agent template from ChatGPT. Can you:
1. Create the file in src/agents/ following our rules?
2. Add proper type hints and docstrings?
3. Create the matching test file in tests/?
4. Ensure it follows repository hygiene rules?"
```

**Result:** I implement it correctly in your project

### Step 3: Iterate

**Ask ChatGPT:**
```
"I implemented ProductManagerAgent but it's not handling errors well.
Show me best practices for:
- Input validation
- Error handling in agent process() method
- Logging errors properly
- Returning error states in structured dict"
```

**Then ask me:**
```
"Update ProductManagerAgent with better error handling based on ChatGPT's suggestions"
```

---

## 💡 Specific Use Cases

### Use Case 1: Creating New Agent

**ChatGPT Prompt:**
```
"Create a BackendDeveloperAgent class that:
- Inherits from BaseFunctionalAgent
- Takes architecture spec from context
- Generates FastAPI endpoint code
- Returns code files as artifacts
- Includes proper error handling

Show me the complete implementation with:
- Class definition
- process() method
- Helper methods
- Error handling
- Type hints and docstrings"
```

**Then tell me:**
```
"Create src/agents/backend_developer.py with this code, 
and create tests/test_backend_developer.py following our testing rules"
```

### Use Case 2: Designing Orchestrator

**ChatGPT Prompt:**
```
"Design an orchestrator system for multi-agent pipelines:
- Loads YAML pipeline definitions
- Validates agent-advisor mappings (1:1 rule)
- Executes stages with dependencies
- Runs cross-cutting agents on every stage
- Handles CEO decisions (PROCEED/RERUN/ROLLBACK/FINALIZE)
- Supports resume from checkpoints

Show me:
1. Main Orchestrator class structure
2. Pipeline loader with validation
3. Stage executor
4. Decision engine
5. Resume system"
```

**Then tell me:**
```
"Create the orchestrator structure in src/orchestrator/ 
following our project rules. Use ChatGPT's design as reference"
```

### Use Case 3: Writing Tests

**ChatGPT Prompt:**
```
"Generate pytest tests for ProductManagerAgent that verify:
- process() returns correct structure
- artifacts are valid file paths
- metadata contains required fields
- Error handling works correctly
- Edge cases are covered

Use pytest fixtures and mocks where appropriate."
```

**Then tell me:**
```
"Create tests/test_product_manager.py with these tests,
following our testing rules and file structure"
```

---

## 🎨 Prompt Templates

### Template 1: Agent Creation

```
"I need to create a [AGENT_NAME] agent for my multi-agent system.

Requirements:
- Inherits from BaseFunctionalAgent
- Implements process(context: dict[str, Any]) -> dict[str, Any]
- Takes [INPUT] from context
- Generates [OUTPUT_TYPE]
- Returns structured dict with content, artifacts, metadata

Constraints:
- Python 3.8+
- Type hints required
- PEP 8 compliant
- English only (no Hebrew, no emojis)
- Proper error handling

Generate the complete class with:
1. Class definition
2. process() method
3. Helper methods
4. Error handling
5. Docstrings
6. Type hints"
```

### Template 2: Advisor Creation

```
"I need to create a [ADVISOR_NAME] advisor for my multi-agent system.

Requirements:
- Inherits from BaseAgent
- Implements review_output(shared_memory, agent_output, agent_name) -> dict
- Reviews [AGENT_NAME] output
- Returns: {score, approved, critical_issues, suggestions, summary, severity}

Review Criteria:
- [CRITERIA_1]
- [CRITERIA_2]
- [CRITERIA_3]

Generate the complete class with:
1. Class definition
2. review_output() method
3. Review logic
4. Scoring algorithm (0.0-1.0)
5. Error handling
6. Docstrings
7. Type hints"
```

### Template 3: Architecture Design

```
"I'm building a [COMPONENT] for my multi-agent system.

Context:
- [DESCRIPTION_OF_COMPONENT]
- Needs to integrate with [OTHER_COMPONENTS]
- Must follow [CONSTRAINTS]

Requirements:
- [REQUIREMENT_1]
- [REQUIREMENT_2]
- [REQUIREMENT_3]

Help me design:
1. Class structure
2. Key methods
3. Integration points
4. Error handling
5. Testing strategy

Show me code examples."
```

---

## 📝 What to Ask ChatGPT About

### ✅ Good Topics for ChatGPT

1. **Architecture & Design Patterns**
   - "How to design a multi-agent orchestrator?"
   - "What's the best pattern for agent factories?"
   - "How to handle shared memory in multi-agent systems?"

2. **Code Examples**
   - "Show me a FastAPI endpoint example"
   - "How to parse YAML files in Python?"
   - "Best practices for error handling in Python?"

3. **Algorithms & Logic**
   - "How to resolve dependencies in a DAG?"
   - "Best algorithm for scoring agent output?"
   - "How to implement checkpoint/resume?"

4. **Learning**
   - "Explain the observer pattern"
   - "What is dependency injection?"
   - "How does pytest work?"

### ❌ Not Ideal for ChatGPT

1. **Project-Specific Implementation**
   - "Create src/agents/product_manager.py" → Ask me instead
   - "Where should I put this file?" → Ask me (I know the rules)
   - "Does this follow our rules?" → Ask me (I enforce rules)

2. **File Structure**
   - "What's the correct directory structure?" → Check docs/ or ask me
   - "Where do tests go?" → Ask me (tests/ directory)

3. **Rule Enforcement**
   - "Is this code compliant?" → Ask me (I check rules)
   - "Should this be in docs/ or src/?" → Ask me (I know placement rules)

---

## 🔗 Communication Flow

### Example: Building ProductManagerAgent

**1. Ask ChatGPT:**
```
"Design a ProductManagerAgent that takes user prompts and generates 
product requirements documents. Show me the class structure, 
process method, and error handling."
```

**2. Get ChatGPT's Response:**
- Class structure
- Code example
- Best practices

**3. Bring to Me (Cursor AI):**
```
"I got this ProductManagerAgent design from ChatGPT. 
Can you:
1. Create src/agents/product_manager.py following our rules?
2. Ensure it follows code_style.mdc (English only, type hints)?
3. Create tests/test_product_manager.py?
4. Verify it matches our agent contract?"
```

**4. I Implement:**
- Create file in correct location
- Follow all rules
- Add proper structure
- Create tests

**5. Iterate:**
```
"ChatGPT suggested adding input validation. 
Can you update ProductManagerAgent with validation?"
```

---

## 🎓 Learning Path

### Week 1: Foundation
**ChatGPT:**
- "Explain multi-agent systems architecture"
- "What is the observer pattern?"
- "How do orchestrators work?"

**Then ask me:**
- "Create the base classes based on ChatGPT's explanation"
- "Set up the project structure"

### Week 2: First Agents
**ChatGPT:**
- "Show me agent implementation examples"
- "How to structure agent output?"
- "Best practices for agent error handling"

**Then ask me:**
- "Create 3 agents following ChatGPT's patterns"
- "Ensure they follow our rules"

### Week 3: Orchestrator
**ChatGPT:**
- "Design a pipeline orchestrator"
- "How to handle dependencies?"
- "Resume/checkpoint patterns"

**Then ask me:**
- "Implement orchestrator based on ChatGPT's design"
- "Add pipeline validation"

---

## 📚 Reference Prompts

### For Architecture Questions
```
"I'm building [COMPONENT]. Help me understand:
- What patterns to use?
- How to structure it?
- Best practices?
- Common pitfalls to avoid?"
```

### For Code Generation
```
"Generate [COMPONENT] that:
- [REQUIREMENT_1]
- [REQUIREMENT_2]
- [REQUIREMENT_3]
- Follows [CONSTRAINTS]
- Includes [FEATURES]"
```

### For Problem Solving
```
"I'm having trouble with [PROBLEM]. 
Context: [CONTEXT]
Error: [ERROR]
What I tried: [ATTEMPTS]
Help me solve this."
```

### For Learning
```
"Explain [CONCEPT] in the context of:
- Multi-agent systems
- Python best practices
- Software architecture
Give me examples."
```

---

## ✅ Checklist: Using ChatGPT Effectively

- [ ] Provide context about your project
- [ ] Specify requirements clearly
- [ ] Ask for code examples
- [ ] Request explanations when learning
- [ ] Get multiple approaches/options
- [ ] Ask for best practices
- [ ] Request error handling examples
- [ ] Ask for testing strategies

---

## 🚫 What NOT to Do

- ❌ Don't ask ChatGPT to create files in your project (ask me)
- ❌ Don't ask ChatGPT about your specific file structure (ask me)
- ❌ Don't ask ChatGPT to enforce your rules (ask me)
- ❌ Don't copy-paste ChatGPT code without adapting it
- ❌ Don't skip bringing ChatGPT's output to me

---

## 💬 Example Conversation Flow

**You → ChatGPT:**
```
"Design a ProductManagerAgent for my multi-agent system..."
```

**ChatGPT → You:**
```
[Provides design and code example]
```

**You → Me (Cursor AI):**
```
"I got this ProductManagerAgent design from ChatGPT. 
Can you create it in src/agents/ following our rules?"
```

**Me → You:**
```
[Creates file, follows rules, adds tests]
```

**You → ChatGPT:**
```
"The agent works but needs better error handling. 
Show me best practices..."
```

**ChatGPT → You:**
```
[Provides error handling patterns]
```

**You → Me:**
```
"Update ProductManagerAgent with better error handling 
based on ChatGPT's suggestions"
```

**Me → You:**
```
[Updates code, maintains rules compliance]
```

---

## 🎯 Key Takeaway

**ChatGPT = Design & Learning**  
**Cursor AI (Me) = Implementation & Rules**

Use ChatGPT for:
- Architecture design
- Code examples
- Learning concepts
- Problem-solving

Use me (Cursor AI) for:
- Creating files in correct locations
- Following project rules
- Enforcing conventions
- Integration with codebase

**Together we build better!** 🚀

---

## 📖 Quick Reference

**When to use ChatGPT:**
- "How do I design X?"
- "Show me an example of Y"
- "Explain Z concept"
- "What's the best way to handle W?"

**When to use me (Cursor AI):**
- "Create file X in location Y"
- "Does this follow our rules?"
- "Where should this file go?"
- "Update X to follow our conventions"
- "Create tests for Y"

---

**Remember:** ChatGPT gives you the "what" and "how", I help you implement it correctly in your project! 🎯

