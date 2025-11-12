# Post-Release Checklist (v0.9.0)

Complete these tasks after releasing v0.9.0 to prepare for the next development cycle.

## ✅ Immediate (Same Day)

### 1. Version Bump for Next Dev Cycle

Update `src/__init__.py`:

```python
__version__ = "0.9.1-dev"
```

### 2. Create GitHub Release

1. Go to [Releases](https://github.com/your-org/AgentsSystemV2/releases)
2. Click "Draft a new release"
3. **Tag**: `v0.9.0`
4. **Title**: `v0.9.0 – Production-ready Orchestrator`
5. **Description**: Copy from `RELEASE_NOTES_v0.9.0.md`
6. **Attach artifacts** (optional):
   - `out/pipeline.png` (if exists)
   - `out/smoke/SMOKE_SUMMARY.md`
   - `out/smoke/smoke_junit.xml`
7. Check "Set as the latest release"
8. Publish release

### 3. Tag and Push

```bash
git tag v0.9.0
git push origin v0.9.0
```

## 📋 Tracking Issues (Open 5 Issues)

### Issue 1: v1.0 "Features Freeze & Hard Tests" Meta-Issue

**Title**: `[META] v1.0 Features Freeze & Hard Tests`

**Body**:
```markdown
## Goal
Prepare for v1.0 stable release with feature freeze and comprehensive testing.

## Tasks
- [ ] Feature freeze (no new features, only bug fixes)
- [ ] Comprehensive test coverage (>90%)
- [ ] Performance benchmarks
- [ ] Security audit
- [ ] Documentation review
- [ ] Migration guide from v0.9.x

## Timeline
Target: Q2 2025
```

### Issue 2: API Documentation Generator

**Title**: `[FEATURE] API Documentation Generator`

**Body**:
```markdown
## Description
Generate API documentation from docstrings using pdoc or pydoc-markdown.

## Tasks
- [ ] Set up pdoc/pydoc-markdown
- [ ] Configure output to `docs/api/`
- [ ] Add to CI/CD pipeline
- [ ] Link from `docs/INDEX.md`

## Acceptance Criteria
- API docs generated automatically on release
- All public APIs documented
- Searchable and browsable
```

### Issue 3: Pipelines Gallery

**Title**: `[FEATURE] Pipelines Gallery with Examples`

**Body**:
```markdown
## Description
Create a gallery of example pipelines with screenshots and use cases.

## Tasks
- [ ] Collect example pipelines
- [ ] Add screenshots/visualizations
- [ ] Document use cases
- [ ] Create `docs/pipelines/` directory
- [ ] Link from main README

## Examples Needed
- MVP fast delivery
- Production stability
- Research/experimental
- Custom workflows
```

### Issue 4: Council Presets per Category

**Title**: `[FEATURE] Council Presets per Category`

**Body**:
```markdown
## Description
Create YAML shortcuts for common council configurations per category.

## Tasks
- [ ] Define preset categories (MVP, Production, Research)
- [ ] Create preset YAML files
- [ ] Document usage
- [ ] Add CLI flag `--preset <name>`

## Presets
- `mvp-fast`: Light advisors, lower thresholds
- `production`: Full advisors, strict thresholds
- `research`: Experimental, relaxed scoring
```

### Issue 5: Artifact Retention Policy

**Title**: `[FEATURE] Artifact Retention Policy`

**Body**:
```markdown
## Description
Implement automatic cleanup and size limits for artifacts.

## Tasks
- [ ] Define retention policy (time-based, size-based)
- [ ] Implement cleanup logic
- [ ] Add configuration options
- [ ] Add CLI command `cleanup-artifacts`
- [ ] Document in `docs/CONFIG.md`

## Policy Options
- Max age (days)
- Max size per run
- Max total size
- Keep latest N runs
```

## 🔧 GitHub Configuration

### 1. Enable Dependabot

Create `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
```

### 2. Branch Protection

Enable branch protection for `main`:
- Require pull request reviews
- Require status checks:
  - `tests` (pytest)
  - `smoke` (smoke_test.py)
- Require branches to be up to date
- Do not allow force pushes

### 3. Required CI Checks

In repository settings → Branches → Branch protection rules:
- Add required check: `smoke-fast`
- Add required check: `tests`

## 📝 Security & QA

### 1. Verify SECURITY.md

- [ ] Contact email is correct
- [ ] Response timeline is realistic
- [ ] Disclosure policy is clear

### 2. Verify LICENSE

- [ ] Copyright year is correct
- [ ] Organization/name is correct

### 3. Security Audit

- [ ] Review dependencies for known vulnerabilities
- [ ] Run `pip audit` or `safety check`
- [ ] Update vulnerable packages if needed

## 🎨 Nice-to-Have (Fast Wins)

### 1. Issue Templates ✅

Already created:
- `.github/ISSUE_TEMPLATE/bug.md`
- `.github/ISSUE_TEMPLATE/feature.md`

### 2. PR Template ✅

Already created:
- `.github/pull_request_template.md`

### 3. Badges ✅

Already added to README.md

### 4. Docs/INDEX.md Quick Links ✅

Already updated

## 📊 Monitoring

### 1. Set Up Release Analytics

- Monitor download counts
- Track issue reports
- Monitor CI/CD success rates

### 2. Community Engagement

- Respond to issues within 48 hours
- Review PRs promptly
- Update documentation based on feedback

## ✅ Completion Checklist

- [ ] Version bumped to `0.9.1-dev`
- [ ] GitHub release created
- [ ] Tag pushed
- [ ] 5 tracking issues opened
- [ ] Dependabot enabled
- [ ] Branch protection configured
- [ ] SECURITY.md verified
- [ ] LICENSE verified
- [ ] Security audit completed
- [ ] Issue templates created
- [ ] PR template created
- [ ] Badges added
- [ ] Docs/INDEX.md updated

---

**Next Steps**: Start working on v1.0 roadmap issues!

