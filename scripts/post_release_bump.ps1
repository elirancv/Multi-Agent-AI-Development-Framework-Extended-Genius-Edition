# Post-release version bump script (PowerShell)
# Bumps version to next dev version after release

param(
    [string]$CurrentVersion = "1.0.0",
    [string]$NextVersion = "1.0.1-dev"
)

Write-Host "Bumping version from $CurrentVersion to $NextVersion..."

# Update src/__init__.py
if (Test-Path "src/__init__.py") {
    $content = Get-Content "src/__init__.py" -Raw
    $content = $content -replace "__version__ = `"$CurrentVersion`"", "__version__ = `"$NextVersion`""
    Set-Content "src/__init__.py" -Value $content -NoNewline
    Write-Host "✅ Updated src/__init__.py"
}

# Update pyproject.toml
if (Test-Path "pyproject.toml") {
    $content = Get-Content "pyproject.toml" -Raw
    $content = $content -replace "version = `"$CurrentVersion`"", "version = `"$NextVersion`""
    Set-Content "pyproject.toml" -Value $content -NoNewline
    Write-Host "✅ Updated pyproject.toml"
}

# Verify
Write-Host ""
Write-Host "Verifying version bump:"
python -c "from src import __version__; print(f'Version: {__version__}')"

Write-Host ""
Write-Host "✅ Version bumped to $NextVersion"
Write-Host ""
Write-Host "Next steps:"
Write-Host "  git add -A"
Write-Host "  git commit -m 'chore: bump version to $NextVersion'"
Write-Host "  git push"

