# Ready-to-Use Commit Messages

Copy-paste ready commit messages for v1.0.0 release and post-release.

## 🏷️ Release Commit (v1.0.0)

```
chore(release): v1.0.0 stable release

- add doctor command for environment diagnostics
- add dependency audit and performance baseline scripts
- add Plugin API infrastructure (preview)
- add coverage reporting and build validation
- add comprehensive documentation and checklists
- add GitHub protection setup and CI workflows
- add automated PR labeling and release drafter
- add external test plugin CI validation

See docs/RELEASE_SUMMARY.md for complete changelog.

BREAKING CHANGE: None (stable release, backward compatible)
```

## 📦 Post-Release Bump Commit

```
chore: bump version to 1.0.1-dev

Post-release version bump for development.
```

## 🔧 Feature Commits (if committing separately)

### Doctor Command
```
feat(cli): add doctor command for environment diagnostics

- check Python version, modules, commands
- verify write permissions and disk space
- validate environment variables
- support JSON output for CI
- exit codes: 0=ok, 1=warnings, 2=errors

Closes #XXX
```

### Plugin API Infrastructure
```
feat(plugin): dynamic entry-point loader + factory integration

- add plugin_loader with contract validation & cache
- extend factory to merge core + plugins
- add docs/PLUGIN_API.md and pyproject entry points
- add external test plugin CI workflow

BREAKING CHANGE: None (preview feature, backward compatible)
```

### Coverage & Build
```
feat(ci): add code coverage and build validation

- integrate Codecov workflow with component flags
- add package build validation workflow
- add coverage thresholds (core 95%, orchestrator 90%)
- add build-check workflow for release validation
```

### Documentation
```
docs: add comprehensive release documentation

- add release checklist and verification guides
- add known issues and troubleshooting
- add plugin API documentation and templates
- add pre-release sanity checks and final verification
- add success metrics and v1.1 roadmap
```

### Configuration
```
chore(config): add GitHub protection and automation

- add branch and tag protection setup guide
- add CodeQL security analysis workflow
- add Release Drafter configuration
- add SBOM generation workflow
- add automated PR labeling
```

## 🎯 v1.1 Feature Commits (Future)

### multiagent new GA
```
feat(cli): promote multiagent new to GA

- add multiagent CLI entry point
- add templates: static-site, api-service, etl-pipeline
- add flags: --preset, --with-ci, --with-docs, --with-examples
- update documentation

Closes #XXX
```

### Pipelines Gallery
```
feat(gallery): add pipelines gallery with 5 reference examples

- add static-site generator pipeline
- add REST API service pipeline
- add ETL pipeline
- add CLI tool pipeline
- add microservice pipeline
- include DOT/PNG graphs and execution reports

Closes #XXX
```

### Plugin API Tests
```
feat(plugin): add external test plugin for CI validation

- create test-plugin-multiagent repository
- integrate into main framework CI
- add integration tests
- document plugin development workflow

Closes #XXX
```

### PyPI Publishing
```
feat(release): publish to PyPI

- finalize entry points and CLI
- add long_description from README
- add classifiers (Python versions, topics)
- publish to PyPI
- update installation documentation

Closes #XXX
```

## 📝 Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `chore`: Maintenance
- `refactor`: Code refactoring
- `perf`: Performance
- `test`: Tests

**Scopes** (optional):
- `cli`, `plugin`, `ci`, `docs`, `config`, `release`

## See Also

- [Semantic Release Guidelines](SEMANTIC_RELEASE.md)
- [Conventional Commits](https://www.conventionalcommits.org/)

