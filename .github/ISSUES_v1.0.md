# v1.0 Tracking Issues (Ready to Open)

Copy these issues to GitHub Issues. Each issue is ready to use.

---

## Issue 1: SQLite CheckpointStore

**Title**: `[P0] SQLite CheckpointStore for atomic operations and fast queries`

**Labels**: `enhancement`, `p0`, `v1.0`, `infrastructure`

**Body**:
```markdown
## Description

Replace or complement filesystem-based checkpoint store with SQLite for:
- Atomic save operations
- Fast queries (find by run_id, step_index, date range)
- Better reliability and recovery

## Current Implementation

Filesystem-based store (`FileCheckpointStore`) works but:
- No atomicity guarantees
- Slow queries (filesystem glob)
- No date range queries

## Proposed Solution

Create `SQLiteCheckpointStore` that:
- Uses SQLite database (`checkpoints.db`)
- Provides atomic save/load operations
- Supports fast queries: `find_by_run_id()`, `find_by_date_range()`, `find_latest()`
- Maintains backward compatibility (can migrate from FS)

## Tasks

- [ ] Create `src/orchestrator/checkpoint_sqlite.py`
- [ ] Implement `SQLiteCheckpointStore` class
- [ ] Add migration utility (FS → SQLite)
- [ ] Update `CheckpointStore` interface if needed
- [ ] Add tests (`tests/test_checkpoint_sqlite.py`)
- [ ] Update CLI to support `--checkpoint-store sqlite|fs`
- [ ] Update documentation

## Acceptance Criteria

- [ ] SQLite store passes all existing checkpoint tests
- [ ] Atomic save operations (no partial writes)
- [ ] Fast queries (< 10ms for find_latest)
- [ ] Migration utility works
- [ ] Backward compatible with FS store

## Effort Estimate

1-1.5 days
```

---

## Issue 2: Artifact Retention Policy + Clean Command

**Title**: `[P0] Artifact Retention Policy and Clean Command`

**Labels**: `enhancement`, `p0`, `v1.0`, `ops`

**Body**:
```markdown
## Description

Implement automatic artifact cleanup with retention policies:
- Time-based retention (keep artifacts for N days)
- Size-based limits (max size per run, max total size)
- Keep latest N runs
- CLI command: `multiagent clean` with dry-run

## Use Cases

- Cleanup old artifacts automatically
- Prevent disk space issues
- Keep only relevant artifacts
- Dry-run before cleanup

## Proposed Solution

### CLI Command
```bash
multiagent clean --older-than 7d --max-size 2GB --keep-latest 10 --dry-run
```

### Configuration
```yaml
# policy.yaml
artifact_retention:
  max_age_days: 7
  max_size_per_run: "500MB"
  max_total_size: "2GB"
  keep_latest_runs: 10
```

## Tasks

- [ ] Add `clean` command to CLI
- [ ] Implement retention policy logic
- [ ] Add size calculation utilities
- [ ] Add dry-run mode
- [ ] Generate cleanup report
- [ ] Add tests
- [ ] Update documentation

## Acceptance Criteria

- [ ] `multiagent clean --dry-run` shows what would be deleted
- [ ] Cleanup respects retention policies
- [ ] Cleanup report shows deleted files and freed space
- [ ] Tests cover all retention scenarios
- [ ] Documentation updated

## Effort Estimate

0.5-1 day
```

---

## Issue 3: API Documentation Generator

**Title**: `[P1] API Documentation Generator (pdoc/pydoc-markdown)`

**Labels**: `enhancement`, `p1`, `v1.0`, `documentation`

