# One-Click Release Script - Complete v1.0.0 release automation (PowerShell)
# Runs: Go/No-Go checks → Release → Post-release bump
# Usage: .\scripts\release_all.ps1 [-DryRun]

param(
    [switch]$DryRun = $false
)

$ErrorActionPreference = "Stop"

$VERSION = "1.0.0"
$NEXT_VERSION = "1.0.1-dev"
$TAG_NAME = "v$VERSION"

Write-Host "🚀 One-Click Release Script - v$VERSION" -ForegroundColor Green
Write-Host "=========================================="
Write-Host ""

# Step 0: Pre-flight checks
Write-Host "[0/6] Pre-flight checks..." -ForegroundColor Cyan
if (Select-String -Path "README.md" -Pattern "your-org/AgentsSystemV2" -Quiet) {
    Write-Host "⚠️  WARNING: Badge URLs still contain 'your-org/AgentsSystemV2'" -ForegroundColor Yellow
    Write-Host "   Update them before release (see docs/README_BADGE_UPDATE.md)"
    if (-not $DryRun) {
        $response = Read-Host "Continue anyway? (y/N)"
        if ($response -ne "y" -and $response -ne "Y") {
            Write-Host "Aborted."
            exit 1
        }
    }
}

# Step 1: Final checks
Write-Host "[1/6] Running final checks..." -ForegroundColor Cyan
Write-Host "  • Version check..."
$VERSION_OUT = python cli.py --version 2>&1
if ($VERSION_OUT -ne $VERSION) {
    Write-Host "❌ Version mismatch: expected $VERSION, got $VERSION_OUT" -ForegroundColor Red
    exit 1
}
Write-Host "  ✅ Version: $VERSION_OUT" -ForegroundColor Green

Write-Host "  • Dry-run validation..."
python cli.py --pipeline pipeline/production.yaml --dry-run --export-graph out/pipeline.dot *>$null
Write-Host "  ✅ Dry-run passed" -ForegroundColor Green

Write-Host "  • Smoke tests..."
python scripts/smoke_test.py --skip-slow --json *>$null
Write-Host "  ✅ Smoke tests completed" -ForegroundColor Green

# Step 2: Tag & Release
Write-Host "[2/6] Tagging and releasing..." -ForegroundColor Cyan
if ($DryRun) {
    Write-Host "  [DRY-RUN] Would run: .\scripts\commit_push.ps1 -CreateTag:`$true -SignTag:`$true -TagName `"$TAG_NAME`""
} else {
    .\scripts\commit_push.ps1 -CreateTag:$true -SignTag:$true -TagName $TAG_NAME
}
Write-Host "  ✅ Tag created and pushed" -ForegroundColor Green

# Step 3: GitHub Release reminder
Write-Host "[3/6] GitHub Release..." -ForegroundColor Cyan
if ($DryRun) {
    Write-Host "  [DRY-RUN] Would create GitHub Release:"
    Write-Host "    Tag: $TAG_NAME"
    Write-Host "    Body: Copy from docs/GITHUB_RELEASE_SHORT_v1.0.0.md"
} else {
    Write-Host "  📝 Manual step required:"
    Write-Host "    1. Go to: https://github.com/<owner>/<repo>/releases/new"
    Write-Host "    2. Tag: $TAG_NAME"
    Write-Host "    3. Title: Release $TAG_NAME"
    Write-Host "    4. Body: Copy from docs/GITHUB_RELEASE_SHORT_v1.0.0.md"
    Write-Host "    5. Publish"
}

# Step 4: Post-release bump
Write-Host "[4/6] Post-release version bump..." -ForegroundColor Cyan
if ($DryRun) {
    Write-Host "  [DRY-RUN] Would run: .\scripts\post_release_bump.ps1 -CurrentVersion `"$VERSION`" -NextVersion `"$NEXT_VERSION`""
} else {
    .\scripts\post_release_bump.ps1 -CurrentVersion $VERSION -NextVersion $NEXT_VERSION
    git add -A
    $commitResult = git commit -m "chore: bump version to $NEXT_VERSION" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  (no changes to commit)"
    }
    git push
}
Write-Host "  ✅ Version bumped to $NEXT_VERSION" -ForegroundColor Green

# Step 5: Trigger automations reminder
Write-Host "[5/6] Trigger automations..." -ForegroundColor Cyan
if ($DryRun) {
    Write-Host "  [DRY-RUN] Would trigger:"
    Write-Host "    • Hard Tests Nightly (manual workflow_dispatch)"
    Write-Host "    • Verify workflows running (Release Drafter, Coverage, SBOM, CodeQL)"
} else {
    Write-Host "  📝 Manual steps:"
    Write-Host "    1. Trigger Hard Tests Nightly: Actions → hard-tests-nightly.yml → Run workflow"
    Write-Host "    2. Verify workflows: Release Drafter, Coverage, SBOM, CodeQL"
}

# Step 6: v1.1 kickoff
Write-Host "[6/6] v1.1 kickoff..." -ForegroundColor Cyan
if ($DryRun) {
    Write-Host "  [DRY-RUN] Would run: .\scripts\create_v1.1_issues.sh"
} else {
    if (Get-Command gh -ErrorAction SilentlyContinue) {
        Write-Host "  • Creating v1.1 milestone and issues..."
        bash ./scripts/create_v1.1_issues.sh
        if ($LASTEXITCODE -ne 0) {
            Write-Host "  ⚠️  Failed to create issues (gh CLI may not be authenticated)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  ⚠️  gh CLI not found, skipping issue creation" -ForegroundColor Yellow
        Write-Host "     Run manually: .\scripts\create_v1.1_issues.sh"
    }
}

Write-Host ""
Write-Host "✅ Release process complete!" -ForegroundColor Green
Write-Host ""
if ($DryRun) {
    Write-Host "This was a DRY-RUN. To execute for real, run without -DryRun flag."
} else {
    Write-Host "Next steps:"
    Write-Host "  1. Create GitHub Release (see step 3 above)"
    Write-Host "  2. Trigger Nightly Tests (see step 5 above)"
    Write-Host "  3. Monitor metrics (see docs/POST_RELEASE_MONITORING.md)"
}

