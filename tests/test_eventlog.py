"""Test event log."""

from pathlib import Path

from src.orchestrator.eventlog import JsonlEventLog


def test_eventlog_emits_events(tmp_path: Path) -> None:
    """Test that event log emits events to JSONL file."""

    log_path = tmp_path / "events.jsonl"
    log = JsonlEventLog(path=str(log_path))

    log.emit("test_event", stage="s1", score=0.9)
    log.emit("another_event", agent="A", approved=True)

    assert log_path.exists()
    lines = log_path.read_text(encoding="utf-8").strip().split("\n")
    assert len(lines) == 2

    import json

    first = json.loads(lines[0])
    assert first["event"] == "test_event"
    assert first["stage"] == "s1"
    assert first["score"] == 0.9
    assert "ts" in first

    second = json.loads(lines[1])
    assert second["event"] == "another_event"
    assert second["agent"] == "A"
    assert second["approved"] is True


def test_eventlog_creates_parent_dirs(tmp_path: Path) -> None:
    """Test that event log creates parent directories."""

    log_path = tmp_path / "nested" / "dir" / "events.jsonl"
    log = JsonlEventLog(path=str(log_path))

    log.emit("test", data="value")

    assert log_path.exists()
    assert log_path.parent.exists()
