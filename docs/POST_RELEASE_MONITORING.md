# Post-Release Monitoring - 90 Day Tracking

Key metrics to monitor after v1.0.0 release.

## 🎯 Success Metrics (30-90 days)

### Nightly Hard Tests
- **Target**: ≥ 95% green rate
- **Measurement**: `.github/workflows/hard-tests-nightly.yml` success rate
- **Tracking**: GitHub Actions workflow runs
- **Frequency**: Daily (scheduled at 2 AM UTC)

**How to Check**:
```bash
# View workflow runs
gh run list --workflow=hard-tests-nightly.yml

# View latest run
gh run view --workflow=hard-tests-nightly.yml --log
```

### Performance
- **Target**: Runtime ↓ 20% in `hard_test.yaml` pipeline
- **Measurement**: Compare KPI baseline (`docs/benchmarks/baseline_latest.json`) vs current
- **Tracking**: Weekly KPI reports from nightly tests

**Baseline**: See `docs/benchmarks/baseline_latest.json`

**Compare**:
```bash
# Generate new baseline
python scripts/perf_baseline.py

# Compare
diff docs/benchmarks/baseline_latest.json docs/benchmarks/baseline_*.json
```

### Code Coverage
- **Overall**: ≥ 85%
- **Core**: ≥ 95%
- **Orchestrator**: ≥ 90%
- **Agents/Advisors**: ≥ 80%
- **Measurement**: Codecov reports (component flags)
- **Tracking**: Weekly Codecov reports

**View Dashboard**: https://codecov.io/gh/<owner>/<repo>

**Component Flags**:
- `core` - Core types/base classes
- `orchestrator` - Orchestrator logic
- `agents` - Agent implementations
- `advisors` - Advisor implementations

### Plugin Ecosystem
- **Target**: At least 1 external "Hello-World" plugin passes CI
- **Measurement**: `.github/workflows/plugin-api-test.yml` with external plugin
- **Tracking**: GitHub Actions workflow runs

**How to Check**:
```bash
# View plugin API test runs
gh run list --workflow=plugin-api-test.yml

# Check for external plugins
# (Currently uses internal test plugin, external plugins will show up here)
```

## 📊 Tracking Schedule

### Daily
- [ ] Check nightly test status
- [ ] Review any failures

### Weekly
- [ ] Review KPI reports
- [ ] Check coverage trends
- [ ] Analyze performance metrics
- [ ] Review plugin ecosystem status

### Monthly
- [ ] Aggregate metrics
- [ ] Compare to targets
- [ ] Identify regressions
- [ ] Update baseline if needed

## 📈 Baseline (v1.0.0)

### Initial Baseline
- **Nightly Tests**: First run after release
- **Performance**: `docs/benchmarks/baseline_latest.json`
- **Coverage**: Initial coverage report
- **Plugins**: 0 external plugins

### Update Baseline
```bash
# Generate new baseline
python scripts/perf_baseline.py

# Baseline saved to: docs/benchmarks/baseline_*.json
```

## 🎯 Success Criteria

### 30 Days
- [ ] Nightly tests: ≥ 90% green
- [ ] Coverage: Overall ≥ 80%, Core ≥ 90%
- [ ] No critical regressions
- [ ] Performance: Baseline established

### 60 Days
- [ ] Nightly tests: ≥ 95% green
- [ ] Performance: Runtime ↓ 10%
- [ ] Coverage: Overall ≥ 85%, Core ≥ 95%
- [ ] At least 1 external plugin in development

### 90 Days
- [ ] Nightly tests: ≥ 95% green
- [ ] Performance: Runtime ↓ 20%
- [ ] Coverage: All targets met
- [ ] At least 1 external plugin passes CI

## 📝 Monthly Report Template

```markdown
# Monthly Metrics Report - [Month Year]

## Nightly Tests
- Success Rate: X%
- Target: ≥ 95%
- Status: ✅/❌
- Notes: [Any observations]

## Performance
- Runtime Change: ±X%
- Target: ↓ 20%
- Status: ✅/❌
- Baseline: [baseline date]
- Notes: [Any observations]

## Coverage
- Overall: X%
- Core: X%
- Orchestrator: X%
- Agents/Advisors: X%
- Target: Overall ≥ 85%, Core ≥ 95%
- Status: ✅/❌
- Notes: [Any observations]

## Plugins
- External Plugins: X
- Target: ≥ 1 passing CI
- Status: ✅/❌
- Notes: [Any observations]

## Summary
[Overall assessment and next steps]
```

## 🔍 Monitoring Tools

### GitHub Actions
- Monitor workflow runs
- Set up notifications for failures
- Track success rates

### Codecov
- Set up alerts for coverage drops
- Monitor component trends
- Review PR coverage reports

### KPIs
- Weekly KPI aggregation
- Compare to baseline
- Track trends over time

## See Also

- [Success Metrics](SUCCESS_METRICS.md) - Detailed metrics guide
- [Performance Baseline](docs/benchmarks/) - Baseline files
- [Codecov Dashboard](https://codecov.io/gh/<owner>/<repo>)
- [GitHub Actions](https://github.com/<owner>/<repo>/actions)

