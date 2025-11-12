# Push with Personal Access Token

## Quick Fix

Your token needs the `workflow` scope. Here's how to fix it:

### Step 1: Create/Edit Token with Correct Scopes

1. Go to: **https://github.com/settings/tokens**
2. Either:
   - **Edit existing token**: Find "AgentsSystemV2-Push" → Click "Edit"
   - **Create new token**: Click "Generate new token (classic)"
3. **Make sure BOTH scopes are checked**:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows) ← **This is required!**
4. Click "Generate token" (or "Update token")
5. **Copy the token immediately**

### Step 2: Use Token to Push

**Option A: Set token in remote URL (one-time)**

```powershell
# Replace YOUR_TOKEN with your actual token
git remote set-url origin https://YOUR_TOKEN@github.com/elirancv/Multi-Agent-AI-Development-Framework-Extended-Genius-Edition.git

# Then push
git push -u origin main
```

**Option B: Push and enter credentials when prompted**

```powershell
git push -u origin main
```

When prompted:
- **Username**: `elirancv`
- **Password**: Paste your token (NOT your GitHub password)

---

## Security Note

⚠️ **Important**: If you use Option A (token in URL), it will be stored in `.git/config`.

**After pushing**, you can remove it:
```powershell
git remote set-url origin https://github.com/elirancv/Multi-Agent-AI-Development-Framework-Extended-Genius-Edition.git
```

Then use Option B for future pushes (Windows Credential Manager will save it securely).

---

## Troubleshooting

### "refusing to allow a Personal Access Token to create or update workflow"
**Fix**: Token must have `workflow` scope. Create/edit token and ensure this scope is checked.

### "credential-manager-core is not a git command"
**Fix**: Use Option A (token in URL) or install Git Credential Manager:
```powershell
winget install Git.Git --override "/DIR=C:\Program Files\Git"
```

---

**Last Updated**: 2025-01-12