**Body**:
```markdown
## Description

Generate API documentation automatically from docstrings:
- Output to `docs/api/`
- Auto-generate on CI/release
- Link from `docs/INDEX.md`
- Searchable and browsable

## Tools

- **pdoc**: Simple, fast, Python-native
- **pydoc-markdown**: More features, Markdown output

## Proposed Solution

1. Use `pdoc` for HTML generation
2. Add CI step to generate docs
3. Link from `docs/INDEX.md`
4. Add to release bundle

## Tasks

- [ ] Install pdoc: `pip install pdoc`
- [ ] Configure pdoc for `src/orchestrator/*` and `src/core/*`
- [ ] Add CI step to generate `docs/api/`
- [ ] Update `docs/INDEX.md` with API link
- [ ] Add to release bundle workflow
- [ ] Test locally

## Acceptance Criteria

- [ ] `docs/api/index.html` generated automatically
- [ ] All public APIs documented
- [ ] CI generates docs on release
- [ ] Link from INDEX.md works
- [ ] Docs are searchable

## Effort Estimate

0.5 day
```

---

## Issue 4: Hard Tests Nightly + KPIs

**Title**: `[P1] Hard Tests Nightly Workflow with KPIs`

**Labels**: `enhancement`, `p1`, `v1.0`, `testing`, `ci`

**Body**:
```markdown
## Description

Create nightly workflow that runs comprehensive tests:
- Large pipeline (10+ stages)
- Parallel execution
- Budget enforcement
- Resume functionality
- Track KPIs: execution time, budget compliance, success rate

## KPIs to Track

- Average pipeline execution time (target: < 5 min)
- Budget violations (target: 0)
- Test success rate (target: > 95%)
- Resume success rate (target: 100%)

## Proposed Solution

### Workflow
```yaml
name: Hard Tests Nightly
on:
  schedule:
    - cron: '0 2 * * *'  # 2 AM UTC
  workflow_dispatch:
```

### Test Pipeline
- Create `pipeline/hard_test.yaml` with 10+ stages
- Run with parallel execution
- Test resume functionality
- Enforce budget limits
- Generate KPI report

## Tasks

- [ ] Create `pipeline/hard_test.yaml`
- [ ] Create `scripts/hard_test.py` with KPI tracking
- [ ] Add nightly workflow (`.github/workflows/hard-tests-nightly.yml`)
- [ ] Generate KPI report (JSON + Markdown)
- [ ] Upload artifacts
- [ ] Add KPI dashboard (optional)

## Acceptance Criteria

- [ ] Nightly workflow runs successfully
- [ ] KPI report generated
- [ ] KPIs tracked: time, budget, success rate
- [ ] Artifacts uploaded
- [ ] Workflow runs on schedule

## Effort Estimate

1-2 days
```

---

## Issue 5: Council Presets in YAML

**Title**: `[P1] Council Presets (YAML Shortcuts for Common Profiles)`

**Labels**: `enhancement`, `p1`, `v1.0`, `configuration`

**Body**:
```markdown
## Description

Create YAML shortcuts for common council configurations:
- MVP Fast: Light advisors, lower thresholds
- Production: Full advisors, strict thresholds
- Research: Experimental, relaxed scoring

## Use Case

Instead of:
```yaml
council:
  advisors: [Advisor1, Advisor2, ...]
  decision: average
  weights: {...}
```

Use:
```yaml
council_preset: mvp-fast
```

## Proposed Solution

### Preset Definitions
```yaml
# config/presets.yaml
presets:
  mvp-fast:
    advisors: [ProductManagerAdvisor, CodeReviewAdvisor]
    decision: average
    min_score: 0.7
    weights: {}
  
  production:
    advisors: [ProductManagerAdvisor, CodeReviewAdvisor, SecurityAdvisor, ...]
    decision: average
    min_score: 0.85
    weights: {SecurityAdvisor: 1.5}
```

## Tasks

- [ ] Create `config/presets.yaml`
- [ ] Add preset loader to YAML loader
- [ ] Update schema validation
- [ ] Add CLI flag: `--preset <name>`
- [ ] Add tests
- [ ] Update documentation with examples

## Acceptance Criteria

- [ ] Presets load correctly
- [ ] `--preset mvp-fast` works
- [ ] Presets expand to full council config
- [ ] Tests pass
- [ ] Documentation updated

## Effort Estimate

0.5 day
```

---

## Issue 6: Pipelines Gallery

**Title**: `[P2] Pipelines Gallery with Examples and Screenshots`

**Labels**: `enhancement`, `p2`, `v1.0`, `documentation`

**Body**:
```markdown
## Description

Create a gallery of example pipelines:
- Use cases and descriptions
- Screenshots/visualizations
- Pipeline graphs (DOT/PNG)
- Best practices

## Structure

```
docs/pipelines/
├── index.md
├── mvp-fast.md
├── production.md
├── research.md
└── images/
    ├── mvp-fast.png
    └── production.png
```

## Content

Each pipeline page should include:
- Use case description
- Pipeline YAML
- Visual graph (PNG)
- Execution example
- Best practices

## Tasks

- [ ] Create `docs/pipelines/` directory
- [ ] Generate pipeline graphs (DOT → PNG)
- [ ] Write pipeline documentation
- [ ] Add screenshots/examples
- [ ] Link from README.md
- [ ] Add to docs/INDEX.md

## Acceptance Criteria

- [ ] Gallery accessible from README
- [ ] All example pipelines documented
- [ ] Visual graphs included
- [ ] Examples work out-of-the-box
- [ ] Best practices documented

## Effort Estimate

1-2 days
```

---

## How to Use

1. Copy each issue body
2. Go to GitHub Issues → New Issue
3. Paste the body
4. Add labels
5. Assign to milestone: v1.0
6. Submit

---

**Total Effort Estimate**: 7-10 days for P0+P1, 2-4 days for P2 (optional)

