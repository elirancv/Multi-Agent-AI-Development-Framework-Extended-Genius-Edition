# Semantic Release Guidelines

This document outlines commit message conventions for automated versioning and changelog generation (planned for v1.1+).

## Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

## Types

- **feat**: A new feature (triggers minor version bump)
- **fix**: A bug fix (triggers patch version bump)
- **docs**: Documentation only changes
- **style**: Code style changes (formatting, missing semicolons, etc.)
- **refactor**: Code refactoring without changing functionality
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, dependency updates, build config changes
- **ci**: CI/CD changes
- **build**: Build system or external dependencies changes

## Scopes (Optional)

- `agents`: Changes to agent implementations
- `advisors`: Changes to advisor implementations
- `orchestrator`: Changes to orchestrator logic
- `cli`: CLI command changes
- `pipeline`: Pipeline configuration changes
- `docs`: Documentation changes
- `tests`: Test changes
- `ci`: CI/CD changes

## Examples

### Feature (Minor Version Bump)

```
feat(agents): add new ProductManagerAgent

Implements product definition agent with Steve Jobs advisor integration.
Closes #123
```

### Bug Fix (Patch Version Bump)

```
fix(orchestrator): resolve race condition in parallel execution

Fixes issue where parallel agents could overwrite shared memory.
Fixes #456
```

### Breaking Change (Major Version Bump)

```
feat(cli)!: change --output flag to --format

BREAKING CHANGE: The --output flag has been renamed to --format for clarity.
Migration: Use --format instead of --output.

Closes #789
```

### Documentation

```
docs: update quickstart guide with PowerShell examples

Added Windows PowerShell examples to match Linux/macOS examples.
```

### Chore (No Version Bump)

```
chore: update dependencies to latest versions

- Updated PyYAML to 7.0
- Updated pydantic to 2.5.0
```

## Version Bumping Rules

- **MAJOR** (1.0.0 → 2.0.0): Breaking changes (indicated by `!` after type)
- **MINOR** (1.0.0 → 1.1.0): New features (feat)
- **PATCH** (1.0.0 → 1.0.1): Bug fixes (fix)

## Implementation Plan (v1.1+)

1. **Setup**: Configure semantic-release or similar tool
2. **CI Integration**: Add to GitHub Actions workflow
3. **Changelog**: Auto-generate from commit messages
4. **Versioning**: Auto-bump version based on commits
5. **Release**: Auto-create GitHub releases

## Tools

- [semantic-release](https://github.com/semantic-release/semantic-release) - Full-featured release automation
- [python-semantic-release](https://python-semantic-release.readthedocs.io/) - Python-specific semantic release
- [commitizen](https://commitizen-tools.github.io/commitizen/) - Commit message validation

## Current Status

**Status**: Draft / Planned for v1.1+

**Current Practice**: Manual versioning and release notes

**Migration**: Will adopt semantic release conventions starting v1.1.0

## References

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)

