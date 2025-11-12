# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-XX

### Added
- SQLite CheckpointStore with atomic operations and fast queries
- FS → SQLite migration utility (`scripts/migrate_checkpoints.py`)
- Artifact retention and cleanup (`python cli.py clean`)
- Council presets (mvp-fast, production, research)
- Hard tests pipeline with KPI tracking
- KPI aggregation and Markdown summary generation
- Smoke tests for artifact cleanup
- API documentation generation (pdoc)
- Nightly hard tests workflow
- Weekly retention cleanup workflow
- CLI `--checkpoint-store` flag
- CLI `--preset` flag
- Duration parsing for retention (`7d`, `24h`, `3600s`)
- JSON output for cleanup reports
- Pipeline generator (`multiagent new`)

### Changed
- Version bumped to 1.0.0 (stable release)
- Checkpoint store factory pattern in CLI
- Preset loader Policy mapping fixed

### Fixed
- Checkpoint timestamp handling in SQLite store
- Artifact cleanup freed_bytes calculation in dry-run
- Preset loader Policy constructor arguments

## [0.9.0] - 2025-01-12

### Added
- OpenTelemetry integration for distributed tracing
- Deterministic seeding per run/stage for reproducibility
- Artifact "Smart Diff" for text comparison
- Budget Guard (Policy): time/stages/artifact weight enforcement
- Advisor Calibration Weights (for Council)
- CLI flags: `--otel-endpoint`, `--otel-service`, `--no-cache`, `--export-graph`, `--resume-run-id`
- Top 5 suggestions report option
- Comprehensive smoke test suite with JUnit XML and Markdown reports
- Smart color detection (auto-disable in CI/non-TTY)
- JSON output for machine consumption (`--json` flag)
- Strict performance mode (`--strict-performance` flag)
- Test listing (`--list-tests` flag)
- Version command (`--version` flag)
- Structured JSON logging (when `CI=true` or `ORCH_JSON_LOG=true`)
- Environment variable configuration support
- `find_key()` method in FileCheckpointStore for specific checkpoint lookup
- Enhanced JUnit XML with system-out/system-err for better CI debugging

### Changed
- Improved checkpoint store to use step_index instead of mtime for reliability
- Enhanced graphviz detection with detailed installation instructions
- Better error messages and user feedback throughout

### Fixed
- Fixed Unicode encoding issues on Windows
- Fixed AdvisorCouncil missing `gate()` method
- Fixed test_pipeline_graph.py assertion on dot.body (list vs string)
- Fixed checkpoint find_last_key to use step_index instead of mtime
- Suppressed OpenTelemetry connection errors when no collector is available

### Security
- Added SECURITY.md for vulnerability reporting
- Added CONTRIBUTING.md with development guidelines

[0.9.0]: https://github.com/your-org/AgentsSystemV2/releases/tag/v0.9.0
