"""Tests for artifact diff utilities."""

from src.orchestrator.artifact_diff import diff_text, diff_summary


def test_diff_text_same():
    """Test that identical text produces empty diff."""
    text = "line1\nline2\nline3"
    diff = diff_text(text, text)
    assert diff == ""


def test_diff_text_different():
    """Test that different text produces diff."""
    old = "line1\nline2\nline3"
    new = "line1\nline2_modified\nline3"
    diff = diff_text(old, new)
    assert "line2" in diff
    assert "line2_modified" in diff


def test_diff_summary():
    """Test that diff summary counts changes correctly."""
    old = "line1\nline2\nline3"
    new = "line1\nline2_modified\nline3\nline4"
    added, removed = diff_summary(old, new)
    assert added > 0 or removed > 0

