# Backfill Test Plan - v1.0.1

Systematic test backfill plan to achieve comprehensive coverage and catch regressions.

## 🎯 Goals

- **Core/Orchestrator**: 90-95% coverage
- **Agents/Advisors**: 80% coverage
- **Contract tests**: All agents/advisors
- **E2E tests**: CLI happy paths + failure gates
- **Property tests**: Templating, cache, budget

## 📊 Step 1: Coverage Gap Analysis (90 min)

### Run Coverage Report

```bash
coverage run -m pytest
coverage html
# Open htmlcov/index.html
```

### Priority Order

1. **Core** (`src/core/`) - Target: 95%
   - `base.py` - BaseFunctionalAgent, BaseAdvisor contracts
   - `types.py` - AgentOutput, AdvisorReview validation
   - `memory.py` - SharedMemory operations
   - `resume.py` - Checkpoint/Resume logic

2. **Orchestrator** (`src/orchestrator/`) - Target: 90%
   - `runner.py` - Sequential orchestrator
   - `runner_parallel.py` - Parallel orchestrator
   - `factory.py` - Agent/Advisor factories
   - `yaml_loader.py` - Pipeline loading/validation
   - `task_render.py` - Template rendering
   - `cache.py` - Output caching
   - `budget.py` - Budget guards

3. **Agents** (`src/agents/`) - Target: 80%
   - Contract compliance
   - Basic functionality

4. **Advisors** (`src/advisors/`) - Target: 80%
   - Contract compliance
   - Review logic

### Top 10 Low Coverage Files

Run this to identify:
```bash
coverage report --sort=cover | head -15
```

**Action**: Create backfill tasks for each file below threshold.

## 🧪 Step 2: Cross-System Tests (Big Eggs First)

### Orchestrator E2E CLI Tests

**Priority**: High
**Files**: `tests/test_cli_e2e_backfill.py`

**Scenarios**:
- [ ] Happy path (sequential)
- [ ] Happy path (parallel)
- [ ] With/without cache
- [ ] With policy council
- [ ] Failure gates (timeout, invalid output, exhausted retries)
- [ ] Resume/checkpoint (FS + SQLite)

### YAML Loader Tests

**Priority**: High
**Files**: `tests/test_yaml_loader_backfill.py`

**Scenarios**:
- [ ] All policy variations (thresholds, timeouts, retries, advisor weights)
- [ ] Dependencies (cycles, missing deps)
- [ ] Invalid YAML handling
- [ ] Missing agent/advisor classes

### Artifact Sink & Report Tests

**Priority**: Medium
**Files**: `tests/test_artifacts_backfill.py`

**Scenarios**:
- [ ] Binary artifacts
- [ ] manifest.json generation
- [ ] Relative links
- [ ] Report diffs between runs

## 📋 Step 3: Contract Tests

**Priority**: Critical
**Files**: `tests/test_contracts_backfill.py`

**Requirements**:
- [ ] All agents return AgentOutput with correct structure
- [ ] All advisors return AdvisorReview with correct structure
- [ ] Type validation
- [ ] Required fields present

## ✅ Step 4: Approval Tests (Goldens)

**Priority**: Medium
**Files**: `tests/test_approval_backfill.py`

**Scenarios**:
- [ ] Markdown report snapshots
- [ ] JSONL eventlog snapshots
- [ ] Pipeline graph snapshots

## 🔬 Step 5: Property-Based Tests

**Priority**: Medium
**Files**: `tests/test_property_backfill.py`

**Scenarios**:
- [ ] Task templating (Jinja2 edge cases)
- [ ] Cache key generation
- [ ] Budget guard calculations

## 📈 Execution Order

1. **Contracts + YAML Loader** (cheap, covers a lot)
2. **CLI E2E** (sequential/parallel)
3. **Report/Artifacts** (binary + manifest + diffs)
4. **Cache/Resume/Policy gates**
5. **Property/Fuzz** (templating, cache key, budget guard)

## 🚦 PR Gates

Before PR merge:
- [ ] `pytest -q` passes
- [ ] `python scripts/smoke_test.py --skip-slow` passes
- [ ] Codecov ≥ thresholds (core 95%, orchestrator 90%, agents/advisors 80%)
- [ ] `pre-commit run --all-files` passes
- [ ] `mypy .` passes (if configured)

## 📝 Tracking

### Coverage Progress

| Component | Current | Target | Status |
|-----------|---------|--------|--------|
| Core | ?% | 95% | ⏳ |
| Orchestrator | ?% | 90% | ⏳ |
| Agents | ?% | 80% | ⏳ |
| Advisors | ?% | 80% | ⏳ |

### Test Files Created

- [x] `tests/test_contracts_backfill.py` - Contract tests for all agents/advisors
- [x] `tests/test_cli_e2e_backfill.py` - CLI E2E tests (dry-run, flags, etc.)
- [x] `tests/test_yaml_loader_backfill.py` - YAML loader tests (policy, dependencies, validation)
- [ ] `tests/test_artifacts_backfill.py` - Artifact sink & report tests (TODO)
- [x] `tests/test_approval_backfill.py` - Approval/golden snapshot tests
- [x] `tests/test_property_backfill.py` - Property-based tests (templating, cache, budget)
- [x] `tests/test_orchestrator_backfill.py` - Orchestrator tests (timeouts, retries, council weights)

## See Also

- [Testing Requirements](.cursor/rules/testing.mdc)
- [Success Metrics](SUCCESS_METRICS.md)
