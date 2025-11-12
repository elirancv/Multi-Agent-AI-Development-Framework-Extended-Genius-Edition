# Definition of Done - v1.0.0

Final checklist to verify v1.0.0 release is complete.

## ✅ Pre-Release

- [x] All tests passing (87/87)
- [x] Smoke tests passing
- [x] Documentation complete
- [x] Release notes prepared
- [x] Announcements prepared
- [x] Scripts created and tested

## ✅ Release

- [ ] **Tag v1.0.0 published**
  - [ ] Tag created: `git tag v1.0.0`
  - [ ] Tag signed (if GPG available): `git tag -s v1.0.0`
  - [ ] Tag pushed: `git push origin v1.0.0`

- [ ] **GitHub Release published**
  - [ ] Release created on GitHub
  - [ ] Release body from `GITHUB_RELEASE_BODY_v1.0.0.md` or short version
  - [ ] Assets attached (if any):
    - [ ] `sbom/sbom.json` (auto-generated)
    - [ ] `sbom/sbom.xml` (auto-generated)
    - [ ] Optional: `out/pipeline.dot`, `out/smoke/SMOKE_SUMMARY.md`

## ✅ Post-Release Verification

- [ ] **Nightly Hard Tests**
  - [ ] Manually triggered via `workflow_dispatch`
  - [ ] KPIs generated and saved
  - [ ] Results reviewed

- [ ] **Weekly Retention Job**
  - [ ] Job scheduled in GitHub Actions
  - [ ] First dry-run completed
  - [ ] Retention policies verified

- [ ] **Quickstart Verified**
  - [ ] Bash commands work
  - [ ] PowerShell commands work
  - [ ] Output is correct

- [ ] **README Updated**
  - [ ] Quickstart section (Bash + PowerShell)
  - [ ] Support section added
  - [ ] Badges point to correct URLs

- [ ] **CodeQL Security Scan**
  - [ ] Workflow runs successfully
  - [ ] No critical security issues
  - [ ] Results reviewed

- [ ] **SBOM Generated**
  - [ ] SBOM created in release artifacts
  - [ ] JSON and XML formats available
  - [ ] Dependencies listed correctly

## ✅ Documentation

- [ ] **All docs in place**
  - [ ] `docs/QUICKSTART.md` exists and accurate
  - [ ] `docs/INDEX.md` exists with working links
  - [ ] `docs/KNOWN_ISSUES.md` created
  - [ ] `docs/RELEASE_VERIFICATION.md` created
  - [ ] `docs/DEFINITION_OF_DONE_v1.0.md` (this file)

- [ ] **API Documentation**
  - [ ] API docs generated (if using pdoc)
  - [ ] Published to `docs/api/` or GitHub Pages

## ✅ Configuration

- [ ] **GitHub Protection**
  - [ ] Branch protection on `main` configured
  - [ ] Tag protection on `v*` configured
  - [ ] CODEOWNERS file updated with correct usernames

- [ ] **CI/CD**
  - [ ] All workflows passing
  - [ ] Release Drafter configured
  - [ ] CodeQL configured
  - [ ] SBOM generation configured

## ✅ v1.1 Roadmap

- [ ] **Milestone Created**
  - [ ] GitHub Milestone "v1.1.0" created
  - [ ] Target date set

- [ ] **Issues Created** (5 issues minimum)
  - [ ] Issue: "Promote multiagent new from preview to GA"
  - [ ] Issue: "Add industry-specific presets (security/compliance/a11y)"
  - [ ] Issue: "Create template pack (Static site, API service, Data/ETL)"
  - [ ] Issue: "PyPI packaging with entry point (multiagent)"
  - [ ] Issue: "Plugin API for external Agents/Advisors"
  - [ ] Issue: "Pipelines Gallery with 5 examples"
  - [ ] Issue: "Artifact Retention Policy v2"

## ✅ Final Checks

- [ ] **Version Verification**
  ```bash
  python cli.py --version
  # Should output: 1.0.0
  ```

- [ ] **Doctor Command**
  ```bash
  python scripts/doctor.py
  # Should pass all checks
  ```

- [ ] **Dependency Audit**
  ```bash
  python scripts/deps_audit.py
  # Should show all dependencies with allowed licenses
  ```

- [ ] **Performance Baseline**
  ```bash
  python scripts/perf_baseline.py
  # Should create baseline in docs/benchmarks/
  ```

## ✅ Announcements

- [ ] **GitHub Release** - Published
- [ ] **LinkedIn** - Posted (if applicable)
- [ ] **Telegram** - Posted (if applicable)
- [ ] **Twitter/X** - Posted (if applicable)

## Status

**Current Status**: 🟡 In Progress

**Target Completion**: Before v1.0.0 release

**Last Updated**: 2025-01-XX

---

## Sign-Off

When all items are checked:

- [ ] **Technical Lead**: _________________ Date: _______
- [ ] **Release Manager**: _________________ Date: _______

**Release Approved**: ☐ Yes  ☐ No

---

**Note**: This checklist should be completed before marking v1.0.0 as "released" in GitHub.
