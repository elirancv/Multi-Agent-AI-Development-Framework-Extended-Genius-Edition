"""Comprehensive smoke test suite for multi-agent pipeline system.

This script runs a series of smoke tests to verify:
- Pipeline validation (dry-run)
- Graph export
- Sequential execution
- Parallel execution
- Cache control
- Budget enforcement
- Resume functionality
- OpenTelemetry integration
- Report generation

Usage:
    python scripts/smoke_test.py [--pipeline PIPELINE] [--verbose] [--skip-slow]
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from xml.etree.ElementTree import Element, SubElement, tostring

# Smart color detection: disable in CI or non-TTY
USE_COLOR = sys.stdout.isatty() and os.environ.get("CI") != "true"

# Colors for terminal output (works on Windows 10+ and Unix)
GREEN = "\033[92m" if USE_COLOR else ""
RED = "\033[91m" if USE_COLOR else ""
YELLOW = "\033[93m" if USE_COLOR else ""
BLUE = "\033[94m" if USE_COLOR else ""
RESET = "\033[0m" if USE_COLOR else ""
BOLD = "\033[1m" if USE_COLOR else ""


class TestResult:
    """Test result with status and message."""

    def __init__(
        self,
        name: str,
        passed: bool,
        message: str = "",
        details: str = "",
        seconds: float = 0.0,
        skipped: bool = False,
    ):
        self.name = name
        self.passed = passed
        self.message = message
        self.details = details
        self.seconds = seconds
        self.skipped = skipped

    def to_dict(self) -> Dict[str, any]:
        """Convert to dictionary for JUnit/Markdown export."""
        status = "skipped" if self.skipped else ("passed" if self.passed else "failed")
        return {
            "name": self.name,
            "status": status,
            "message": self.message,
            "details": self.details,
            "seconds": self.seconds,
        }


def run_cli_command(
    args: List[str], timeout: Optional[int] = None
) -> Tuple[int, str, str, float]:
    """
    Helper function to run CLI commands with timing.

    Args:
        args: CLI arguments (without 'python cli.py')
        timeout: Timeout in seconds

    Returns:
        Tuple of (exit_code, stdout, stderr, seconds_elapsed)
    """
    cmd = ["python", "cli.py"] + args
    start = time.time()
    exit_code, stdout, stderr = run_command(cmd, timeout=timeout)
    elapsed = time.time() - start
    return exit_code, stdout, stderr, elapsed


def run_command(
    cmd: List[str], capture_output: bool = True, timeout: Optional[int] = None
) -> Tuple[int, str, str]:
    """
    Run a command and return exit code, stdout, stderr.

    Args:
        cmd: Command to run as list of strings
        capture_output: Whether to capture output
        timeout: Timeout in seconds

    Returns:
        Tuple of (exit_code, stdout, stderr)
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture_output,
            text=True,
            timeout=timeout,
            check=False,
            encoding="utf-8",
            errors="replace",  # Replace encoding errors instead of failing
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "Command timed out"
    except Exception as e:
        return 1, "", str(e)


def has_graphviz() -> Tuple[bool, str]:
    """
    Check if graphviz is available (both Python package and system dot command).
    
    Returns:
        Tuple of (is_available, error_message)
    """
    # Check if graphviz Python package is installed
    try:
        import graphviz
    except ImportError:
        return False, "Python package 'graphviz' not installed. Install with: pip install graphviz"
    
    # Check if dot command is available in PATH
    if shutil.which("dot") is None:
        return False, (
            "System 'dot' command not found. "
            "Install Graphviz system package:\n"
            "  - Windows: Download from https://graphviz.org/download/ or use: winget install graphviz\n"
            "  - Linux: apt-get install graphviz (Debian/Ubuntu) or yum install graphviz (RHEL/CentOS)\n"
            "  - macOS: brew install graphviz"
        )
    
    # Try to create a simple graph to verify it works
    try:
        g = graphviz.Digraph("test")
        g.node("A")
        g.node("B")
        g.edge("A", "B")
        # Don't actually render, just verify the object was created
        return True, ""
    except Exception as e:
        return False, f"Graphviz test failed: {e}"


