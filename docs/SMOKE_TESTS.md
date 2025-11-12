# Smoke Test Suite

Comprehensive smoke tests for the multi-agent pipeline system.

## Quick Start

```bash
# Run all tests (fast mode - skips slow execution tests)
python scripts/smoke_test.py --skip-slow

# Run all tests including execution tests
python scripts/smoke_test.py

# Run specific test
python scripts/smoke_test.py --test dry-run

# Verbose output
python scripts/smoke_test.py --verbose
```

## Available Tests

1. **Dry-run validation** - Validates pipeline YAML structure
2. **Graph export** - Exports pipeline graph to DOT format
3. **Sequential execution** - Runs pipeline sequentially (slow)
4. **Cache control** - Tests `--no-cache` flag (slow)
5. **Budget enforcement** - Verifies budget guard works (slow)
6. **Top suggestions** - Tests report with top suggestions (slow)
7. **All pipelines validation** - Validates all YAML files in `pipeline/`

## Manual Smoke Tests

### Bash

```bash
# 1) Dry-run + Graph export
python cli.py --pipeline pipeline/production.yaml --dry-run --export-graph out/pipeline.dot
dot -Tpng out/pipeline.dot -o out/pipeline.png

# 2) Validate all pipelines
for f in pipeline/*.yaml; do python cli.py --pipeline "$f" --dry-run; done

# 3) Sequential execution with artifacts
python cli.py --pipeline pipeline/production.yaml --output human --save-artifacts

# 4) Parallel execution
python cli.py --pipeline pipeline/with_codegen.yaml --parallel --max-workers 4 --output human

# 5) No cache (debug)
python cli.py --pipeline pipeline/production.yaml --no-cache --output json

# 6) Budget test (may fail if budget exceeded)
python cli.py --pipeline pipeline/production.yaml --output json 2>/dev/null || echo "[EXPECTED] budget guard blocked run"

# 7) Resume from checkpoint
python cli.py --pipeline pipeline/production.yaml --resume-run-id <RUN_ID> --output human

# 8) OpenTelemetry
python cli.py --pipeline pipeline/production.yaml --otel-endpoint http://localhost:4318/v1/traces --otel-service multi-agent-dev
```

### PowerShell

```powershell
# 1) Dry-run + Graph export
python cli.py --pipeline pipeline/production.yaml --dry-run --export-graph out/pipeline.dot
dot -Tpng out/pipeline.dot -o out/pipeline.png

# 2) Validate all pipelines
Get-ChildItem pipeline/*.yaml | ForEach-Object { python cli.py --pipeline $_.FullName --dry-run }

# 3) Sequential execution
python cli.py --pipeline pipeline/production.yaml --output human --save-artifacts

# 4) Parallel execution
python cli.py --pipeline pipeline/with_codegen.yaml --parallel --max-workers 4 --output human

# 5) No cache
python cli.py --pipeline pipeline/production.yaml --no-cache --output json

# 6) Budget test
python cli.py --pipeline pipeline/production.yaml --output json 2>$null; if ($LASTEXITCODE -ne 0) { Write-Host "[EXPECTED] budget guard blocked run" }

# 7) Resume
python cli.py --pipeline pipeline/production.yaml --resume-run-id <RUN_ID> --output human

# 8) OpenTelemetry
python cli.py --pipeline pipeline/production.yaml --otel-endpoint http://localhost:4318/v1/traces --otel-service multi-agent-dev
```

## Expected Outputs

### Dry-run Output

```json
{
  "pipeline": "pipeline/production.yaml",
  "stages": 5,
  "order": ["requirements", "prompt_refine", "code_skeleton", "static_lint", "accessibility_audit"],
  "status": "valid"
}
```

### Report Output (--output human)

- Stage-by-stage breakdown with:
  - Category
  - Duration (ms)
  - Error reason (if any)
  - Artifact links (if `--save-artifacts`)
  - Diff (if previous content exists)

### Event Log (`out/<run_id>_events.jsonl`)

Look for:
- `step_start` - Stage execution started
- `step_result` - Stage completed
- `step_rejected` - Stage rejected by advisor
- `error` - Error occurred
- `cache_hit` - Cache was used

## Tips

### Testing Weighted Council

Ensure your YAML has:

```yaml
policy:
  advisors:
    requirements:
      decision: average
      list: ["RequirementsAdvisor", "PromptRefinerAdvisor"]
      weights:
        RequirementsAdvisor: 1.0
        PromptRefinerAdvisor: 0.7
```

### Testing Budget Guard

Set a tight budget in policy:

```yaml
policy:
  budget:
    max_artifacts_bytes: 1000  # Very small to trigger guard
```

### Debugging Cache

Compare runs with/without `--no-cache` and check `cache_hit` events in `*_events.jsonl`.

## Exit Codes

- `0` - All tests passed
- `1` - One or more tests failed

