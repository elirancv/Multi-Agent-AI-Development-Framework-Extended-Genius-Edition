"""KPI aggregation utilities for hard tests."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, Any


def aggregate_kpis(run_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Aggregate KPIs from pipeline run result.
    
    Args:
        run_result: Pipeline execution result dictionary
        
    Returns:
        Dictionary with aggregated KPIs
    """
    hist = run_result.get("history", [])
    
    total_ms = sum(int(s.get("duration_ms", 0)) for s in hist)
    approved = sum(1 for s in hist if s.get("approved"))
    avg_score = (
        sum(float(s.get("score", 0.0)) for s in hist) / max(1, len(hist))
    )
    timeouts = sum(1 for s in hist if s.get("error_reason") == "timeout")
    exhausted = sum(1 for s in hist if s.get("error_reason") == "exhausted_retries")
    artifacts_bytes = int(run_result.get("artifacts_bytes", 0))
    cache_hits = int(run_result.get("cache_hits", 0))
    
    return {
        "stages": len(hist),
        "approved_ratio": round(approved / max(1, len(hist)), 3),
        "avg_score": round(avg_score, 3),
        "total_duration_ms": total_ms,
        "timeouts": timeouts,
        "exhausted_retries": exhausted,
        "artifacts_bytes": artifacts_bytes,
        "cache_hits": cache_hits,
    }


def write_kpis(out_dir: str, kpis: Dict[str, Any]) -> None:
    """
    Write KPIs to JSON and CSV files.
    
    Args:
        out_dir: Output directory
        kpis: KPI dictionary
    """
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    
    # Write JSON
    json_path = out / "kpis.json"
    json_path.write_text(
        json.dumps(kpis, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    
    # Write CSV
    csv_path = out / "kpis.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(kpis.keys())
        writer.writerow(kpis.values())
    
    print(f"KPIs written to {json_path} and {csv_path}")


def generate_kpi_markdown(kpis: Dict[str, Any], out_path: str) -> None:
    """
    Generate Markdown summary from KPIs.
    
    Args:
        kpis: KPI dictionary
        out_path: Output file path
    """
    md_lines = [
        "# KPI Summary",
        "",
        "## Execution Metrics",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Stages Completed | {kpis.get('stages', 0)} |",
        f"| Approved Ratio | {kpis.get('approved_ratio', 0.0):.1%} |",
        f"| Average Score | {kpis.get('avg_score', 0.0):.3f} |",
        f"| Total Duration | {kpis.get('total_duration_ms', 0) / 1000:.2f}s |",
        "",
        "## Error Metrics",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Timeouts | {kpis.get('timeouts', 0)} |",
        f"| Exhausted Retries | {kpis.get('exhausted_retries', 0)} |",
        "",
        "## Resource Metrics",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Artifacts Size | {kpis.get('artifacts_bytes', 0) / (1024**2):.2f} MB |",
        f"| Cache Hits | {kpis.get('cache_hits', 0)} |",
        "",
    ]
    
    # Add status indicators
    approved_ratio = kpis.get("approved_ratio", 0.0)
    avg_score = kpis.get("avg_score", 0.0)
    
    status = "✅ PASS" if approved_ratio >= 0.95 and avg_score >= 0.85 else "⚠️ WARN" if approved_ratio >= 0.8 else "❌ FAIL"
    
    md_lines.extend([
        "## Status",
        "",
        f"**{status}**",
        "",
        f"- Approved Ratio: {'✅' if approved_ratio >= 0.95 else '⚠️' if approved_ratio >= 0.8 else '❌'} {approved_ratio:.1%}",
        f"- Average Score: {'✅' if avg_score >= 0.85 else '⚠️' if avg_score >= 0.7 else '❌'} {avg_score:.3f}",
        "",
    ])
    
    Path(out_path).write_text("\n".join(md_lines), encoding="utf-8")
    print(f"KPI Markdown summary written to {out_path}")

