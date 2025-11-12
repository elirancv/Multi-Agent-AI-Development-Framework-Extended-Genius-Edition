Param(
  [string]$BranchDefault = "main",
  [bool]$CreateTag = $false,
  [string]$TagName = "v1.0.0",
  [bool]$SignTag = $false,
  [bool]$DryRun = $false
)

$ErrorActionPreference = "Stop"

Write-Host "[1/7] Detecting branch & remote..."
try { $BRANCH = (git rev-parse --abbrev-ref HEAD) } catch { $BRANCH = $BranchDefault }
try { $REMOTE = (git remote | Select-Object -First 1) } catch { $REMOTE = "origin" }
Write-Host "   • branch: $BRANCH"
Write-Host "   • remote: $REMOTE"

Write-Host "[2/7] Housekeeping: formatting & linting..."
if (Get-Command pre-commit -ErrorAction SilentlyContinue) {
  try { pre-commit install | Out-Null } catch {}
  pre-commit run --all-files
} else { Write-Host "   (pre-commit not found, skipping)" }

if (Get-Command ruff -ErrorAction SilentlyContinue) { ruff check --fix . }
if (Get-Command mypy -ErrorAction SilentlyContinue) { mypy . } else { Write-Host "   (mypy not found, skipping)" }

Write-Host "[3/7] Tests..."
pytest -q
python scripts/smoke_test.py --skip-slow --json | Out-Null

Write-Host "[4/7] Build docs (optional)..."
if (Get-Command pdoc -ErrorAction SilentlyContinue) {
  try { pdoc -o docs/api src } catch { Write-Host "   (pdoc failed/absent, continuing)" }
} else { Write-Host "   (pdoc not found, skipping api docs)" }

Write-Host "[5/7] Export graph (optional)..."
try { python cli.py --pipeline pipeline/production.yaml --dry-run --export-graph out/pipeline.dot } catch {}

Write-Host "[6/7] Git add & commit..."
git add -A

$versionLine = "unknown"
try {
  $versionLine = python -c "import sys; sys.path.insert(0, '.'); from src import __version__; print(__version__)"
} catch {}

$commitMsg = @"
chore(repo): tidy project & release bundle

- run pre-commit, ruff fix, type-checks
- run tests & smoke
- update docs/api (if available) & export graph
- prepare release assets

Version: $versionLine
"@

$hasChanges = (git diff --cached --quiet) -eq $false
if ($hasChanges) {
  git commit -m $commitMsg
} else {
  Write-Host "   No staged changes. Skipping commit."
}

Write-Host "[7/7] Push..."
if ($DryRun) {
  Write-Host "   DRY_RUN=true -> skipping push"
} else {
  git push $REMOTE $BRANCH
}

if ($CreateTag) {
  Write-Host "   Creating tag: $TagName"
  if ($SignTag) {
    git tag -s $TagName -m "Release $TagName"
  } else {
    git tag $TagName -m "Release $TagName"
  }
  if (-not $DryRun) { git push $REMOTE $TagName }
}

Write-Host "✅ Done."
