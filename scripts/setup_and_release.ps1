# One-Liner: Setup Repo → Re-Validate → Release (PowerShell)
# Usage: .\scripts\setup_and_release.ps1 [-DryRun]

param(
    [switch]$DryRun = $false
)

$ErrorActionPreference = "Continue"

$Owner = "elirancv"
$Repo = "Multi-Agent-AI-Development-Framework-Extended-Genius-Edition"

Write-Host "🚀 Setup & Release - $Owner/$Repo" -ForegroundColor Green
Write-Host "=================================="
Write-Host ""

# Step 1: Git init & remote
Write-Host "[1/5] Setting up Git repository..." -ForegroundColor Cyan
git init -b main 2>$null
git remote remove origin 2>$null
git remote add origin "https://github.com/$Owner/$Repo.git" 2>$null
Write-Host "  ✅ Remote configured: $Owner/$Repo" -ForegroundColor Green

# Step 2: Create .env
Write-Host "[2/5] Creating .env file..." -ForegroundColor Cyan
"OWNER=$Owner`nREPO=$Repo" | Out-File -Encoding utf8 .env
Write-Host "  ✅ .env created" -ForegroundColor Green

# Step 3: Re-validate
Write-Host "[3/5] Running re-validation..." -ForegroundColor Cyan
.\scripts\revalidate.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  ⚠️  Re-validation had warnings (check out/validation/FINAL_VALIDATION.md)" -ForegroundColor Yellow
}

# Step 4: Commit changes
Write-Host "[4/5] Committing changes..." -ForegroundColor Cyan
git add -A
$hasChanges = (git diff --cached --quiet) -eq $false
if ($hasChanges) {
    git commit -m "chore: repo wiring + badges patch for $Owner/$Repo" 2>$null
    Write-Host "  ✅ Changes committed" -ForegroundColor Green
} else {
    Write-Host "  (no changes to commit)"
}

# Step 5: Release
Write-Host "[5/5] Release process..." -ForegroundColor Cyan
if ($DryRun) {
    Write-Host "  [DRY-RUN] Would run release..." -ForegroundColor Yellow
    .\scripts\release_all.ps1 -DryRun
} else {
    Write-Host "  ⚠️  Ready to release. Run manually:" -ForegroundColor Yellow
    Write-Host "     .\scripts\release_all.ps1"
    Write-Host ""
    Write-Host "  Or push first:"
    Write-Host "     git push -u origin main"
}

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Push to GitHub: git push -u origin main"
Write-Host "  2. Review: out/validation/FINAL_VALIDATION.md"
Write-Host "  3. Release: .\scripts\release_all.ps1"
