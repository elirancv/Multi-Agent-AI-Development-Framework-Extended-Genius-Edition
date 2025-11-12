# Success Metrics - 30-90 Day Tracking

Key metrics to track after v1.0.0 release.

## 🎯 Target Metrics (30-90 days)

### Nightly Tests
- **Target**: Green rate ≥ 95%
- **Measurement**: `.github/workflows/hard-tests-nightly.yml` success rate
- **Tracking**: GitHub Actions workflow runs

### Performance
- **Target**: Runtime ↓ 20% in `hard_test.yaml` pipeline
- **Measurement**: Compare KPI baseline (`docs/benchmarks/baseline_latest.json`) vs current
- **Tracking**: Weekly KPI reports from nightly tests

### Code Coverage
- **Overall**: ≥ 85%
- **Core**: ≥ 95%
- **Orchestrator**: ≥ 90%
- **Agents/Advisors**: ≥ 80%
- **Measurement**: Codecov reports (component flags)
- **Tracking**: Weekly Codecov reports

### Plugin Ecosystem
- **Target**: At least 1 external "Hello-World" plugin passes CI
- **Measurement**: `.github/workflows/plugin-api-test.yml` with external plugin
- **Tracking**: GitHub Actions workflow runs

## 📊 Tracking Methods

### Automated Tracking

1. **GitHub Actions Metrics**
   - Nightly test success rate
   - Plugin API test runs
   - Coverage trends

2. **Codecov Dashboard**
   - Component coverage trends
   - Coverage by flag (agents, advisors, orchestrator, core)

3. **KPI Reports**
   - Weekly KPI aggregation
   - Performance trends
   - Baseline comparisons

### Manual Tracking

1. **Weekly Review**
   - Check GitHub Actions status
   - Review Codecov trends
   - Analyze KPI reports

2. **Monthly Report**
   - Aggregate metrics
   - Compare to targets
   - Identify regressions

## 📈 Baseline (v1.0.0)

### Current Baseline
- **Nightly Tests**: Baseline from first run
- **Performance**: Baseline from `docs/benchmarks/baseline_latest.json`
- **Coverage**: Initial coverage report
- **Plugins**: 0 external plugins

### Update Baseline
```bash
# Generate new baseline
python scripts/perf_baseline.py

# Compare baselines
diff docs/benchmarks/baseline_*.json
```

## 🎯 Success Criteria

### 30 Days
- [ ] Nightly tests: ≥ 90% green
- [ ] Coverage: Overall ≥ 80%, Core ≥ 90%
- [ ] No critical regressions

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

## 📝 Reporting

### Weekly Status
- Check GitHub Actions
- Review Codecov trends
- Analyze KPI reports

### Monthly Report Template
```markdown
# Monthly Metrics Report - [Month Year]

## Nightly Tests
- Success Rate: X%
- Target: ≥ 95%
- Status: ✅/❌

## Performance
- Runtime Change: ±X%
- Target: ↓ 20%
- Status: ✅/❌

## Coverage
- Overall: X%
- Core: X%
- Target: Overall ≥ 85%, Core ≥ 95%
- Status: ✅/❌

## Plugins
- External Plugins: X
- Target: ≥ 1 passing CI
- Status: ✅/❌

## Notes
- [Any observations or issues]
```

## 🔍 Monitoring

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

- [Performance Baseline](docs/benchmarks/)
- [Codecov Dashboard](https://codecov.io/gh/<owner>/<repo>)
- [GitHub Actions](https://github.com/<owner>/<repo>/actions)
