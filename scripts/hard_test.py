"""Hard tests with KPI tracking for nightly runs."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Any

from scripts.kpi_aggregator import aggregate_kpis, write_kpis


def run_hard_test(
    pipeline: str,
    parallel: bool = False,
    max_workers: int = 4,
    save_artifacts: bool = False,
    out_dir: str = "out/hard-tests",
) -> Dict[str, Any]:
    """Run hard test pipeline and collect KPIs."""
    start_time = time.time()
    
    # Build CLI args
    cmd = ["python", "cli.py", "--pipeline", pipeline, "--output", "json"]
    
    if parallel:
        cmd.extend(["--parallel", "--max-workers", str(max_workers)])
    
    if save_artifacts:
        cmd.append("--save-artifacts")
    
    # Run pipeline
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=900,  # 15 min timeout
        )
        
        execution_time = time.time() - start_time
        
        # Parse JSON output
        try:
            run_result = json.loads(result.stdout) if result.stdout else {}
        except json.JSONDecodeError:
            run_result = {}
        
        # Aggregate KPIs
        kpis = aggregate_kpis(run_result)
        kpis["execution_time_sec"] = execution_time
        kpis["exit_code"] = result.returncode
        
        return kpis
        
    except subprocess.TimeoutExpired:
        return {
            "execution_time_sec": time.time() - start_time,
            "stages": 0,
            "approved_ratio": 0.0,
            "avg_score": 0.0,
            "total_duration_ms": 0,
            "timeouts": 1,
            "exhausted_retries": 0,
            "artifacts_bytes": 0,
            "cache_hits": 0,
            "exit_code": 124,
            "error": "timeout",
        }
    except Exception as e:
        return {
            "execution_time_sec": time.time() - start_time,
            "stages": 0,
            "approved_ratio": 0.0,
            "avg_score": 0.0,
            "total_duration_ms": 0,
            "timeouts": 0,
            "exhausted_retries": 0,
            "artifacts_bytes": 0,
            "cache_hits": 0,
            "exit_code": 1,
            "error": str(e),
        }


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run hard tests with KPI tracking")
    parser.add_argument("--pipeline", required=True, help="Pipeline YAML file")
    parser.add_argument("--parallel", action="store_true", help="Use parallel execution")
    parser.add_argument("--max-workers", type=int, default=4, help="Max parallel workers")
    parser.add_argument("--save-artifacts", action="store_true", help="Save artifacts")
    parser.add_argument("--out", type=str, default="out/hard-tests", help="Output directory")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    
    args = parser.parse_args()
    
    kpis = run_hard_test(
        pipeline=args.pipeline,
        parallel=args.parallel,
        max_workers=args.max_workers,
        save_artifacts=args.save_artifacts,
        out_dir=args.out,
    )
    
    # Write KPIs to files
    write_kpis(args.out, kpis)
    
    # Generate Markdown summary
    from scripts.kpi_aggregator import generate_kpi_markdown
    generate_kpi_markdown(kpis, str(Path(args.out) / "KPIS_SUMMARY.md"))
    
    if args.json:
        print(json.dumps(kpis, indent=2))
    else:
        print("\nKPI Report:")
        for key, value in kpis.items():
            print(f"  {key}: {value}")
    
    # Success criteria: approved_ratio >= 0.95 and avg_score >= 0.85
    success = (
        kpis.get("approved_ratio", 0.0) >= 0.95
        and kpis.get("avg_score", 0.0) >= 0.85
    )
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

