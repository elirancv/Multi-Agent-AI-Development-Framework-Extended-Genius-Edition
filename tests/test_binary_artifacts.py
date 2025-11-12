"""Test binary artifact support."""

from pathlib import Path

from src.orchestrator.artifact_sink import persist_artifacts, _safe_name


def test_safe_name_sanitization() -> None:
    """Test filename sanitization."""
    assert _safe_name("normal_file.txt") == "normal_file.txt"
    assert _safe_name("file with spaces.md") == "file with spaces.md"
    assert _safe_name("file/with/slashes.txt") == "file_with_slashes.txt"
    assert _safe_name("file*with*stars.txt") == "file_with_stars.txt"
    assert len(_safe_name("a" * 200)) <= 120


def test_binary_artifact_persistence(tmp_path: Path) -> None:
    """Test binary artifact persistence."""
    binary_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
    result = {
        "run_id": "r_binary",
        "history": [{"stage": "s1", "approved": True, "score": 0.9}],
        "memory": {
            "s1.artifacts": [
                {"name": "image.png", "type": "binary", "content": binary_content}
            ],
        },
    }

    count = persist_artifacts(result, out_dir=str(tmp_path))
    assert count == 1
    artifact_file = tmp_path / "r_binary" / "s1" / "image.png"
    assert artifact_file.exists()
    assert artifact_file.read_bytes() == binary_content


def test_base64_artifact_decoding(tmp_path: Path) -> None:
    """Test base64 string artifact decoding."""
    import base64

    original_content = b"Hello, binary world!"
    base64_content = base64.b64encode(original_content).decode("utf-8")

    result = {
        "run_id": "r_base64",
        "history": [{"stage": "s1", "approved": True, "score": 0.9}],
        "memory": {
            "s1.artifacts": [
                {"name": "data.bin", "type": "binary", "content": base64_content}
            ],
        },
    }

    count = persist_artifacts(result, out_dir=str(tmp_path))
    assert count == 1
    artifact_file = tmp_path / "r_base64" / "s1" / "data.bin"
    assert artifact_file.exists()
    # Should be decoded from base64
    assert artifact_file.read_bytes() == original_content

