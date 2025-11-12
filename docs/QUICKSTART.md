# Quick Start Guide

## Installation

```bash
# Clone or use as template
git clone <repo-url>
cd AgentsSystemV2

# Install dependencies
pip install -r requirements.txt

# Install pre-commit hooks (optional but recommended)
pip install pre-commit
pre-commit install
```

## Basic Usage

### 1. Run a Simple Pipeline

```bash
# Sequential execution with human-readable report
python cli.py --pipeline pipeline/example.yaml

# JSON output for scripts
python cli.py --pipeline pipeline/example.yaml --output json
```

### 2. Parallel Execution

```bash
# Run with parallel orchestrator (faster for independent steps)
python cli.py \
  --pipeline pipeline/with_codegen.yaml \
  --parallel \
  --max-workers 4
```

### 3. Save Artifacts

```bash
# Save all artifacts to filesystem
python cli.py \
  --pipeline pipeline/example.yaml \
  --save-artifacts

# Artifacts saved to: out/<run_id>/<stage>/
```

### 4. Auto-Refine on Failure

```bash
# Automatically run PromptRefiner when steps fail
python cli.py \
  --pipeline pipeline/example.yaml \
  --refine-on-fail
```

### 5. Fail-Fast Mode

```bash
# Stop on first failure
python cli.py \
  --pipeline pipeline/example.yaml \
  --fail-fast
```

## Complete Example

```bash
python cli.py \
  --pipeline pipeline/with_codegen.yaml \
  --parallel \
  --max-workers 4 \
  --output human \
  --save-artifacts \
  --refine-on-fail \
  --fail-fast \
  --mem product_idea="Build a todo app"
```

## Pipeline YAML Structure

```yaml
project_mode: mvp_fast_delivery

policy:
  score_thresholds:
    requirements: 0.80
    codegen: 0.90

stages:
  - name: requirements
    category: requirements
    agent: RequirementsDraftingAgent
    advisor: RequirementsAdvisor
    task: "Create PRD for: {product_idea}"
    max_retries: 1

  - name: code_skeleton
    category: codegen
    depends_on: [requirements]
    agent: CodeSkeletonAgent
    advisor: CodeReviewAdvisor
    task: "Generate HTML/CSS skeleton"
    max_retries: 1
```

## Output Formats

### Human-Readable (Markdown)

```bash
python cli.py --pipeline example.yaml --output human
```

Generates a markdown report with:
- Run summary (stages, approvals, average score)
- Stage details (status, score, artifacts, review)
- Critical issues and suggestions

### JSON

```bash
python cli.py --pipeline example.yaml --output json
```

Returns structured JSON for programmatic use.

## Artifact Management

### View Saved Artifacts

```bash
# After running with --save-artifacts
ls -R out/<run_id>/

# Example structure:
# out/abc123/
#   ├── SUMMARY.md
#   ├── requirements/
#   │   └── prd.md
#   └── code_skeleton/
#       ├── index.html
#       └── styles.css
```

### CI/CD Integration

```yaml
# .github/workflows/ci.yml
- name: Run pipeline
  run: |
    python cli.py \
      --pipeline pipeline/production.yaml \
      --parallel \
      --output human \
      --save-artifacts \
      --fail-fast

- name: Upload artifacts
  uses: actions/upload-artifact@v3
  with:
    name: pipeline-artifacts
    path: out/
```

## Using Advisor Council

For multi-advisor reviews (programmatic):

```python
from src.orchestrator.council import AdvisorCouncil
from src.orchestrator.factory import advisor_factory

council = AdvisorCouncil(
    advisor_factory=advisor_factory,
    advisors=["RequirementsAdvisor", "CodeReviewAdvisor"],
    decision="majority",
    min_score=0.85,
)

review = council.review(output=agent_output, task=task, context=context)
```

## Advanced Flags

- `--dry-run` — Validate YAML only (no execution)
- `--refine-on-fail` — Auto PromptRefiner on failed steps
- `--parallel --max-workers N` — DAG waves execution
- `--save-artifacts` — Persist artifacts under `out/<run_id>/`
- `--output human|json` — Console output format
- `--fail-fast` — Stop on first failure

## Common Workflows

### Development

```bash
# Fast iteration with relaxed thresholds
python cli.py \
  --pipeline pipeline/mvp.yaml \
  --output human
```

### Production

```bash
# Strict validation with all checks
python cli.py \
  --pipeline pipeline/production.yaml \
  --parallel \
  --output human \
  --save-artifacts \
  --fail-fast
```

### Debugging

```bash
# Save artifacts and generate detailed report
python cli.py \
  --pipeline pipeline/example.yaml \
  --save-artifacts \
  --output human \
  --mem debug_mode=true
```

### Validation Only

```bash
# Validate pipeline YAML without execution
python cli.py \
  --pipeline pipeline/example.yaml \
  --dry-run
```

## Next Steps

- Read [REPORTS_AND_ARTIFACTS.md](REPORTS_AND_ARTIFACTS.md) for detailed documentation
- Check [HOOKS_AND_PRE_COMMIT.md](HOOKS_AND_PRE_COMMIT.md) for hooks and quality gates
- See [PARALLEL_EXECUTION.md](PARALLEL_EXECUTION.md) for parallel execution details
- Review pipeline examples in `pipeline/` directory
