# Push Instructions - Quick Guide

## Personal Access Token Method (Fastest)

### Step 1: Create Token

1. Go to: **https://github.com/settings/tokens**
2. Click: **"Generate new token"** → **"Generate new token (classic)"**
3. Fill in:
   - **Note**: `AgentsSystemV2-Push`
   - **Expiration**: Choose (90 days recommended)
   - **Scopes**:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `workflow` (Update GitHub Action workflows)
4. Click: **"Generate token"**
5. **⚠️ COPY THE TOKEN IMMEDIATELY** - You won't see it again!

### Step 2: Push

```powershell
git push -u origin main
```

**When prompted:**
- **Username**: `elirancv`
- **Password**: Paste your token (NOT your GitHub password)

Windows Credential Manager will save it automatically for future pushes.

---

## Alternative: Install GitHub CLI (Requires Admin)

If you have admin rights:

```powershell
# Run PowerShell as Administrator, then:
choco install gh -y
gh auth login --scopes workflow
git push -u origin main
```

---

## Troubleshooting

### "refusing to allow a Personal Access Token to create or update workflow"
**Fix**: Token must have `workflow` scope. Create a new token with this scope.

### "Permission denied"
**Fix**: Make sure you selected `repo` and `workflow` scopes when creating the token.

### "remote: Invalid username or password"
**Fix**:
- Username should be `elirancv` (your GitHub username)
- Password should be the token, NOT your GitHub password

---

**Last Updated**: 2025-01-12