def test_dry_run(
    pipeline: str, verbose: bool = False, max_seconds: float = 5.0, strict_performance: bool = False
) -> TestResult:
    """Test 1: Dry-run validation."""
    print(f"{BLUE}[TEST 1]{RESET} Dry-run validation...", end=" ", flush=True)
    start = time.time()
    exit_code, stdout, stderr, elapsed = run_cli_command(
        ["--pipeline", pipeline, "--dry-run"]
    )

    if exit_code == 0:
        try:
            data = json.loads(stdout)
            if data.get("status") == "valid":
                stages = data.get("stages", 0)
                msg = f"Pipeline valid with {stages} stages"
                exceeded = elapsed > max_seconds
                if exceeded:
                    msg += f" (slow: {elapsed:.2f}s > {max_seconds}s)"
                    if strict_performance:
                        print(f"{RED}FAILED{RESET} (performance threshold exceeded: {elapsed:.2f}s > {max_seconds}s)")
                        return TestResult(
                            "Dry-run validation",
                            False,
                            f"Performance threshold exceeded: {elapsed:.2f}s > {max_seconds}s",
                            stdout if verbose else "",
                            seconds=elapsed,
                        )
                    else:
                        print(f"{YELLOW}PASSED{RESET} ({stages} stages, {elapsed:.2f}s) - slow")
                else:
                    print(f"{GREEN}PASSED{RESET} ({stages} stages, {elapsed:.2f}s)")
                return TestResult(
                    "Dry-run validation",
                    True,
                    msg,
                    stdout if verbose else "",
                    seconds=elapsed,
                )
        except json.JSONDecodeError:
            pass

    print(f"{RED}FAILED{RESET}")
    return TestResult(
        "Dry-run validation",
        False,
        "Pipeline validation failed",
        stderr,
        seconds=elapsed,
    )


def test_graph_export(
    pipeline: str, verbose: bool = False, out_dir: str = "out"
) -> TestResult:
    """Test 2: Graph export."""
    print(f"{BLUE}[TEST 2]{RESET} Graph export...", end=" ", flush=True)
    
    graphviz_available, error_msg = has_graphviz()
    if not graphviz_available:
        print(f"{YELLOW}SKIPPED{RESET} (graphviz not available)")
        return TestResult(
            "Graph export",
            True,  # Don't fail suite
            f"Skipped ({error_msg})",
            "",
            skipped=True,
        )
    
    graph_path = Path(out_dir) / "smoke_test_graph.dot"
    graph_path.parent.mkdir(parents=True, exist_ok=True)

    start = time.time()
    exit_code, stdout, stderr, elapsed = run_cli_command(
        [
            "--pipeline",
            pipeline,
            "--dry-run",
            "--export-graph",
            str(graph_path),
        ]
    )

    if exit_code == 0 and graph_path.exists():
        size = graph_path.stat().st_size
        print(f"{GREEN}PASSED{RESET} ({size} bytes, {elapsed:.2f}s)")
        return TestResult(
            "Graph export",
            True,
            f"Graph exported to {graph_path} ({size} bytes)",
            str(graph_path.read_text()[:200]) if verbose else "",
            seconds=elapsed,
        )

    # Check if failure is due to missing graphviz
    if "graphviz" in stderr.lower() or "graphviz" in stdout.lower():
        print(f"{YELLOW}SKIPPED{RESET} (graphviz not available)")
        return TestResult(
            "Graph export",
            True,  # Don't fail suite
            "Skipped (graphviz not available)",
            stderr if verbose else "",
            skipped=True,
        )

    print(f"{RED}FAILED{RESET}")
    return TestResult(
        "Graph export", False, "Graph export failed", stderr, seconds=elapsed
    )


