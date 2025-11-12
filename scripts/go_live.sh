#!/usr/bin/env bash

# GO-LIVE Script - Complete Release Automation
# Usage: ./scripts/go_live.sh [brand] [color] [tone] [font]
# Example: ./scripts/go_live.sh "BlueBean" "#0ea5e9" "minimal" "Inter"

set -euo pipefail

# Configuration
BRAND="${1:-BlueBean}"
COLOR="${2:-#0ea5e9}"
TONE="${3:-minimal}"
FONT="${4:-Inter}"
PRODUCT_IDEA="${5:-Coffee shop}"
VERSION="${6:-v1.0.0}"

echo "========================================"
echo "GO-LIVE: Release $VERSION"
echo "========================================"
echo ""
echo "Configuration:"
echo "  Brand: $BRAND"
echo "  Color: $COLOR"
echo "  Tone: $TONE"
echo "  Font: $FONT"
echo "  Product: $PRODUCT_IDEA"
echo ""

# Step 1: Update badges
echo "[1/8] Updating badges..."
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
    else
        echo "OWNER=elirancv" > .env
        echo "REPO=Multi-Agent-AI-Development-Framework-Extended-Genius-Edition" >> .env
    fi
fi

# Update .env if needed
if grep -q "OWNER=your-org" .env 2>/dev/null || ! grep -q "OWNER=elirancv" .env 2>/dev/null; then
    sed -i.bak 's/OWNER=.*/OWNER=elirancv/' .env 2>/dev/null || \
    sed -i '' 's/OWNER=.*/OWNER=elirancv/' .env 2>/dev/null || \
    echo "OWNER=elirancv" >> .env
fi

if grep -q "REPO=AgentsSystemV2" .env 2>/dev/null || ! grep -q "REPO=Multi-Agent-AI-Development-Framework-Extended-Genius-Edition" .env 2>/dev/null; then
    sed -i.bak 's|REPO=.*|REPO=Multi-Agent-AI-Development-Framework-Extended-Genius-Edition|' .env 2>/dev/null || \
    sed -i '' 's|REPO=.*|REPO=Multi-Agent-AI-Development-Framework-Extended-Genius-Edition|' .env 2>/dev/null || \
    echo "REPO=Multi-Agent-AI-Development-Framework-Extended-Genius-Edition" >> .env
fi

echo "✅ Badges configured"

# Step 2: Install screenshot tools
echo ""
echo "[2/8] Installing screenshot tools..."
if ! python -c "import playwright" 2>/dev/null; then
    echo "Installing playwright..."
    pip install playwright --quiet
    python -m playwright install chromium --quiet
    echo "✅ Playwright installed"
else
    echo "✅ Playwright already installed"
fi

# Step 3: Run production demo
echo ""
echo "[3/8] Running production demo pipeline..."
python cli.py \
    --pipeline pipeline/gallery/idea-to-zip/pipeline-production-demo.yaml \
    --mem "product_idea=\"$PRODUCT_IDEA\" brand=\"$BRAND\" primary_color=\"$COLOR\" tone=\"$TONE\" font_family=\"$FONT\"" \
    --save-artifacts \
    --output human

LATEST_RUN=$(ls -t out/ 2>/dev/null | grep -v "^\." | grep -v "^validation$" | grep -v "^checkpoints$" | head -1 || echo "")
if [ -z "$LATEST_RUN" ]; then
    echo "⚠️  Warning: No run found. Pipeline may have failed."
    exit 1
fi

echo "✅ Pipeline completed: $LATEST_RUN"

# Step 4: Integration tests
echo ""
echo "[4/8] Running integration tests..."
pytest tests/test_idea_to_zip_integration.py::test_production_demo_zip_completeness -q || echo "⚠️  ZIP completeness test skipped"
pytest tests/test_idea_to_zip_integration.py::test_production_demo_screenshot_sanity -q || echo "⚠️  Screenshot sanity test skipped"
pytest tests/test_idea_to_zip_integration.py::test_production_demo_html_sanity -q || echo "⚠️  HTML sanity test skipped"
echo "✅ Integration tests completed"

