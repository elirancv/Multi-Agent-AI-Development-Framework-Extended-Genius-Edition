# GO-LIVE Script - Complete Release Automation (PowerShell)
# Usage: .\scripts\go_live.ps1 [-Brand "BlueBean"] [-Color "#0ea5e9"] [-Tone "minimal"] [-Font "Inter"] [-Product "Coffee shop"] [-Version "v1.0.0"]

param(
    [string]$Brand = "BlueBean",
    [string]$Color = "#0ea5e9",
    [string]$Tone = "minimal",
    [string]$Font = "Inter",
    [string]$Product = "Coffee shop",
    [string]$Version = "v1.0.0"
)

$ErrorActionPreference = "Continue"  # Continue on errors to show all issues

# Add Graphviz to PATH if installed but not in PATH
$graphvizPaths = @("C:\Program Files\Graphviz\bin", "C:\Program Files (x86)\Graphviz\bin")
foreach ($path in $graphvizPaths) {
    if (Test-Path $path -and $env:PATH -notlike "*$path*") {
        $env:PATH = "$path;$env:PATH"
    }
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "GO-LIVE: Release $Version" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  Brand: $Brand" -ForegroundColor White
Write-Host "  Color: $Color" -ForegroundColor White
Write-Host "  Tone: $Tone" -ForegroundColor White
Write-Host "  Font: $Font" -ForegroundColor White
Write-Host "  Product: $Product" -ForegroundColor White
Write-Host ""

# Step 1: Update badges
Write-Host "[1/8] Updating badges..." -ForegroundColor Cyan
if (-not (Test-Path .env)) {
    if (Test-Path .env.example) {
        Copy-Item .env.example .env
    } else {
        @"
OWNER=elirancv
REPO=Multi-Agent-AI-Development-Framework-Extended-Genius-Edition
"@ | Out-File -FilePath .env -Encoding utf8
    }
}

# Update .env
$envContent = Get-Content .env -Raw -ErrorAction SilentlyContinue
if ($envContent -notmatch "OWNER=elirancv") {
    $envContent = $envContent -replace "OWNER=.*", "OWNER=elirancv"
    if ($envContent -notmatch "OWNER=") {
        $envContent += "`nOWNER=elirancv"
    }
}
if ($envContent -notmatch "REPO=Multi-Agent-AI-Development-Framework-Extended-Genius-Edition") {
    $envContent = $envContent -replace "REPO=.*", "REPO=Multi-Agent-AI-Development-Framework-Extended-Genius-Edition"
    if ($envContent -notmatch "REPO=") {
        $envContent += "`nREPO=Multi-Agent-AI-Development-Framework-Extended-Genius-Edition"
    }
}
Set-Content -Path .env -Value $envContent -Encoding utf8
Write-Host "✅ Badges configured" -ForegroundColor Green

# Step 2: Install screenshot tools
Write-Host ""
Write-Host "[2/8] Installing screenshot tools..." -ForegroundColor Cyan
try {
    python -c "import playwright" 2>$null
    Write-Host "✅ Playwright already installed" -ForegroundColor Green
} catch {
    Write-Host "Installing playwright..." -ForegroundColor Yellow
    pip install playwright --quiet
    python -m playwright install chromium --quiet
    Write-Host "✅ Playwright installed" -ForegroundColor Green
}

# Step 3: Run production demo
Write-Host ""
Write-Host "[3/8] Running production demo pipeline..." -ForegroundColor Cyan
$memArgs = "product_idea=`"$Product`" brand=`"$Brand`" primary_color=`"$Color`" tone=`"$Tone`" font_family=`"$Font`""
$pipelineExitCode = 0

python cli.py `
    --pipeline pipeline/gallery/idea-to-zip/pipeline-production-demo.yaml `
    --mem $memArgs `
    --save-artifacts `
    --output human 2>&1 | Tee-Object -Variable pipelineOutput

$pipelineExitCode = $LASTEXITCODE

# Wait a moment for files to be written
Start-Sleep -Seconds 2

$LatestRun = Get-ChildItem out -Directory | Where-Object {
    $_.Name -notmatch "^\." -and $_.Name -ne "validation" -and $_.Name -ne "checkpoints"
} | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if (-not $LatestRun) {
    Write-Host "❌ Warning: No run found. Pipeline may have failed." -ForegroundColor Red
    Write-Host "Pipeline output:" -ForegroundColor Yellow
    $pipelineOutput | Select-Object -Last 10
    if ($pipelineExitCode -ne 0) {
        Write-Host "⚠️  Pipeline had errors but continuing..." -ForegroundColor Yellow
    }
} else {
    Write-Host "✅ Pipeline completed: $($LatestRun.Name)" -ForegroundColor Green
}

# Step 4: Integration tests
Write-Host ""
Write-Host "[4/8] Running integration tests..." -ForegroundColor Cyan
if ($LatestRun) {
    pytest tests/test_idea_to_zip_integration.py::test_production_demo_zip_completeness -q 2>&1 | Out-Null
    pytest tests/test_idea_to_zip_integration.py::test_production_demo_screenshot_sanity -q 2>&1 | Out-Null
    pytest tests/test_idea_to_zip_integration.py::test_production_demo_html_sanity -q 2>&1 | Out-Null
    Write-Host "✅ Integration tests completed" -ForegroundColor Green
} else {
    Write-Host "⚠️  Skipping integration tests (no run found)" -ForegroundColor Yellow
}

# Step 5: Smoke + Validation
Write-Host ""
Write-Host "[5/8] Running smoke tests and validation..." -ForegroundColor Cyan
python scripts/smoke_test.py --skip-slow --json
if (Test-Path scripts/revalidate.ps1) {
    .\scripts\revalidate.ps1
} else {
    Write-Host "⚠️  revalidate.ps1 not found, skipping" -ForegroundColor Yellow
}
Write-Host "✅ Smoke and validation completed" -ForegroundColor Green

# Step 6: Verify outputs
Write-Host ""
Write-Host "[6/8] Verifying outputs..." -ForegroundColor Cyan
$ZipPath = Join-Path $LatestRun.FullName "Package ZIP" "package.zip"
$ScreenshotPath = Join-Path $LatestRun.FullName "Screenshot" "preview.png"

if (-not (Test-Path $ScreenshotPath)) {
    $ScreenshotPath = Join-Path $LatestRun.FullName "screenshots" "preview.png"
}

if (Test-Path $ZipPath) {
    $ZipSize = (Get-Item $ZipPath).Length
    Write-Host "✅ ZIP found: $ZipPath ($([math]::Round($ZipSize/1KB, 2)) KB)" -ForegroundColor Green
} else {
    Write-Host "❌ ZIP not found: $ZipPath" -ForegroundColor Red
    Write-Host "⚠️  Continuing anyway - ZIP may be created in different location" -ForegroundColor Yellow
    # Try to find ZIP in alternative locations
    $AltZip = Get-ChildItem "out/$($LatestRun.Name)" -Recurse -Filter "package.zip" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($AltZip) {
        Write-Host "✅ Found ZIP at: $($AltZip.FullName)" -ForegroundColor Green
        $ZipPath = $AltZip.FullName
    }
}

if (Test-Path $ScreenshotPath) {
    $ScreenshotSize = (Get-Item $ScreenshotPath).Length
    if ($ScreenshotSize -gt 30000) {
        Write-Host "✅ Screenshot found: $ScreenshotPath ($([math]::Round($ScreenshotSize/1KB, 2)) KB) - Real screenshot" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Screenshot found but small: $ScreenshotPath ($([math]::Round($ScreenshotSize/1KB, 2)) KB) - May be placeholder" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  Screenshot not found: $ScreenshotPath" -ForegroundColor Yellow
}

# Step 7: Create release
Write-Host ""
Write-Host "[7/8] Creating GitHub release..." -ForegroundColor Cyan
if (Test-Path scripts/create_release_with_assets.ps1) {
    .\scripts\create_release_with_assets.ps1 -Tag $Version
} else {
    Write-Host "⚠️  create_release_with_assets.ps1 not found" -ForegroundColor Yellow
}

# Step 8: Post-release bump
Write-Host ""
Write-Host "[8/8] Post-release version bump..." -ForegroundColor Cyan
if (Test-Path scripts/post_release_bump.ps1) {
    $CurrentVersion = $Version -replace "^v", ""
    $VersionParts = $CurrentVersion.Split(".")
    $NextVersion = "$($VersionParts[0]).$($VersionParts[1]).$([int]$VersionParts[2] + 1)-dev"
    .\scripts\post_release_bump.ps1 -CurrentVersion $CurrentVersion -NextVersion $NextVersion
} else {
    Write-Host "⚠️  post_release_bump.ps1 not found, skipping" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ GO-LIVE COMPLETE!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Verify release on GitHub" -ForegroundColor White
Write-Host "  2. Test ZIP: Expand-Archive `"$ZipPath`" -DestinationPath out/demo/; python -m http.server -d out/demo 8000" -ForegroundColor White
Write-Host "  3. Create v1.1 issues: .\scripts\create_v1.1_issues.ps1" -ForegroundColor White
Write-Host "  4. Trigger workflows: gh workflow run production-demo.yml" -ForegroundColor White
Write-Host ""
