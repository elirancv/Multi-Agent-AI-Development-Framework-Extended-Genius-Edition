#!/usr/bin/env bash

# Quick check script for production demo outputs
# Usage: ./scripts/quick_check_production_demo.sh

set -euo pipefail

OUT_DIR="out"
REQUIRED_FILES=(
    "index.html"
    "README.md"
    "lint_report.md"
    "a11y_report.md"
    "MANIFEST.txt"
)

echo "Checking production demo outputs..."

# Find latest run
LATEST_RUN=$(ls -t "$OUT_DIR" 2>/dev/null | grep -v "^\." | head -1 || echo "")

if [ -z "$LATEST_RUN" ]; then
    echo "❌ No runs found in $OUT_DIR"
    exit 1
fi

echo "Latest run: $LATEST_RUN"

# Check ZIP
ZIP_PATH="$OUT_DIR/$LATEST_RUN/Package ZIP/package.zip"
if [ ! -f "$ZIP_PATH" ]; then
    echo "❌ ZIP not found: $ZIP_PATH"
    exit 1
fi

echo "✅ ZIP found: $ZIP_PATH"

# Check ZIP contents
echo ""
echo "Checking ZIP contents..."
python3 - <<'PY'
import zipfile
from pathlib import PurePosixPath
import sys

zip_path = "$ZIP_PATH"
required = {
    PurePosixPath("index.html"),
    PurePosixPath("README.md"),
    PurePosixPath("lint_report.md"),
    PurePosixPath("a11y_report.md"),
    PurePosixPath("MANIFEST.txt"),
}

with zipfile.ZipFile(zip_path, "r") as z:
    names = set(map(PurePosixPath, z.namelist()))
    missing = required - names

    if missing:
        print(f"❌ Missing files: {missing}")
        sys.exit(1)

    print("✅ All required files present in ZIP")

    # Check file sizes
    for req_file in required:
        for name in z.namelist():
            if PurePosixPath(name).name == req_file.name:
                info = z.getinfo(name)
                if info.file_size == 0:
                    print(f"⚠️  {req_file.name} is empty")
                else:
                    print(f"  ✓ {req_file.name} ({info.file_size} bytes)")
                break
PY

# Check screenshot
SCREENSHOT_PATH="$OUT_DIR/$LATEST_RUN/Screenshot/preview.png"
if [ ! -f "$SCREENSHOT_PATH" ]; then
    SCREENSHOT_PATH="$OUT_DIR/$LATEST_RUN/screenshots/preview.png"
fi

if [ -f "$SCREENSHOT_PATH" ]; then
    SCREENSHOT_SIZE=$(stat -f%z "$SCREENSHOT_PATH" 2>/dev/null || stat -c%s "$SCREENSHOT_PATH" 2>/dev/null || echo "0")
    if [ "$SCREENSHOT_SIZE" -gt 30000 ]; then
        echo "✅ Screenshot OK: $SCREENSHOT_PATH ($SCREENSHOT_SIZE bytes)"
    else
        echo "⚠️  Screenshot likely placeholder: $SCREENSHOT_PATH ($SCREENSHOT_SIZE bytes)"
        echo "   Install playwright: pip install playwright && playwright install chromium"
    fi
else
    echo "⚠️  Screenshot not found"
fi

# Check HTML sanity
HTML_PATH="$OUT_DIR/$LATEST_RUN/code_skeleton/index.html"
if [ -f "$HTML_PATH" ]; then
    if grep -q "<title>" "$HTML_PATH" && grep -q "viewport" "$HTML_PATH"; then
        echo "✅ HTML sanity check passed"
    else
        echo "⚠️  HTML missing required elements (title/viewport)"
    fi
fi

echo ""
echo "✅ Production demo check complete!"
