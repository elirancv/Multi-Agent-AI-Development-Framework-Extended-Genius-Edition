# Quick Setup - One Command (PowerShell)

$Owner = "elirancv"
$Repo = "Multi-Agent-AI-Development-Framework-Extended-Genius-Edition"

Write-Host "🚀 Quick Setup - $Owner/$Repo" -ForegroundColor Green

# Git setup
git init -b main 2>$null
git remote remove origin 2>$null
git remote add origin "https://github.com/$Owner/$Repo.git" 2>$null

# Create .env
"OWNER=$Owner`nREPO=$Repo" | Out-File -Encoding utf8 .env

# Re-validate
.\scripts\revalidate.ps1

# Commit changes
git add -A
$hasChanges = (git diff --cached --quiet) -eq $false
if ($hasChanges) {
    git commit -m "chore: repo wiring + badges patch for $Owner/$Repo" 2>$null
}

Write-Host ""
Write-Host "✅ Quick setup complete!" -ForegroundColor Green
Write-Host "Next: git push -u origin main"
