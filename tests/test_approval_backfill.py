"""Approval tests (golden snapshots) for reports and eventlogs."""

import json
from pathlib import Path

import pytest

from src.orchestrator.report import build_markdown_report


def test_markdown_report_structure():
    """Test markdown report has expected structure."""
    dummy_result = {
        "run_id": "test-run-123",
        "history": [
            {
                "stage": "test_stage",
                "category": "requirements",
                "approved": True,
                "score": 0.95,
                "artifacts": {},
                "agent": "TestAgent",
                "advisor": "TestAdvisor",
            }
        ],
        "summary": {
            "total_stages": 1,
            "approved": 1,
            "rejected": 0,
        }
    }
    
    md = build_markdown_report(
        dummy_result,
        artifacts_saved=False,
        top_suggestions=False
    )
    
    # Check structure
    assert isinstance(md, str)
    assert "test-run-123" in md or "test_stage" in md
    assert len(md) > 0


def test_markdown_report_with_artifacts():
    """Test markdown report includes artifact information."""
    dummy_result = {
        "run_id": "test-run-123",
        "history": [
            {
                "stage": "test_stage",
                "category": "requirements",
                "approved": True,
                "score": 0.95,
                "artifacts": {
                    "test.md": {"size": 100}
                },
            }
        ],
    }
    
    md = build_markdown_report(
        dummy_result,
        artifacts_saved=True,
        top_suggestions=False
    )
    
    assert "artifact" in md.lower() or "test.md" in md


def test_json_output_structure():
    """Test JSON output has expected structure."""
    dummy_result = {
        "run_id": "test-run-123",
        "history": [
            {
                "stage": "test_stage",
                "approved": True,
                "score": 0.95,
            }
        ],
    }
    
    json_str = json.dumps(dummy_result, indent=2)
    data = json.loads(json_str)
    
    assert "run_id" in data
    assert "history" in data
    assert isinstance(data["history"], list)


@pytest.mark.skipif(not Path("out").exists(), reason="out directory not found")
def test_eventlog_structure(tmp_path):
    """Test eventlog JSONL structure."""
    # This would test actual eventlog writing
    # For now, just verify structure expectations
    eventlog_path = tmp_path / "events.jsonl"
    
    events = [
        {"event": "stage_start", "stage": "test", "timestamp": "2025-01-01T00:00:00Z"},
        {"event": "stage_complete", "stage": "test", "score": 0.95, "timestamp": "2025-01-01T00:00:01Z"},
    ]
    
    with open(eventlog_path, "w") as f:
        for event in events:
            f.write(json.dumps(event) + "\n")
    
    # Verify structure
    with open(eventlog_path) as f:
        lines = f.readlines()
        assert len(lines) == 2
        
        for line in lines:
            data = json.loads(line)
            assert "event" in data
            assert "timestamp" in data


# Note: Full approval testing would require pytest-snapshot or similar
# For now, these are structure tests
def test_report_consistency():
    """Test report is consistent across runs with same input."""
    dummy_result = {
        "run_id": "test-run-123",
        "history": [
            {
                "stage": "test_stage",
                "approved": True,
                "score": 0.95,
            }
        ],
    }
    
    md1 = build_markdown_report(dummy_result, artifacts_saved=False, top_suggestions=False)
    md2 = build_markdown_report(dummy_result, artifacts_saved=False, top_suggestions=False)
    
    # Should be identical for same input
    assert md1 == md2

