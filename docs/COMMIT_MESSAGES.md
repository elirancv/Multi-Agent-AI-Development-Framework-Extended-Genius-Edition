# Conventional Commit Messages

Reference for commit message format (for v1.1+ semantic release).

## Plugin API Infrastructure Commit

For the Plugin API infrastructure added:

```
feat(plugin): dynamic entry-point loader + factory integration

- add plugin_loader with contract validation & cache
- extend factory to merge core + plugins
- add docs/PLUGIN_API.md and pyproject entry points
- add coverage and build-check workflows
- update codecov.yml with component flags

BREAKING CHANGE: None (preview feature, backward compatible)
```

## Release Commit

For v1.0.0 release:

```
chore(release): v1.0.0 stable release

- add doctor command for environment diagnostics
- add dependency audit and performance baseline scripts
- add Plugin API infrastructure (preview)
- add coverage reporting and build validation
- add comprehensive documentation and checklists
- add GitHub protection setup and CI workflows

See docs/RELEASE_SUMMARY.md for complete changelog.
```

## Feature Commits

### Doctor Command
```
feat(cli): add doctor command for environment diagnostics

- check Python version, modules, commands
- verify write permissions and disk space
- validate environment variables
- support JSON output for CI
- exit codes: 0=ok, 1=warnings, 2=errors
```

### Dependency Audit
```
feat(scripts): add dependency audit with license checking

- freeze dependencies from requirements.txt
- check licenses (MIT/Apache2/BSD only)
- generate JSON and Markdown reports
- validate against allowed license list
```

### Coverage
```
feat(ci): add code coverage reporting

- integrate Codecov workflow
- add component flags (agents, advisors, orchestrator, core)
- generate coverage reports and artifacts
- add coverage badge to README
```

### Build Check
```
feat(ci): add package build validation

- validate package builds correctly
- check with twine before release
- upload build artifacts on release
- verify package contents
```

## Documentation Commits

```
docs: add comprehensive release documentation

- add release checklist and verification guides
- add known issues and troubleshooting
- add plugin API documentation
- add pre-release sanity checks
```

## Configuration Commits

```
chore(config): add GitHub protection and CI workflows

- add branch and tag protection setup guide
- add CodeQL security analysis
- add Release Drafter configuration
- add SBOM generation workflow
```

## See Also

- [Semantic Release Guidelines](SEMANTIC_RELEASE.md)
- [Conventional Commits](https://www.conventionalcommits.org/)
