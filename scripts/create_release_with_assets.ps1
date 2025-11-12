# Create GitHub Release with production demo assets (PowerShell)
# Usage: .\scripts\create_release_with_assets.ps1 -Tag "v1.0.0" [-Title "Release v1.0.0"] [-NotesFile "docs/GITHUB_RELEASE_SHORT_v1.0.0.md"]

param(
    [Parameter(Mandatory=$true)]
    [string]$Tag,

    [string]$Title = "Release $Tag",

    [string]$NotesFile = "docs/GITHUB_RELEASE_SHORT_v1.0.0.md"
)

$ErrorActionPreference = "Stop"

Write-Host "Creating release $Tag..." -ForegroundColor Cyan

# Find latest run artifacts
$OutDir = "out"
$LatestRun = Get-ChildItem $OutDir -Directory | Where-Object { $_.Name -notmatch "^\." } | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if (-not $LatestRun) {
    Write-Host "⚠️  No runs found. Running production demo pipeline..." -ForegroundColor Yellow
    python cli.py `
        --pipeline pipeline/gallery/idea-to-zip/pipeline-production-demo.yaml `
        --mem 'product_idea="Coffee shop" brand="BlueBean" primary_color="#0ea5e9" tone="minimal" font_family="Inter"' `
        --save-artifacts `
        --output json

    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Pipeline failed. Please run manually first." -ForegroundColor Red
        exit 1
    }

    $LatestRun = Get-ChildItem $OutDir -Directory | Where-Object { $_.Name -notmatch "^\." } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
}

Write-Host "Using run: $($LatestRun.Name)" -ForegroundColor Green

# Find artifacts
$ZipPath = Join-Path $LatestRun.FullName "Package ZIP" "package.zip"
$SummaryPath = Join-Path $LatestRun.FullName "SUMMARY.md"
$ScreenshotPath = Join-Path $LatestRun.FullName "Screenshot" "preview.png"

# Try alternative screenshot path
if (-not (Test-Path $ScreenshotPath)) {
    $ScreenshotPath = Join-Path $LatestRun.FullName "screenshots" "preview.png"
}

# Prepare release notes
if (Test-Path $NotesFile) {
    $ReleaseNotes = Get-Content $NotesFile -Raw
} else {
    $ReleaseNotes = "Release $Tag - See repository for details."
}

# Add artifacts info
$ReleaseNotes += "`n`n## Demo Assets`n`nThis release includes a complete production demo:`n- **ZIP Package**: Contains HTML, README, validation reports, and screenshot`n- **Screenshot**: Preview of generated landing page`n- **Summary**: Full execution report`n`nGenerated from: ``$($LatestRun.Name)``"

# Build gh release create command
$Assets = @()
if (Test-Path $ZipPath) { $Assets += $ZipPath }
if (Test-Path $SummaryPath) { $Assets += $SummaryPath }
if (Test-Path $ScreenshotPath) { $Assets += $ScreenshotPath }

Write-Host "Creating GitHub release..." -ForegroundColor Cyan

# Check gh version - newer versions use --attach, older use positional args
$ghVersion = gh --version 2>&1 | Select-Object -First 1
$useAttach = $ghVersion -match "gh version [2-9]"

if ($useAttach) {
    # Newer gh CLI - use --attach flag
    $AssetsArgs = $Assets | ForEach-Object { "--attach", $_ }
    gh release create $Tag `
        --title $Title `
        --notes $ReleaseNotes `
        $AssetsArgs `
        --target main
} else {
    # Older gh CLI - use positional arguments (files after tag)
    $ReleaseArgs = @($Tag, "--title", $Title, "--notes", $ReleaseNotes, "--target", "main")
    $AllArgs = $ReleaseArgs + $Assets
    & gh release create $AllArgs
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Release creation failed. Check:" -ForegroundColor Red
    Write-Host "  1. Tag doesn't already exist" -ForegroundColor Yellow
    Write-Host "  2. GitHub CLI is authenticated (gh auth login)" -ForegroundColor Yellow
    Write-Host "  3. You have write permissions" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Release $Tag created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Attached assets:" -ForegroundColor Cyan
if (Test-Path $ZipPath) { Write-Host "  ✅ $ZipPath" -ForegroundColor Green }
if (Test-Path $SummaryPath) { Write-Host "  ✅ $SummaryPath" -ForegroundColor Green }
if (Test-Path $ScreenshotPath) { Write-Host "  ✅ $ScreenshotPath" -ForegroundColor Green }
