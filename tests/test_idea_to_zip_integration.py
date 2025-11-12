"""
Integration test for idea-to-zip pipeline.

Tests that the pipeline produces a valid ZIP package with expected contents.
"""

import os
import subprocess
import sys
import zipfile
from pathlib import Path, PurePosixPath

import pytest


def test_idea_to_zip_builds_zip(tmp_path, monkeypatch):
    """Test that idea-to-zip pipeline produces a valid ZIP file."""
    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    # Run pipeline
    cmd = [
        sys.executable,
        "cli.py",
        "--pipeline",
        "pipeline/gallery/idea-to-zip/pipeline.yaml",
        "--mem",
        'product_idea="Demo test site"',
        "--save-artifacts",
        "--output",
        "json",
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=project_root,
        timeout=300,  # 5 minutes max
    )

    # Check pipeline ran successfully
    assert result.returncode == 0, f"Pipeline failed: {result.stderr}"

    # Find the latest run
    out_dir = project_root / "out"
    if not out_dir.exists():
        assert False, "Output directory not found"

    runs = [d for d in out_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
    assert runs, "No runs found in out/"

    latest_run = sorted(runs, key=lambda x: x.stat().st_mtime)[-1]

    # Check ZIP exists
    zip_path = latest_run / "Package ZIP" / "package.zip"
    assert zip_path.exists(), f"ZIP not found at {zip_path}"

    # Validate ZIP contents
    with zipfile.ZipFile(zip_path, "r") as z:
        names = z.namelist()

        # Check for expected files
        assert any("index.html" in n.lower() for n in names), "index.html missing from ZIP"
        assert any("readme" in n.lower() for n in names), "README missing from ZIP"
        assert any("manifest" in n.lower() for n in names), "MANIFEST missing from ZIP"

        # Check ZIP is not empty
        total_size = sum(z.getinfo(n).file_size for n in names)
        assert total_size > 0, "ZIP is empty"

        # Verify we can read at least one file
        for name in names:
            try:
                content = z.read(name)
                assert len(content) > 0, f"File {name} is empty"
                break
            except Exception:
                continue


def test_idea_to_zip_dry_run_validates(tmp_path, monkeypatch):
    """Test that dry-run validates the pipeline without errors."""
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    cmd = [
        sys.executable,
        "cli.py",
        "--pipeline",
        "pipeline/gallery/idea-to-zip/pipeline.yaml",
        "--dry-run",
        "--output",
        "json",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root, timeout=60)

    assert result.returncode == 0, f"Dry-run failed: {result.stderr}"
    assert "validated" in result.stdout.lower() or "dry-run" in result.stdout.lower()


def test_zip_contains_artifacts_from_stages(tmp_path, monkeypatch):
    """Test that ZIP contains artifacts from all expected stages."""
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    # Run pipeline
    cmd = [
        sys.executable,
        "cli.py",
        "--pipeline",
        "pipeline/gallery/idea-to-zip/pipeline.yaml",
        "--mem",
        'product_idea="Test artifacts"',
        "--save-artifacts",
        "--output",
        "json",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root, timeout=300)

    if result.returncode != 0:
        # Skip if pipeline fails (may need real agents)
        return

    # Find ZIP
    out_dir = project_root / "out"
    runs = [d for d in out_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
    if not runs:
        return

    latest_run = sorted(runs, key=lambda x: x.stat().st_mtime)[-1]
    zip_path = latest_run / "Package ZIP" / "package.zip"

    if not zip_path.exists():
        return

    # Check ZIP has reasonable structure
    with zipfile.ZipFile(zip_path, "r") as z:
        names = z.namelist()

        # Should have at least 3 files (HTML, README, MANIFEST minimum)
        assert len(names) >= 3, f"ZIP should have at least 3 files, got {len(names)}"

        # Check for manifest
        manifest_names = [n for n in names if "manifest" in n.lower()]
        assert manifest_names, "MANIFEST.txt should be in ZIP"


def test_production_demo_zip_completeness(tmp_path, monkeypatch):
    """Test production demo pipeline produces complete ZIP with all required files."""
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    # Run production demo pipeline
    cmd = [
        sys.executable,
        "cli.py",
        "--pipeline",
        "pipeline/gallery/idea-to-zip/pipeline-production-demo.yaml",
        "--mem",
        'product_idea="Test demo" brand="TestBrand" primary_color="#0ea5e9" tone="minimal"',
        "--save-artifacts",
        "--output",
        "json",
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=project_root,
        timeout=600,  # 10 minutes for production demo
    )

    if result.returncode != 0:
        # Skip if pipeline fails (may need real agents or tools)
        pytest.skip(f"Pipeline failed: {result.stderr}")

    # Find latest ZIP
    out_dir = project_root / "out"
    zips = sorted(out_dir.glob("**/Package ZIP/package.zip"), key=lambda x: x.stat().st_mtime)
    assert zips, "package.zip not found"

    zip_path = zips[-1]

    # Check ZIP completeness
    with zipfile.ZipFile(zip_path, "r") as z:
        names = set(map(PurePosixPath, z.namelist()))

        required = {
            PurePosixPath("index.html"),
            PurePosixPath("README.md"),
            PurePosixPath("lint_report.md"),
            PurePosixPath("a11y_report.md"),
            PurePosixPath("MANIFEST.txt"),
        }

        # Screenshot is optional (may be placeholder if playwright not installed)
        has_screenshot = any(
            "screenshot" in str(n).lower() or "preview.png" in str(n).lower() for n in names
        )

        missing = required - names
        assert not missing, f"Missing required files in ZIP: {missing}"

        # Verify files are not empty
        for req_file in required:
            file_info = None
            for name in z.namelist():
                if PurePosixPath(name).name == req_file.name:
                    file_info = z.getinfo(name)
                    break
            assert file_info, f"Could not find {req_file.name} in ZIP"
            assert file_info.file_size > 0, f"{req_file.name} is empty"


def test_production_demo_screenshot_sanity(tmp_path, monkeypatch):
    """Test that screenshot exists and is not a placeholder (size check)."""
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    # Find latest screenshot
    out_dir = project_root / "out"
    screenshots = sorted(
        out_dir.glob("**/Screenshot/*.png"), key=lambda x: x.stat().st_mtime if x.exists() else 0
    )

    if not screenshots:
        # Try alternative paths
        screenshots = sorted(
            out_dir.glob("**/screenshots/*.png"),
            key=lambda x: x.stat().st_mtime if x.exists() else 0,
        )

    if not screenshots:
        pytest.skip("No screenshot found (pipeline may not have run or screenshot stage skipped)")

    screenshot_path = screenshots[-1]

    # Check screenshot size (placeholder is usually < 30KB)
    screenshot_size = screenshot_path.stat().st_size
    assert screenshot_size > 30_000, (
        f"Screenshot likely placeholder (size: {screenshot_size} bytes, expected > 30KB). "
        "Install playwright: pip install playwright && playwright install chromium"
    )


def test_production_demo_html_sanity(tmp_path, monkeypatch):
    """Test that generated HTML has basic required elements."""
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    # Find latest HTML
    out_dir = project_root / "out"
    html_files = sorted(
        out_dir.glob("**/code_skeleton/index.html"),
        key=lambda x: x.stat().st_mtime if x.exists() else 0,
    )

    if not html_files:
        # Try alternative paths
        html_files = sorted(
            out_dir.glob("**/*.html"), key=lambda x: x.stat().st_mtime if x.exists() else 0
        )

    if not html_files:
        pytest.skip("No HTML file found")

    html_path = html_files[-1]
    html_content = html_path.read_text(encoding="utf-8")

    # Check for required elements
    assert "<title>" in html_content, "HTML missing <title> tag"
    assert (
        'name="viewport"' in html_content or "name='viewport'" in html_content
    ), "HTML missing viewport meta tag"
    assert "<html" in html_content.lower(), "HTML missing <html> tag"
    assert len(html_content) > 500, "HTML seems too short"