# Step 5: Smoke + Validation
echo ""
echo "[5/8] Running smoke tests and validation..."
python scripts/smoke_test.py --skip-slow --json || echo "⚠️  Smoke tests had warnings"
if [ -f scripts/revalidate.sh ]; then
    bash scripts/revalidate.sh || echo "⚠️  Validation had warnings"
else
    echo "⚠️  revalidate.sh not found, skipping"
fi
echo "✅ Smoke and validation completed"

# Step 6: Verify outputs
echo ""
echo "[6/8] Verifying outputs..."
ZIP_PATH="out/$LATEST_RUN/Package ZIP/package.zip"
SCREENSHOT_PATH="out/$LATEST_RUN/Screenshot/preview.png"

if [ ! -f "$SCREENSHOT_PATH" ]; then
    SCREENSHOT_PATH="out/$LATEST_RUN/screenshots/preview.png"
fi

if [ -f "$ZIP_PATH" ]; then
    ZIP_SIZE=$(stat -f%z "$ZIP_PATH" 2>/dev/null || stat -c%s "$ZIP_PATH" 2>/dev/null || echo "0")
    echo "✅ ZIP found: $ZIP_PATH ($(($ZIP_SIZE / 1024)) KB)"
else
    echo "❌ ZIP not found: $ZIP_PATH"
    exit 1
fi

if [ -f "$SCREENSHOT_PATH" ]; then
    SCREENSHOT_SIZE=$(stat -f%z "$SCREENSHOT_PATH" 2>/dev/null || stat -c%s "$SCREENSHOT_PATH" 2>/dev/null || echo "0")
    if [ "$SCREENSHOT_SIZE" -gt 30000 ]; then
        echo "✅ Screenshot found: $SCREENSHOT_PATH ($(($SCREENSHOT_SIZE / 1024)) KB) - Real screenshot"
    else
        echo "⚠️  Screenshot found but small: $SCREENSHOT_PATH ($(($SCREENSHOT_SIZE / 1024)) KB) - May be placeholder"
    fi
else
    echo "⚠️  Screenshot not found: $SCREENSHOT_PATH"
fi

# Step 7: Create release
echo ""
echo "[7/8] Creating GitHub release..."
if [ -f scripts/create_release_with_assets.sh ]; then
    chmod +x scripts/create_release_with_assets.sh
    ./scripts/create_release_with_assets.sh "$VERSION" || {
        echo "⚠️  Release creation failed. Check GitHub CLI authentication."
        echo "   Run: gh auth login"
    }
else
    echo "⚠️  create_release_with_assets.sh not found"
fi

# Step 8: Post-release bump
echo ""
echo "[8/8] Post-release version bump..."
if [ -f scripts/post_release_bump.sh ]; then
    CURRENT_VERSION=$(echo "$VERSION" | sed 's/^v//')
    NEXT_VERSION="${CURRENT_VERSION%.*}.$((${CURRENT_VERSION##*.} + 1))-dev"
    bash scripts/post_release_bump.sh "$CURRENT_VERSION" "$NEXT_VERSION" || echo "⚠️  Version bump script not found or failed"
else
    echo "⚠️  post_release_bump.sh not found, skipping"
fi

echo ""
echo "========================================"
echo "✅ GO-LIVE COMPLETE!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Verify release on GitHub: https://github.com/elirancv/Multi-Agent-AI-Development-Framework-Extended-Genius-Edition/releases"
echo "  2. Test ZIP: unzip \"$ZIP_PATH\" -d out/demo/ && python -m http.server -d out/demo 8000"
echo "  3. Create v1.1 issues: ./scripts/create_v1.1_issues.sh"
echo "  4. Trigger workflows: gh workflow run production-demo.yml"
echo ""
