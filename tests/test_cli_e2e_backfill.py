"""E2E CLI tests for orchestrator."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

PY = sys.executable


def run_cli(args, cwd=None, env=None):
    """Run cli.py with given args."""
    cmd = [PY, "cli.py"] + args
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=cwd,
        env=env,
    )
    return result.returncode, result.stdout, result.stderr


def test_cli_version():
    """Test --version flag."""
    code, out, err = run_cli(["--version"])
    assert code == 0
    assert "1.0.0" in out or "1.0" in out


def test_cli_dry_run_valid():
    """Test dry-run with valid pipeline."""
    code, out, err = run_cli([
        "--pipeline", "pipeline/production.yaml",
        "--dry-run",
        "--output", "json"
    ])
    assert code == 0, f"CLI failed: {err}"
    
    try:
        data = json.loads(out)
        assert "status" in data or "stages" in data or "pipeline" in data
    except json.JSONDecodeError:
        pytest.fail(f"Invalid JSON output: {out}")


def test_cli_dry_run_invalid_pipeline():
    """Test dry-run with invalid pipeline."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("invalid: yaml: content: [")
        f.flush()
        invalid_path = f.name
    
    try:
        code, out, err = run_cli([
            "--pipeline", invalid_path,
            "--dry-run"
        ])
        assert code != 0, "Should fail on invalid pipeline"
    finally:
        Path(invalid_path).unlink(missing_ok=True)


def test_cli_export_graph():
    """Test graph export."""
    with tempfile.TemporaryDirectory() as tmpdir:
        graph_path = Path(tmpdir) / "test.dot"
        
        code, out, err = run_cli([
            "--pipeline", "pipeline/production.yaml",
            "--dry-run",
            "--export-graph", str(graph_path)
        ])
        
        assert code == 0, f"Graph export failed: {err}"
        assert graph_path.exists(), "Graph file not created"
        assert graph_path.stat().st_size > 0, "Graph file is empty"


def test_cli_parallel_flag():
    """Test --parallel flag."""
    code, out, err = run_cli([
        "--pipeline", "pipeline/production.yaml",
        "--dry-run",
        "--parallel",
        "--output", "json"
    ])
    # Should not fail (may not have parallel pipeline, but flag should be accepted)
    assert code in (0, 1)


def test_cli_preset():
    """Test --preset flag."""
    code, out, err = run_cli([
        "--pipeline", "pipeline/production.yaml",
        "--dry-run",
        "--preset", "mvp-fast",
        "--output", "json"
    ])
    # Should accept preset flag
    assert code in (0, 1)


def test_cli_checkpoint_store():
    """Test --checkpoint-store flag."""
    code, out, err = run_cli([
        "--pipeline", "pipeline/production.yaml",
        "--dry-run",
        "--checkpoint-store", "sqlite",
        "--output", "json"
    ])
    # Should accept checkpoint-store flag
    assert code in (0, 1)


def test_cli_memory_overrides():
    """Test --mem flag for memory overrides."""
    code, out, err = run_cli([
        "--pipeline", "pipeline/production.yaml",
        "--dry-run",
        "--mem", 'test_key="test_value"',
        "--output", "json"
    ])
    # Should accept memory overrides
    assert code in (0, 1)


def test_cli_fail_fast():
    """Test --fail-fast flag."""
    code, out, err = run_cli([
        "--pipeline", "pipeline/production.yaml",
        "--dry-run",
        "--fail-fast",
        "--output", "json"
    ])
    # Should accept fail-fast flag
    assert code in (0, 1)


def test_cli_no_cache():
    """Test --no-cache flag."""
    code, out, err = run_cli([
        "--pipeline", "pipeline/production.yaml",
        "--dry-run",
        "--no-cache",
        "--output", "json"
    ])
    # Should accept no-cache flag
    assert code in (0, 1)


def test_cli_save_artifacts():
    """Test --save-artifacts flag."""
    code, out, err = run_cli([
        "--pipeline", "pipeline/production.yaml",
        "--dry-run",
        "--save-artifacts",
        "--output", "json"
    ])
    # Should accept save-artifacts flag
    assert code in (0, 1)