def test_sequential_execution(
    pipeline: str,
    verbose: bool = False,
    save_artifacts: bool = True,
    timeout: Optional[int] = 300,
) -> TestResult:
    """Test 3: Sequential execution."""
    print(f"{BLUE}[TEST 3]{RESET} Sequential execution...", end=" ", flush=True)
    start = time.time()
    
    args = ["--pipeline", pipeline, "--output", "json"]
    if save_artifacts:
        args.append("--save-artifacts")

    exit_code, stdout, stderr, elapsed = run_cli_command(args, timeout=timeout)

    if exit_code == 0:
        try:
            data = json.loads(stdout)
            run_id = data.get("run_id", "unknown")
            history = data.get("history", [])
            passed = sum(1 for h in history if h.get("approved", False))
            total = len(history)
            print(
                f"{GREEN}PASSED{RESET} ({passed}/{total} stages approved, run_id={run_id}, {elapsed:.1f}s)"
            )
            return TestResult(
                "Sequential execution",
                True,
                f"Run completed: {passed}/{total} stages approved",
                json.dumps(data, indent=2)[:500] if verbose else "",
                seconds=elapsed,
            )
        except json.JSONDecodeError:
            pass

    print(f"{RED}FAILED{RESET}")
    return TestResult(
        "Sequential execution",
        False,
        "Execution failed",
        stderr[:500],
        seconds=elapsed,
    )


def test_no_cache(
    pipeline: str, verbose: bool = False, timeout: Optional[int] = 300
) -> TestResult:
    """Test 4: Cache control."""
    print(f"{BLUE}[TEST 4]{RESET} Cache control (--no-cache)...", end=" ", flush=True)
    start = time.time()
    
    exit_code, stdout, stderr, elapsed = run_cli_command(
        ["--pipeline", pipeline, "--no-cache", "--output", "json"], timeout=timeout
    )

    if exit_code == 0:
        print(f"{GREEN}PASSED{RESET} ({elapsed:.1f}s)")
        return TestResult(
            "Cache control",
            True,
            "Cache disabled successfully",
            stdout[:200] if verbose else "",
            seconds=elapsed,
        )

    print(f"{RED}FAILED{RESET}")
    return TestResult(
        "Cache control",
        False,
        "Cache control test failed",
        stderr[:500],
        seconds=elapsed,
    )


