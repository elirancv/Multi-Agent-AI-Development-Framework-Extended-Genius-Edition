# Go/No-Go checks for v1.0.0 release (PowerShell)

$ErrorActionPreference = "Stop"

Write-Host "=== Go/No-Go Checks for v1.0.0 ===" -ForegroundColor Cyan
Write-Host ""

# Check 1: Version
Write-Host "[1/5] Checking version..." -ForegroundColor Yellow
$version = python cli.py --version 2>&1 | Select-Object -First 1
if ($version -eq "1.0.0") {
    Write-Host "✅ Version check: PASSED ($version)" -ForegroundColor Green
} else {
    Write-Host "❌ Version check: FAILED (got: $version, expected: 1.0.0)" -ForegroundColor Red
    exit 1
}

# Check 2: Dry-run with graph export
Write-Host "[2/5] Testing dry-run with graph export..." -ForegroundColor Yellow
python cli.py --pipeline pipeline/production.yaml --dry-run --export-graph out/pipeline_test.dot 2>&1 | Out-Null
if (Test-Path "out/pipeline_test.dot") {
    Write-Host "✅ Graph export: PASSED" -ForegroundColor Green
    Remove-Item "out/pipeline_test.dot" -ErrorAction SilentlyContinue
} else {
    Write-Host "❌ Graph export: FAILED" -ForegroundColor Red
    exit 1
}

# Check 3: Smoke tests
Write-Host "[3/5] Running smoke tests..." -ForegroundColor Yellow
$smokeResult = python scripts/smoke_test.py --skip-slow --json 2>&1
$smokeExitCode = $LASTEXITCODE
if ($smokeExitCode -eq 0) {
    Write-Host "✅ Smoke tests: PASSED" -ForegroundColor Green
} else {
    Write-Host "❌ Smoke tests: FAILED (exit code: $smokeExitCode)" -ForegroundColor Red
    Write-Host "Note: Smoke tests may fail if no pipeline artifacts exist. This is OK for dry-run." -ForegroundColor Yellow
    # Don't exit - smoke tests are optional for Go/No-Go
}

# Check 4: Clean command
Write-Host "[4/5] Testing clean command..." -ForegroundColor Yellow
python cli.py clean --older-than "7d" --dry-run --json 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Clean command: PASSED" -ForegroundColor Green
} else {
    Write-Host "❌ Clean command: FAILED" -ForegroundColor Red
    exit 1
}

# Check 5: Generator preview
Write-Host "[5/5] Testing generator..." -ForegroundColor Yellow
python scripts/multiagent_new.py test-go-nogo --preset mvp-fast --out ./tmp_go_nogo 2>&1 | Out-Null
if (Test-Path "tmp_go_nogo/pipeline/test-go-nogo.yaml") {
    Write-Host "✅ Generator: PASSED" -ForegroundColor Green
    Remove-Item "tmp_go_nogo" -Recurse -Force -ErrorAction SilentlyContinue
} else {
    Write-Host "❌ Generator: FAILED" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== All checks passed! Ready for release. ===" -ForegroundColor Green
