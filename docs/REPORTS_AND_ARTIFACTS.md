# Reports and Artifacts

## Markdown Run Reports

Generate human-friendly markdown reports for pipeline runs.

### Usage

```bash
# Generate markdown report (default)
python cli.py --pipeline pipeline/example.yaml --output human

# JSON output (default)
python cli.py --pipeline pipeline/example.yaml --output json
```

### Report Contents

The markdown report includes:
- **Run ID** and generation timestamp
- **Summary** with stage counts, approval rates, average scores
- **Stage Details** with:
  - Approval status (✅/❌)
  - Score and category
  - Artifact list
  - Review summary (critical issues, suggestions)

### Example Output

```markdown
# Pipeline Run Report
- **Run ID:** `abc123`
- **Generated:** 2025-01-12T10:30:00Z

## Summary
- **Stages:** 3  |  **Approved:** 2  |  **Failed:** 1
- **Average Score:** 0.87

## Stages
### ✅ requirements  —  score: **0.95**  |  category: `requirements`
**Artifacts:**
- `prd.md` · type=`markdown`
**Review:**
- approved=True  |  score=0.95
- Suggestions:
  - Add more user stories
```

## Artifact Persistence

Save all artifacts to filesystem for CI/CD integration and debugging.

### Usage

```bash
# Save artifacts to out/<run_id>/<stage>/
python cli.py --pipeline pipeline/example.yaml --save-artifacts
```

### Directory Structure

```
out/
└── <run_id>/
    ├── SUMMARY.md
    ├── requirements/
    │   ├── prd.md
    │   └── spec.json
    └── code_skeleton/
        ├── index.html
        └── styles.css
```

### Programmatic Usage

```python
from src.orchestrator.artifact_sink import persist_artifacts

result = orch.run(steps)
run_dir = persist_artifacts(result, out_dir="out")
print(f"Artifacts saved to: {run_dir}")
```

## Advisor Council

Review agent output using multiple advisors and aggregate decisions.

### Decision Modes

- **majority** - Approve if majority of advisors approve
- **average** - Approve if average score meets threshold

### Usage

```python
from src.orchestrator.council import AdvisorCouncil
from src.orchestrator.factory import advisor_factory

council = AdvisorCouncil(
    advisor_factory=advisor_factory,
    advisors=["RequirementsAdvisor", "PromptRefinerAdvisor", "CodeReviewAdvisor"],
    decision="majority",
    min_score=0.85,
)

review = council.review(output=agent_output, task=task, context=context)
```

### Council Review Structure

The council aggregates:
- **Score** - Average of all advisor scores
- **Approved** - Based on decision mode (majority/average)
- **Critical Issues** - Combined from all advisors (capped at 10)
- **Suggestions** - Combined from all advisors (capped at 10)
- **Severity** - Calculated from critical issue count
- **Summary** - Includes vote count and average score

### Example

```python
# Single advisor (default)
review = advisor.review(output, task, context)

# Council of advisors
council = AdvisorCouncil(
    advisor_factory=advisor_factory,
    advisors=["RequirementsAdvisor", "CodeReviewAdvisor"],
    decision="majority",
    min_score=0.85,
)
review = council.review(output, task, context)
# Review includes aggregated feedback from both advisors
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
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

### Artifact Retention

Artifacts are stored under `out/<run_id>/` and can be:
- Uploaded to CI artifact storage
- Archived for compliance
- Used for debugging failed runs
- Shared with stakeholders

## Best Practices

1. **Use markdown reports** for human review and PR summaries
2. **Save artifacts** in CI/CD for traceability
3. **Use councils** for critical stages (production, security)
4. **Combine with hooks** - Council reviews can trigger refinement hooks
5. **Archive reports** - Keep markdown reports alongside artifacts

## CLI Flags Summary

```bash
# Output format
--output human    # Markdown report (default for human review)
--output json     # JSON output (default for scripts)

# Artifact persistence
--save-artifacts  # Save artifacts to out/<run_id>/

# Combined example
python cli.py \
  --pipeline pipeline/example.yaml \
  --parallel \
  --output human \
  --save-artifacts \
  --refine-on-fail
```