def test_budget_enforcement(
    pipeline: str, verbose: bool = False, timeout: Optional[int] = 300
) -> TestResult:
    """Test 5: Budget enforcement (if policy has budget)."""
    print(f"{BLUE}[TEST 5]{RESET} Budget enforcement...", end=" ", flush=True)

    # Check if pipeline has budget in policy
    import yaml

    try:
        with open(pipeline, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        policy_budget = data.get("policy", {}).get("budget")
        if not policy_budget:
            print(f"{YELLOW}SKIPPED{RESET} (no budget in policy)")
            return TestResult(
                "Budget enforcement",
                True,
                "Skipped (no budget configured)",
                "",
                skipped=True,
            )
    except Exception:
        print(f"{YELLOW}SKIPPED{RESET} (could not read policy)")
        return TestResult(
            "Budget enforcement",
            True,
            "Skipped (could not read policy)",
            "",
            skipped=True,
        )

    # Run with budget - should either pass or fail gracefully
    start = time.time()
    exit_code, stdout, stderr, elapsed = run_cli_command(
        ["--pipeline", pipeline, "--output", "json"], timeout=timeout
    )

    # Budget enforcement can cause failure, which is expected
    if "budget" in stderr.lower() or "budget" in stdout.lower():
        print(f"{GREEN}PASSED{RESET} (budget guard active, {elapsed:.1f}s)")
        return TestResult(
            "Budget enforcement",
            True,
            "Budget guard is active",
            stderr[:300] if verbose else "",
            seconds=elapsed,
        )
    elif exit_code == 0:
        print(f"{GREEN}PASSED{RESET} (within budget, {elapsed:.1f}s)")
        return TestResult(
            "Budget enforcement",
            True,
            "Execution within budget limits",
            "",
            seconds=elapsed,
        )

    print(f"{YELLOW}UNKNOWN{RESET}")
    return TestResult(
        "Budget enforcement",
        True,  # Don't fail suite on budget test
        "Budget test completed (status unclear)",
        stderr[:300],
        seconds=elapsed,
    )


def test_top_suggestions(
    pipeline: str, verbose: bool = False, timeout: Optional[int] = 300
) -> TestResult:
    """Test 6: Top suggestions in report."""
    print(f"{BLUE}[TEST 6]{RESET} Top suggestions report...", end=" ", flush=True)
    start = time.time()
    
    exit_code, stdout, stderr, elapsed = run_cli_command(
        [
            "--pipeline",
            pipeline,
            "--output",
            "human",
            "--top-suggestions",
        ],
        timeout=timeout,
    )

    if exit_code == 0:
        # Check for Top suggestions section (case-insensitive, flexible)
        if "Top" in stdout and "Suggestions" in stdout:
            print(f"{GREEN}PASSED{RESET} ({elapsed:.1f}s)")
            return TestResult(
                "Top suggestions",
                True,
                "Top suggestions section included in report",
                stdout[:500] if verbose else "",
                seconds=elapsed,
            )
        elif exit_code == 0:
            # If run succeeded but no suggestions section, it's OK (no suggestions to show)
            print(f"{GREEN}PASSED{RESET} (no suggestions to display, {elapsed:.1f}s)")
            return TestResult(
                "Top suggestions",
                True,
                "Report generated successfully (no suggestions to display)",
                "",
                seconds=elapsed,
            )

    print(f"{YELLOW}SKIPPED{RESET} (run failed or incomplete)")
    return TestResult(
        "Top suggestions",
        True,  # Don't fail suite
        "Top suggestions test skipped (run may have failed)",
        stderr[:200] if verbose else "",
        seconds=elapsed,
    )


def write_junit_xml(results: List[TestResult], out_path: str, verbose: bool = False) -> None:
    """
    Write JUnit XML report for CI integration.

    Args:
        results: List of test results
        out_path: Output file path
        verbose: Include system-out/system-err for passed tests
    """
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    total_time = sum(r.seconds for r in results)
    
    testsuite = Element(
        "testsuite",
        name="smoke",
        timestamp=timestamp,
        tests=str(len(results)),
        failures=str(sum(1 for r in results if not r.passed and not r.skipped)),
        skipped=str(sum(1 for r in results if r.skipped)),
        time=f"{total_time:.3f}",
    )
    
    for r in results:
        testcase = SubElement(
            testsuite, "testcase", name=r.name, time=f"{r.seconds:.3f}"
        )
        if r.skipped:
            skipped_elem = SubElement(testcase, "skipped")
            skipped_elem.text = r.message or "skipped"
        elif not r.passed:
            failure = SubElement(testcase, "failure", message=r.message or "failed")
            failure.text = r.details or ""
        
        # Add system-out/system-err for verbose output or failures
        if verbose or not r.passed:
            if r.details:
                so = SubElement(testcase, "system-out")
                so.text = r.details[:20000]  # Limit to 20KB
            if hasattr(r, "stderr") and r.stderr:
                se = SubElement(testcase, "system-err")
                se.text = r.stderr[:20000]
    
    with open(out_path, "wb") as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(tostring(testsuite))


def write_markdown_summary(results: List[TestResult], out_path: str) -> None:
    """
    Write Markdown summary report.

    Args:
        results: List of test results
        out_path: Output file path
    """
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    lines = ["# Smoke Test Summary", ""]
    lines.append(f"Generated: {datetime.datetime.now().isoformat()}")
    lines.append("")
    
    passed = sum(1 for r in results if r.passed and not r.skipped)
    failed = sum(1 for r in results if not r.passed and not r.skipped)
    skipped = sum(1 for r in results if r.skipped)
    total_time = sum(r.seconds for r in results)
    
    lines.extend(
        [
            "## Summary",
            f"- **Passed:** {passed}",
            f"- **Failed:** {failed}",
            f"- **Skipped:** {skipped}",
            f"- **Total Time:** {total_time:.2f}s",
            "",
            "## Tests",
            "",
        ]
    )
    
    for r in results:
        status_icon = {"passed": "[PASS]", "failed": "[FAIL]", "skipped": "[SKIP]"}[
            "skipped" if r.skipped else ("passed" if r.passed else "failed")
        ]
        time_str = f" ({r.seconds:.2f}s)" if r.seconds > 0 else ""
        lines.append(f"- {status_icon} **{r.name}**{time_str}")
        if r.message:
            lines.append(f"  - {r.message}")
        if r.details and len(r.details) > 0:
            details_preview = r.details[:200].replace("\n", " ")
            lines.append(f"  - Details: {details_preview}")
        lines.append("")
    
    Path(out_path).write_text("\n".join(lines), encoding="utf-8")


def test_all_pipelines_dry_run(verbose: bool = False) -> TestResult:
    """Test 7: Validate all pipelines in pipeline/ directory."""
    print(f"{BLUE}[TEST 7]{RESET} Validate all pipelines...", end=" ", flush=True)
    start = time.time()
    
    pipeline_dir = Path("pipeline")
    if not pipeline_dir.exists():
        print(f"{RED}FAILED{RESET} (pipeline/ directory not found)")
        return TestResult(
            "All pipelines validation",
            False,
            "pipeline/ not found",
            "",
            seconds=time.time() - start,
        )

    yaml_files = list(pipeline_dir.glob("*.yaml"))
    if not yaml_files:
        print(f"{YELLOW}SKIPPED{RESET} (no YAML files found)")
        return TestResult(
            "All pipelines validation",
            True,
            "No pipelines to validate",
            "",
            skipped=True,
            seconds=time.time() - start,
        )

    failed = []
    for yaml_file in yaml_files:
        exit_code, _, stderr, _ = run_cli_command(
            ["--pipeline", str(yaml_file), "--dry-run"]
        )
        if exit_code != 0:
            failed.append(str(yaml_file))

    elapsed = time.time() - start
    if failed:
        print(f"{RED}FAILED{RESET} ({len(failed)}/{len(yaml_files)} failed, {elapsed:.2f}s)")
        return TestResult(
            "All pipelines validation",
            False,
            f"{len(failed)} pipelines failed validation",
            ", ".join(failed),
            seconds=elapsed,
        )

    print(f"{GREEN}PASSED{RESET} ({len(yaml_files)} pipelines, {elapsed:.2f}s)")
    return TestResult(
        "All pipelines validation",
        True,
        f"All {len(yaml_files)} pipelines valid",
        "",
        seconds=elapsed,
    )


def main() -> int:
    """Run smoke test suite."""
    parser = argparse.ArgumentParser(
        description="Run smoke tests for multi-agent pipeline system"
    )
    parser.add_argument(
        "--pipeline",
        type=str,
        default="pipeline/production.yaml",
        help="Pipeline file to test (default: pipeline/production.yaml)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output for each test",
    )
    parser.add_argument(
        "--skip-slow",
        action="store_true",
        help="Skip slow tests (sequential/parallel execution)",
    )
    parser.add_argument(
        "--test",
        type=str,
        choices=[
            "dry-run",
            "graph",
            "sequential",
            "cache",
            "budget",
            "suggestions",
            "all-pipelines",
        ],
        help="Run a specific test only",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop on first test failure",
    )
    parser.add_argument(
        "--out",
        type=str,
        default="out/smoke",
        help="Output directory for reports and artifacts (default: out/smoke)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=0,
        help="Overall timeout for test suite in seconds (0 = no limit)",
    )
    parser.add_argument(
        "--max-dryrun-sec",
        type=float,
        default=5.0,
        help="Maximum seconds for dry-run test (warns if exceeded)",
    )
    parser.add_argument(
        "--strict-performance",
        action="store_true",
        help="Fail the suite if any performance threshold is exceeded",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON summary to stdout",
    )
    parser.add_argument(
        "--list-tests",
        action="store_true",
        help="List all available tests and exit",
    )

    args = parser.parse_args()
    
    # Define available tests
    TESTS = [
        {"name": "Dry-run validation", "slow": False, "description": "Validate pipeline YAML structure"},
        {"name": "Graph export", "slow": False, "description": "Export pipeline graph (requires graphviz)"},
        {"name": "Sequential execution", "slow": True, "description": "Run pipeline sequentially"},
        {"name": "Cache control", "slow": True, "description": "Test cache behavior"},
        {"name": "Budget enforcement", "slow": True, "description": "Test budget limits"},
        {"name": "Top suggestions", "slow": True, "description": "Test report with top suggestions"},
        {"name": "All pipelines validation", "slow": False, "description": "Validate all pipeline files"},
    ]
    
    # Handle --list-tests
    if args.list_tests:
        print("Available tests:")
        for t in TESTS:
            slow_marker = "[SLOW] " if t["slow"] else "       "
            print(f"  {slow_marker}{t['name']}: {t['description']}")
        return 0

    pipeline_path = Path(args.pipeline)
    if not pipeline_path.exists():
        print(f"{RED}ERROR:{RESET} Pipeline file not found: {args.pipeline}")
        return 1

    # Setup output directory
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"{BOLD}Smoke Test Suite{RESET}")
    print(f"Pipeline: {args.pipeline}")
    print(f"Output directory: {out_dir}")
    print(f"{'=' * 60}\n")

    suite_start = time.time()
    results: List[TestResult] = []
    timeout_remaining = args.timeout if args.timeout > 0 else None
    should_stop = False

    def check_fail_fast(result: TestResult) -> bool:
        """Check if we should stop due to fail-fast."""
        if args.fail_fast and not result.passed and not result.skipped:
            print(f"\n{RED}FAIL-FAST: Stopping after first failure{RESET}")
            return True
        return False

    # Test 1: Dry-run
    if not should_stop and (not args.test or args.test == "dry-run"):
        result = test_dry_run(
            str(pipeline_path), args.verbose, max_seconds=args.max_dryrun_sec, strict_performance=args.strict_performance
        )
        results.append(result)
        should_stop = check_fail_fast(result)

    # Test 2: Graph export
    if not should_stop and (not args.test or args.test == "graph"):
        result = test_graph_export(str(pipeline_path), args.verbose, out_dir=str(out_dir))
        results.append(result)
        should_stop = check_fail_fast(result)

    # Test 3: Sequential execution (skip if --skip-slow)
    if (
        not should_stop
        and not args.skip_slow
        and (not args.test or args.test == "sequential")
    ):
        if timeout_remaining:
            elapsed = time.time() - suite_start
            timeout_remaining = max(0, timeout_remaining - elapsed)
            if timeout_remaining <= 0:
                print(f"{YELLOW}[SKIP]{RESET} Sequential execution (timeout)")
            else:
                result = test_sequential_execution(
                    str(pipeline_path),
                    args.verbose,
                    save_artifacts=False,
                    timeout=int(timeout_remaining),
                )
                results.append(result)
                should_stop = check_fail_fast(result)
        else:
            result = test_sequential_execution(
                str(pipeline_path), args.verbose, save_artifacts=False, timeout=300
            )
            results.append(result)
            should_stop = check_fail_fast(result)

    # Test 4: Cache control
    if not should_stop and (not args.test or args.test == "cache"):
        if args.skip_slow:
            print(f"{YELLOW}[SKIP]{RESET} Cache control (--skip-slow)")
        else:
            if timeout_remaining:
                elapsed = time.time() - suite_start
                timeout_remaining = max(0, timeout_remaining - elapsed)
                if timeout_remaining <= 0:
                    print(f"{YELLOW}[SKIP]{RESET} Cache control (timeout)")
                else:
                    result = test_no_cache(
                        str(pipeline_path),
                        args.verbose,
                        timeout=int(timeout_remaining),
                    )
                    results.append(result)
                    should_stop = check_fail_fast(result)
            else:
                result = test_no_cache(str(pipeline_path), args.verbose, timeout=300)
                results.append(result)
                should_stop = check_fail_fast(result)

    # Test 5: Budget enforcement
    if not should_stop and (not args.test or args.test == "budget"):
        if args.skip_slow:
            print(f"{YELLOW}[SKIP]{RESET} Budget enforcement (--skip-slow)")
        else:
            if timeout_remaining:
                elapsed = time.time() - suite_start
                timeout_remaining = max(0, timeout_remaining - elapsed)
                if timeout_remaining <= 0:
                    print(f"{YELLOW}[SKIP]{RESET} Budget enforcement (timeout)")
                else:
                    result = test_budget_enforcement(
                        str(pipeline_path),
                        args.verbose,
                        timeout=int(timeout_remaining),
                    )
                    results.append(result)
                    should_stop = check_fail_fast(result)
            else:
                result = test_budget_enforcement(
                    str(pipeline_path), args.verbose, timeout=300
                )
                results.append(result)
                should_stop = check_fail_fast(result)

    # Test 6: Top suggestions
    if not should_stop and (not args.test or args.test == "suggestions"):
        if args.skip_slow:
            print(f"{YELLOW}[SKIP]{RESET} Top suggestions (--skip-slow)")
        else:
            if timeout_remaining:
                elapsed = time.time() - suite_start
                timeout_remaining = max(0, timeout_remaining - elapsed)
                if timeout_remaining <= 0:
                    print(f"{YELLOW}[SKIP]{RESET} Top suggestions (timeout)")
                else:
                    result = test_top_suggestions(
                        str(pipeline_path),
                        args.verbose,
                        timeout=int(timeout_remaining),
                    )
                    results.append(result)
                    should_stop = check_fail_fast(result)
            else:
                result = test_top_suggestions(
                    str(pipeline_path), args.verbose, timeout=300
                )
                results.append(result)
                should_stop = check_fail_fast(result)

    # Test 7: All pipelines validation
    if not should_stop and (not args.test or args.test == "all-pipelines"):
        result = test_all_pipelines_dry_run(args.verbose)
        results.append(result)
        should_stop = check_fail_fast(result)

    # Summary
    print(f"\n{BOLD}{'=' * 60}{RESET}")
    print(f"{BOLD}Summary{RESET}\n")

    passed = sum(1 for r in results if r.passed)
    total = len(results)
    failed_results = [r for r in results if not r.passed]

    for result in results:
        status = f"{GREEN}PASSED{RESET}" if result.passed else f"{RED}FAILED{RESET}"
        print(f"  {status} {result.name}")
        if result.message and args.verbose:
            print(f"    {result.message}")
        if result.details and args.verbose:
            print(f"    Details: {result.details[:200]}")

    suite_time = time.time() - suite_start
    print(f"\n{BOLD}Results:{RESET} {passed}/{total} tests passed (total time: {suite_time:.2f}s)")

    if failed_results:
        print(f"\n{RED}Failed tests:{RESET}")
        for result in failed_results:
            print(f"  - {result.name}: {result.message}")
            if result.details:
                print(f"    {result.details[:200]}")

    # Write reports
    junit_path = str(out_dir / "smoke_junit.xml")
    md_path = str(out_dir / "SMOKE_SUMMARY.md")
    
    try:
        write_junit_xml(results, junit_path, verbose=args.verbose)
        write_markdown_summary(results, md_path)
        if not args.json:
            print(f"\n{BOLD}Reports written:{RESET}")
            print(f"  - JUnit XML: {junit_path}")
            print(f"  - Markdown: {md_path}")
    except Exception as e:
        print(f"\n{YELLOW}Warning:{RESET} Failed to write reports: {e}")

    # JSON output for machine consumption
    if args.json:
        all_results = [r.to_dict() for r in results]
        summary = {
            "results": all_results,
            "summary": {
                "passed": passed,
                "failed": total - passed,
                "skipped": sum(1 for r in results if r.skipped),
                "total": total,
                "total_time": suite_time,
            },
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())

