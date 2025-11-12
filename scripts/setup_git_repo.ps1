# Git Repository Setup Script for v1.0.0
# Run this script to initialize git and push to GitHub

$ErrorActionPreference = "Stop"

Write-Host "=== Git Repository Setup for v1.0.0 ===" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Git is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Check if already a git repo
if (Test-Path ".git") {
    Write-Host "Warning: .git directory already exists" -ForegroundColor Yellow
    Write-Host "Checking current status..." -ForegroundColor Yellow
    git status --short | Select-Object -First 10
    Write-Host ""
    $continue = Read-Host "Continue with setup? (y/n)"
    if ($continue -ne "y") {
        Write-Host "Aborted." -ForegroundColor Yellow
        exit 0
    }
} else {
    Write-Host "[1/6] Initializing git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
}

# Check current branch
Write-Host "[2/6] Checking branch..." -ForegroundColor Yellow
$currentBranch = git branch --show-current 2>&1
if ($currentBranch -and $currentBranch -ne "main") {
    Write-Host "Renaming branch to 'main'..." -ForegroundColor Yellow
    git branch -M main
}
Write-Host "✅ Branch: main" -ForegroundColor Green

# Add all files
Write-Host "[3/6] Staging all files..." -ForegroundColor Yellow
git add .
$staged = git status --short | Measure-Object -Line
Write-Host "✅ Staged $($staged.Lines) files" -ForegroundColor Green

# Initial commit
Write-Host "[4/6] Creating initial commit..." -ForegroundColor Yellow
git commit -m "chore: initial commit - v1.0.0 release"
Write-Host "✅ Initial commit created" -ForegroundColor Green

# Create v1.0.0 tag
Write-Host "[5/6] Creating v1.0.0 tag..." -ForegroundColor Yellow
git tag v1.0.0
Write-Host "✅ Tag v1.0.0 created" -ForegroundColor Green

# Set remote
Write-Host "[6/6] Setting up remote..." -ForegroundColor Yellow
$remoteUrl = "https://github.com/elirancv/Multi-Agent-AI-Development-Framework-Extended-Genius-Edition.git"

# Check if remote exists
$existingRemote = git remote get-url origin 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "Remote 'origin' already exists: $existingRemote" -ForegroundColor Yellow
    $update = Read-Host "Update to new URL? (y/n)"
    if ($update -eq "y") {
        git remote set-url origin $remoteUrl
        Write-Host "✅ Remote updated" -ForegroundColor Green
    }
} else {
    git remote add origin $remoteUrl
    Write-Host "✅ Remote added: $remoteUrl" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Setup Complete! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Review changes: git status" -ForegroundColor White
Write-Host "2. Push to GitHub: git push -u origin main" -ForegroundColor White
Write-Host "3. Push tags: git push origin --tags" -ForegroundColor White
Write-Host ""
Write-Host "Ready to push? Run:" -ForegroundColor Yellow
Write-Host "  git push -u origin main" -ForegroundColor White
Write-Host "  git push origin --tags" -ForegroundColor White
