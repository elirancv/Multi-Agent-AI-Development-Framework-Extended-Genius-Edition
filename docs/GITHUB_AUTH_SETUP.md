# GitHub Authentication Setup Guide

## Quick Options

### Option 1: Install GitHub CLI (Recommended)

**Windows (Chocolatey)**:
```powershell
choco install gh -y
gh auth login --scopes workflow
```

**Windows (winget)**:
```powershell
winget install --id GitHub.cli
gh auth login --scopes workflow
```

**Manual Download**:
- Visit: https://cli.github.com/
- Download Windows installer
- Run installer
- Then: `gh auth login --scopes workflow`

### Option 2: Personal Access Token (No Installation)

1. **Create Token**:
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token" → "Generate new token (classic)"
   - Name: `AgentsSystemV2-Push`
   - Expiration: Choose (90 days recommended)
   - **Select scopes**:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `workflow` (Update GitHub Action workflows)

2. **Copy Token** (save it - you won't see it again!)

3. **Configure Git**:
   ```powershell
   # Set credential helper (Windows)
   git config --global credential.helper manager-core

   # Or use token directly in URL (one-time)
   git remote set-url origin https://<YOUR_TOKEN>@github.com/elirancv/Multi-Agent-AI-Development-Framework-Extended-Genius-Edition.git
   ```

4. **Push**:
   ```powershell
   git push -u origin main
   ```
   - If prompted, username: `elirancv`
   - Password: paste your token

### Option 3: SSH (If You Have SSH Key)

1. **Check for SSH key**:
   ```powershell
   Test-Path ~/.ssh/id_rsa.pub
   ```

2. **If exists, add to GitHub**:
   - Copy: `Get-Content ~/.ssh/id_rsa.pub`
   - Add to: https://github.com/settings/keys

3. **Change remote to SSH**:
   ```powershell
   git remote set-url origin git@github.com:elirancv/Multi-Agent-AI-Development-Framework-Extended-Genius-Edition.git
   ```

4. **Push**:
   ```powershell
   git push -u origin main
   ```

---

## Recommended: Personal Access Token (Fastest)

**Steps**:

1. Create token: https://github.com/settings/tokens
   - Scopes: `repo`, `workflow`
   - Copy token immediately

2. Push with token:
   ```powershell
   git push -u origin main
   ```
   - Username: `elirancv`
   - Password: `<paste-token>`

3. Windows Credential Manager will save it automatically.

---

## Troubleshooting

### "refusing to allow a Personal Access Token to create or update workflow"
**Fix**: Token must have `workflow` scope. Create a new token with this scope.

### "Permission denied (publickey)"
**Fix**: Use HTTPS instead of SSH, or add SSH key to GitHub.

### "remote: Invalid username or password"
**Fix**:
- For PAT: Use token as password, not your GitHub password
- Username should be your GitHub username (`elirancv`)

---

**Last Updated**: 2025-01-12
