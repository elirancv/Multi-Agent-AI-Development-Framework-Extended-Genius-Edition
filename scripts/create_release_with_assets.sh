#!/usr/bin/env bash

# Create GitHub Release with production demo assets
# Usage: ./scripts/create_release_with_assets.sh <tag> [title] [notes_file]

set -euo pipefail

TAG="${1:-}"
TITLE="${2:-Release $TAG}"
NOTES_FILE="${3:-docs/GITHUB_RELEASE_SHORT_v1.0.0.md}"

if [ -z "$TAG" ]; then
    echo "Usage: $0 <tag> [title] [notes_file]"
    echo "Example: $0 v1.0.0 'Release v1.0.0' docs/GITHUB_RELEASE_SHORT_v1.0.0.md"
    exit 1
fi

echo "Creating release $TAG..."

# Find latest run artifacts
OUT_DIR="out"
LATEST_RUN=$(ls -t "$OUT_DIR" 2>/dev/null | grep -v "^\." | head -1 || echo "")

if [ -z "$LATEST_RUN" ]; then
    echo "⚠️  No runs found. Running production demo pipeline..."
    python cli.py \
        --pipeline pipeline/gallery/idea-to-zip/pipeline-production-demo.yaml \
        --mem 'product_idea="Coffee shop" brand="BlueBean" primary_color="#0ea5e9" tone="minimal" font_family="Inter"' \
        --save-artifacts \
        --output json || {
        echo "❌ Pipeline failed. Please run manually first."
        exit 1
    }
    LATEST_RUN=$(ls -t "$OUT_DIR" | grep -v "^\." | head -1)
fi

echo "Using run: $LATEST_RUN"

# Find artifacts
ZIP_PATH="$OUT_DIR/$LATEST_RUN/Package ZIP/package.zip"
SUMMARY_PATH="$OUT_DIR/$LATEST_RUN/SUMMARY.md"
SCREENSHOT_PATH="$OUT_DIR/$LATEST_RUN/Screenshot/preview.png"

# Try alternative screenshot path
if [ ! -f "$SCREENSHOT_PATH" ]; then
    SCREENSHOT_PATH="$OUT_DIR/$LATEST_RUN/screenshots/preview.png"
fi

# Prepare release notes
if [ -f "$NOTES_FILE" ]; then
    RELEASE_NOTES=$(cat "$NOTES_FILE")
else
    RELEASE_NOTES="Release $TAG - See repository for details."
fi

# Add artifacts info to notes
RELEASE_NOTES="$RELEASE_NOTES

## Demo Assets

This release includes a complete production demo:
- **ZIP Package**: Contains HTML, README, validation reports, and screenshot
- **Screenshot**: Preview of generated landing page
- **Summary**: Full execution report

Generated from: \`$LATEST_RUN\`
"

# Create release
echo "Creating GitHub release..."

# Build assets array
ASSETS_ARGS=()
[ -f "$ZIP_PATH" ] && ASSETS_ARGS+=("--attach" "$ZIP_PATH")
[ -f "$SUMMARY_PATH" ] && ASSETS_ARGS+=("--attach" "$SUMMARY_PATH")
[ -f "$SCREENSHOT_PATH" ] && ASSETS_ARGS+=("--attach" "$SCREENSHOT_PATH")

gh release create "$TAG" \
    --title "$TITLE" \
    --notes "$RELEASE_NOTES" \
    "${ASSETS_ARGS[@]}" \
    --target main || {
    echo "❌ Release creation failed. Check:"
    echo "  1. Tag doesn't already exist"
    echo "  2. GitHub CLI is authenticated (gh auth login)"
    echo "  3. You have write permissions"
    exit 1
}

echo "✅ Release $TAG created successfully!"
echo ""
echo "Attached assets:"
[ -f "$ZIP_PATH" ] && echo "  ✅ $ZIP_PATH"
[ -f "$SUMMARY_PATH" ] && echo "  ✅ $SUMMARY_PATH"
[ -f "$SCREENSHOT_PATH" ] && echo "  ✅ $SCREENSHOT_PATH"
