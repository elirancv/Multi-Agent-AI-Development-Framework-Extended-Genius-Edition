# Re-Validation Script - Turn YELLOW → GREEN (PowerShell)
# Installs optional tools, fixes badges, re-runs all checks

$ErrorActionPreference = "Continue"

# Add Graphviz to PATH if installed but not in PATH
$graphvizPaths = @("C:\Program Files\Graphviz\bin", "C:\Program Files (x86)\Graphviz\bin")
foreach ($path in $graphvizPaths) {
    if (Test-Path $path -and $env:PATH -notlike "*$path*") {
        $env:PATH = "$path;$env:PATH"
    }
}

# Load owner/repo from .env if exists
$Owner = ""
$Repo = ""

if (Test-Path .env) {
    Get-Content .env | ForEach-Object {
        if ($_ -match "^OWNER=(.+)$") { $Owner = $matches[1] }
        if ($_ -match "^REPO=(.+)$") { $Repo = $matches[1] }
    }
}

# Override with environment variables if set
if ($env:OWNER) { $Owner = $env:OWNER }
if ($env:REPO) { $Repo = $env:REPO }

Write-Host "== STEP 1: Python deps ==" -ForegroundColor Cyan
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pdoc pre-commit graphviz coverage

Write-Host ""
Write-Host "== STEP 2: System graphviz (optional) ==" -ForegroundColor Cyan
# Prefer choco or scoop if available
if (Get-Command choco -ErrorAction SilentlyContinue) {
    Write-Host "Installing graphviz via choco..."
    choco install graphviz -y
} elseif (Get-Command scoop -ErrorAction SilentlyContinue) {
    Write-Host "Installing graphviz via scoop..."
    scoop install graphviz
} else {
    Write-Host "  (skipped - no package manager found, using Python package)"
}

Write-Host ""
Write-Host "== STEP 3: Pre-commit (optional) ==" -ForegroundColor Cyan
if (Get-Command pre-commit -ErrorAction SilentlyContinue) {
    pre-commit install
    pre-commit run --all-files
} else {
    Write-Host "  (skipped - pre-commit not installed)"
}

Write-Host ""
Write-Host "== STEP 4: Patch README badges (if placeholders exist) ==" -ForegroundColor Cyan
if ($Owner -and $Repo) {
    $content = Get-Content README.md -Raw
    if ($content -match "your-org/AgentsSystemV2") {
        Write-Host "Patching badges: your-org/AgentsSystemV2 → $Owner/$Repo"
        $content = $content -replace "your-org/AgentsSystemV2", "$Owner/$Repo"
        Set-Content README.md $content -Encoding UTF8 -NoNewline
        Write-Host "  ✅ Badges patched"
    } else {
        Write-Host "  (no placeholders found)"
    }
} else {
    Write-Host "  ⚠️  OWNER/REPO not set - skipping badge patch"
    Write-Host "     Set OWNER and REPO in .env or environment variables"
}

Write-Host ""
Write-Host "== STEP 5: Quick sanity ==" -ForegroundColor Cyan
$versionOut = python cli.py --version 2>&1
Write-Host "Version: $versionOut"
if ($versionOut -ne "1.0.0") {
    Write-Host "  ⚠️  Version mismatch"
}

python cli.py --pipeline pipeline/production.yaml --dry-run --export-graph out/pipeline.dot
if (Test-Path out/pipeline.dot) {
    $size = (Get-Item out/pipeline.dot).Length
    Write-Host "  ✅ Graph exported: out/pipeline.dot ($size bytes)"
} else {
    Write-Host "  ⚠️  Graph file not created"
}

Write-Host ""
Write-Host "== STEP 6: Smoke (fast) ==" -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path out/validation | Out-Null
python scripts/smoke_test.py --skip-slow --json | Tee-Object -FilePath out/validation/smoke_output.txt

Write-Host ""
Write-Host "== STEP 7: Full validation report (re-run) ==" -ForegroundColor Cyan
python scripts/doctor.py --verbose | Tee-Object -FilePath out/validation/doctor_output.txt

if (Get-Command coverage -ErrorAction SilentlyContinue) {
python -m coverage run -m pytest -q 2>&1 | Out-Null
python -m coverage xml -o coverage.xml 2>&1 | Out-Null
python -m coverage report 2>&1 | Out-Null | Tee-Object -FilePath out/validation/coverage_report.txt
} else {
    Write-Host "  ⚠️  coverage not available"
}

Write-Host ""
Write-Host "== STEP 7b: All pipelines validation (non-blocking) ==" -ForegroundColor Cyan
python scripts/smoke_test.py --test all-pipelines --verbose 2>&1 | Tee-Object -FilePath out/validation/all_pipelines.txt

Write-Host ""
Write-Host "== STEP 8: Release dry-run ==" -ForegroundColor Cyan
.\scripts\release_all.ps1 -DryRun | Tee-Object -FilePath out/validation/release_dry_run.txt

Write-Host ""
Write-Host "== STEP 9: Final validation summary ==" -ForegroundColor Cyan
python scripts/smoke_test.py --skip-slow --json | Out-File -FilePath out/validation/SMOKE_FAST.json -Encoding utf8

python scripts/revalidate_final.py

$exitCode = $LASTEXITCODE
Write-Host ""
if ($exitCode -eq 0) {
    Write-Host "== DONE. Status: GREEN ==" -ForegroundColor Green
    Write-Host ""
    Write-Host "PowerShell ship (tag & push):"
    Write-Host '  .\scripts\commit_push.ps1 -CreateTag:$true -SignTag:$true -TagName "v1.0.0"'
} else {
    Write-Host "== DONE. Status: YELLOW/RED ==" -ForegroundColor Yellow
    Write-Host "Review warnings in out/validation/FINAL_VALIDATION.md"
}

exit $exitCode
