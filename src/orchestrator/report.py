"""Markdown report generator for pipeline runs."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List

from .artifact_diff import diff_text


def build_markdown_report(
    result: Dict[str, Any], artifacts_saved: bool = False, top_suggestions: bool = False
) -> str:
    """
    Build a human-friendly run report in Markdown from orchestrator result.

    Expected result keys: run_id, history, memory.

    Args:
        result: Orchestrator result dictionary
        artifacts_saved: Whether artifacts were saved to filesystem (enables relative links)
    """
    run_id = result.get("run_id", "unknown")
    history: List[Dict[str, Any]] = result.get("history", [])
    mem: Dict[str, Any] = result.get("memory", {})
    art_root = f"out/{run_id}" if artifacts_saved else None

    lines: List[str] = []
    lines.append("# Pipeline Run Report")
    lines.append(f"- **Run ID:** `{run_id}`")
    lines.append(
        f"- **Generated:** {datetime.now(timezone.utc).isoformat(timespec='seconds')}"
    )
    lines.append("")

    lines.append("## Summary")
    if history:
        passed = sum(1 for h in history if h.get("approved"))
        lines.append(
            f"- **Stages:** {len(history)}  |  **Approved:** {passed}  |  **Failed:** {len(history)-passed}"
        )
        avg = sum(h.get("score", 0.0) for h in history) / max(1, len(history))
        lines.append(f"- **Average Score:** {avg:.2f}")
    else:
        lines.append("- No stages executed.")

    # Collect all suggestions for top suggestions section
    all_suggestions: List[Dict[str, Any]] = []
    
    lines.append("\n## Stages")
    for h in history:
        stage = h["stage"]
        score = h.get("score", 0.0)
        ok = "[PASS]" if h.get("approved") else "[FAIL]"
        cat = h.get("category") or "default"
        error_reason = h.get("error_reason")
        
        # Get duration from memory or checkpoint
        stage_metadata = mem.get(f"{stage}.metadata", {})
        duration_ms = stage_metadata.get("duration_ms")
        if not duration_ms:
            # Try to get from checkpoint if available
            checkpoint_extra = mem.get(f"{stage}.checkpoint_extra", {})
            duration_ms = checkpoint_extra.get("duration_ms")
        
        status_line = f"### {ok} {stage}  —  score: **{score:.2f}**  |  category: `{cat}`"
        if duration_ms:
            status_line += f"  |  duration: **{duration_ms} ms**"
        if error_reason:
            status_line += f"  |  error: `{error_reason}`"
        lines.append(status_line)

        # Basic artifact teaser from memory
        arts = mem.get(f"{stage}.artifacts") or []
        if arts:
            lines.append("**Artifacts:**")
            for a in arts:
                name = a.get("name", "artifact")
                art_type = a.get("type", "unknown")
                if art_root:
                    # Add relative link if artifacts were saved
                    link = f"[`{name}`]({art_root}/{stage}/{name})"
                else:
                    link = f"`{name}`"
                lines.append(f"- {link} · type=`{art_type}`")
                
                # Show diff if previous content exists (from checkpoint/resume)
                current_content = mem.get(f"{stage}.content", "")
                previous_content = mem.get(f"{stage}.previous_content")
                if previous_content and current_content and previous_content != current_content:
                    diff_snippet = diff_text(str(previous_content), str(current_content), context=2)
                    if diff_snippet.strip():
                        lines.append(f"\n**Diff (unified):**\n\n```diff\n{diff_snippet}\n```")

        # Advisor review snippet
        rev = mem.get(f"{stage}.review") or {}
        if rev:
            lines.append("**Review:**")
            lines.append(
                f"- approved={rev.get('approved')}  |  score={rev.get('score')}"
            )
            crit = rev.get("critical_issues") or []
            sug = rev.get("suggestions") or []
            if crit:
                lines.append("- Critical issues:")
                for c in crit[:5]:
                    lines.append(f"  - {c}")
            if sug:
                lines.append("- Suggestions:")
                for s in sug[:5]:
                    lines.append(f"  - {s}")
                    # Collect for top suggestions
                    all_suggestions.append({"stage": stage, "suggestion": s, "score": score})

        lines.append("")

    # Top 5 suggestions section
    if top_suggestions and all_suggestions:
        lines.append("\n## Top 5 Suggestions")
        # Sort by score (highest first) and take top 5
        sorted_suggestions = sorted(all_suggestions, key=lambda x: x["score"], reverse=True)[:5]
        for i, sug in enumerate(sorted_suggestions, 1):
            lines.append(f"{i}. **{sug['stage']}** (score: {sug['score']:.2f}): {sug['suggestion']}")

    return "\n".join(lines)

