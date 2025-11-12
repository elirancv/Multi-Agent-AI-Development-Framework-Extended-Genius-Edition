# Release Execution Pack - Complete v1.0.0 release workflow (PowerShell)
# Usage: .\scripts\release_execute.ps1

$ErrorActionPreference = "Stop"

Write-Host "🚀 Starting v1.0.0 Release Process..." -ForegroundColor Green
Write-Host ""

# Sanity checks
Write-Host "[1/4] Running sanity checks..." -ForegroundColor Cyan
python cli.py --version
python cli.py --pipeline pipeline/production.yaml --dry-run --export-graph out/pipeline.dot
python scripts/smoke_test.py --skip-slow --json
coverage run -m pytest; coverage xml -o coverage.xml; coverage report

Write-Host ""
Write-Host "[2/4] Tagging and releasing..." -ForegroundColor Cyan
.\scripts\commit_push.ps1 -CreateTag:$true -SignTag:$true -TagName "v1.0.0"

Write-Host ""
Write-Host "[3/4] Post-release version bump..." -ForegroundColor Cyan
.\scripts\post_release_bump.ps1 -CurrentVersion "1.0.0" -NextVersion "1.0.1-dev"

Write-Host ""
Write-Host "[4/4] Committing version bump..." -ForegroundColor Cyan
git add -A
git commit -m "chore: bump version to 1.0.1-dev"
git push

Write-Host ""
Write-Host "✅ Release process complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Create GitHub Release: https://github.com/<owner>/<repo>/releases/new"
Write-Host "  2. Copy body from: docs/GITHUB_RELEASE_SHORT_v1.0.0.md"
Write-Host "  3. Create v1.1 milestone and issues (see scripts/create_v1.1_issues.sh)"
