#!/bin/bash
# Go/No-Go checks for v1.0.0 release

set -e

echo "=== Go/No-Go Checks for v1.0.0 ==="
echo ""

# Check 1: Version
echo "[1/5] Checking version..."
VERSION=$(python cli.py --version 2>&1 | head -n 1)
if [[ "$VERSION" == "1.0.0" ]]; then
    echo "✅ Version check: PASSED ($VERSION)"
else
    echo "❌ Version check: FAILED (got: $VERSION, expected: 1.0.0)"
    exit 1
fi

# Check 2: Dry-run with graph export
echo "[2/5] Testing dry-run with graph export..."
python cli.py --pipeline pipeline/production.yaml --dry-run --export-graph out/pipeline_test.dot > /dev/null 2>&1
if [ -f "out/pipeline_test.dot" ]; then
    echo "✅ Graph export: PASSED"
    rm -f out/pipeline_test.dot
else
    echo "❌ Graph export: FAILED"
    exit 1
fi

# Check 3: Smoke tests
echo "[3/5] Running smoke tests..."
python scripts/smoke_test.py --skip-slow --json > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Smoke tests: PASSED"
else
    echo "❌ Smoke tests: FAILED"
    exit 1
fi

# Check 4: Clean command
echo "[4/5] Testing clean command..."
python cli.py clean --older-than 7d --dry-run --json > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Clean command: PASSED"
else
    echo "❌ Clean command: FAILED"
    exit 1
fi

# Check 5: Generator preview
echo "[5/5] Testing generator..."
python scripts/multiagent_new.py test-go-nogo --preset mvp-fast --out ./tmp_go_nogo > /dev/null 2>&1
if [ -f "tmp_go_nogo/pipeline/test-go-nogo.yaml" ]; then
    echo "✅ Generator: PASSED"
    rm -rf tmp_go_nogo
else
    echo "❌ Generator: FAILED"
    exit 1
fi

echo ""
echo "=== All checks passed! Ready for release. ==="

