# Quick Start Release Guide

**Owner**: `elirancv`
**Repo**: `Multi-Agent-AI-Development-Framework-Extended-Genius-Edition`

---

## 🚀 One-Command Setup (Fastest)

### Bash (macOS/Linux)

```bash
cd /path/to/your/project
chmod +x scripts/quick_setup.sh
./scripts/quick_setup.sh
git push -u origin main
```

### PowerShell (Windows)

```powershell
cd \path\to\your\project
.\scripts\quick_setup.ps1
git push -u origin main
```

**What it does**:
- ✅ Sets up Git repo with correct remote
- ✅ Creates `.env` with owner/repo
- ✅ Runs re-validation (patches badges, installs tools)
- ✅ Commits changes
- ✅ Ready for push

---

## 📋 Step-by-Step (If You Prefer)

### Step 1: Git Setup

**Bash**:
```bash
cd /path/to/your/project
git init -b main
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/elirancv/Multi-Agent-AI-Development-Framework-Extended-Genius-Edition.git
```

**PowerShell**:
```powershell
cd \path\to\your\project
git init -b main
git remote remove origin 2>$null
git remote add origin https://github.com/elirancv/Multi-Agent-AI-Development-Framework-Extended-Genius-Edition.git
```

### Step 2: Create .env

**Bash**:
```bash
printf "OWNER=elirancv\nREPO=Multi-Agent-AI-Development-Framework-Extended-Genius-Edition\n" > .env
```

**PowerShell**:
```powershell
"OWNER=elirancv`nREPO=Multi-Agent-AI-Development-Framework-Extended-Genius-Edition" | Out-File -Encoding utf8 .env
```

### Step 3: Re-Validate (Patches Badges + Runs Checks)

**Bash**:
```bash
chmod +x scripts/revalidate.sh
./scripts/revalidate.sh
```

**PowerShell**:
```powershell
.\scripts\revalidate.ps1
```

**Expected**: Status turns GREEN after badge patching.

### Step 4: Commit & Push

**Bash**:
```bash
git add -A
git commit -m "chore: repo wiring + badges patch for elirancv/Multi-Agent-AI-Development-Framework-Extended-Genius-Edition"
git push -u origin main
```

**PowerShell**:
```powershell
git add -A
git commit -m "chore: repo wiring + badges patch for elirancv/Multi-Agent-AI-Development-Framework-Extended-Genius-Edition"
git push -u origin main
```

### Step 5: Release

**Bash**:
```bash
# Dry-run first (recommended)
./scripts/release_all.sh --dry-run

# Real release
./scripts/release_all.sh
```

**PowerShell**:
```powershell
# Dry-run first (recommended)
.\scripts\release_all.ps1 -DryRun

# Real release
.\scripts\release_all.ps1
```

---

## 🔍 Verify Status

Check validation report:
```bash
cat out/validation/FINAL_VALIDATION.md
```

Or view JSON:
```bash
cat out/validation/FINAL_VALIDATION.json | jq .status
```

**Expected**: `"green"` after badge patching.

---

## 🐛 Troubleshooting

### "remote origin already exists"
**Fix**: Script handles this automatically (removes and re-adds).

### "Badge URLs still contain placeholders"
**Fix**:
- Check `.env` file exists and has OWNER/REPO set
- Or update manually in README.md (lines 3, 4, 9, 77)

### "Permission denied" on push
**Fix**:
- Ensure GitHub authentication (SSH key or token)
- Or use `gh auth login` if using GitHub CLI

### Graphviz not found
**Fix**: Optional - install system package:
- macOS: `brew install graphviz`
- Ubuntu: `sudo apt-get install graphviz`
- Windows: `choco install graphviz`

**Note**: Not blocking - graph export works with Python package.

---

## ✅ After Push

1. **Verify Workflows**: Check GitHub Actions run
2. **Set Secrets** (if needed): CODECOV_TOKEN, PYPI_TOKEN
3. **Branch Protection**: See `docs/GITHUB_PROTECTION_SETUP.md`
4. **Create Release**: Use `docs/GITHUB_RELEASE_SHORT_v1.0.0.md`

---

**Last Updated**: 2025-01-12
