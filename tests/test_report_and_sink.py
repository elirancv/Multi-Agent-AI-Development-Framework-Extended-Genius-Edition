"""Test markdown report and artifact sink."""

from pathlib import Path

from src.orchestrator.artifact_sink import persist_artifacts
from src.orchestrator.report import build_markdown_report


def test_markdown_report() -> None:
    """Test markdown report generation."""
    result = {
        "run_id": "r1",
        "history": [{"stage": "s1", "approved": True, "score": 0.9}],
        "memory": {
            "s1.artifacts": [{"name": "a.txt", "type": "text", "content": "ok"}],
            "s1.review": {
                "approved": True,
                "score": 0.9,
                "critical_issues": [],
                "suggestions": [],
            },
        },
    }
    md = build_markdown_report(result)
    assert "# Pipeline Run Report" in md
    assert "s1" in md
    assert "0.9" in md


def test_artifact_sink(tmp_path: Path) -> None:
    """Test artifact persistence to filesystem."""
    result = {
        "run_id": "r1",
        "history": [{"stage": "s1", "approved": True, "score": 0.9}],
        "memory": {
            "s1.artifacts": [{"name": "a.txt", "type": "text", "content": "ok"}],
            "s1.review": {
                "approved": True,
                "score": 0.9,
                "critical_issues": [],
                "suggestions": [],
            },
        },
    }

    count = persist_artifacts(result, out_dir=str(tmp_path))
    assert count == 1
    out = tmp_path / "r1"
    assert (out / "s1" / "a.txt").exists()
    assert (out / "SUMMARY.md").exists()
    assert (out / "manifest.json").exists()
    assert (out / "s1" / "a.txt").read_text() == "ok"


def test_artifact_sink_multiple_stages(tmp_path: Path) -> None:
    """Test artifact sink with multiple stages."""
    result = {
        "run_id": "r2",
        "history": [
            {"stage": "s1", "approved": True, "score": 0.9},
            {"stage": "s2", "approved": False, "score": 0.7},
        ],
        "memory": {
            "s1.artifacts": [{"name": "a.txt", "type": "text", "content": "stage1"}],
            "s2.artifacts": [{"name": "b.txt", "type": "text", "content": "stage2"}],
        },
    }

    count = persist_artifacts(result, out_dir=str(tmp_path))
    assert count == 2
    out = tmp_path / "r2"
    assert (out / "s1" / "a.txt").exists()
    assert (out / "s2" / "b.txt").exists()
    assert (out / "SUMMARY.md").exists()
    assert (out / "manifest.json").exists()
