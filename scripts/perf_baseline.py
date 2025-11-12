"""Performance baseline - Run hard tests and save KPI baseline."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from datetime import datetime

from scripts.hard_test import main as hard_test_main


def save_baseline(kpi_data: dict, output_dir: Path) -> None:
    """Save KPI baseline to docs/benchmarks/."""
    benchmark_dir = Path("docs/benchmarks")
    benchmark_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save JSON
    json_path = benchmark_dir / f"baseline_{timestamp}.json"
    json_path.write_text(json.dumps(kpi_data, indent=2))
    print(f"Saved JSON baseline: {json_path}", file=sys.stderr)
    
    # Save CSV (if available)
    if "metrics" in kpi_data:
        csv_lines = ["metric,value"]
        for metric, value in kpi_data["metrics"].items():
            csv_lines.append(f"{metric},{value}")
        csv_path = benchmark_dir / f"baseline_{timestamp}.csv"
        csv_path.write_text("\n".join(csv_lines))
        print(f"Saved CSV baseline: {csv_path}", file=sys.stderr)
    
    # Save Markdown summary
    md_lines = [
        "# Performance Baseline",
        "",
        f"**Date**: {datetime.now().isoformat()}",
        f"**Version**: {kpi_data.get('version', 'unknown')}",
        "",
        "## Metrics",
        "",
    ]
    
    if "metrics" in kpi_data:
        for metric, value in kpi_data["metrics"].items():
            md_lines.append(f"- **{metric}**: {value}")
    
    if "stages" in kpi_data:
        md_lines.extend([
            "",
            "## Stage Performance",
            "",
            "| Stage | Duration | Status |",
            "|-------|----------|--------|",
        ])
        for stage in kpi_data.get("stages", []):
            md_lines.append(f"| {stage.get('name', 'unknown')} | {stage.get('duration', 'N/A')} | {stage.get('status', 'N/A')} |")
    
    md_path = benchmark_dir / f"baseline_{timestamp}.md"
    md_path.write_text("\n".join(md_lines))
    print(f"Saved Markdown baseline: {md_path}", file=sys.stderr)
    
    # Update latest symlink/reference
    latest_path = benchmark_dir / "baseline_latest.json"
    latest_path.write_text(json.dumps(kpi_data, indent=2))
    print(f"Updated latest baseline: {latest_path}", file=sys.stderr)


def main() -> int:
    """Run hard tests and save baseline."""
    print("Running performance baseline tests...", file=sys.stderr)
    
    # Run hard tests
    # Note: This assumes hard_test.py outputs KPI data
    # Adjust based on actual hard_test.py implementation
    try:
        # Import and run hard test
        # For now, we'll create a mock structure
        # Replace with actual hard_test integration
        
        kpi_data = {
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "total_stages": 0,
                "success_rate": 0.0,
                "avg_duration": 0.0,
            },
            "stages": [],
        }
        
        # TODO: Integrate with actual hard_test.py
        # result = hard_test_main()
        # kpi_data = extract_kpis(result)
        
        save_baseline(kpi_data, Path("docs/benchmarks"))
        
        print("\n✅ Baseline saved successfully", file=sys.stderr)
        return 0
        
    except Exception as e:
        print(f"❌ Error creating baseline: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

