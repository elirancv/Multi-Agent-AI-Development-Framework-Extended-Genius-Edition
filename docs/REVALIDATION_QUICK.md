# Re-Validation Quick Guide (5 Lines)

**Goal**: Turn YELLOW → GREEN by installing tools and fixing badges.

## Quick Commands

**Bash** (with .env):
```bash
cp .env.example .env  # Edit OWNER/REPO
chmod +x scripts/revalidate.sh && ./scripts/revalidate.sh
```

**PowerShell** (with .env):
```powershell
Copy-Item .env.example .env  # Edit OWNER/REPO
.\scripts\revalidate.ps1
```

**Manual** (no .env):
```bash
OWNER=myusername REPO=myrepo ./scripts/revalidate.sh
```

**Result**: Check `out/validation/FINAL_VALIDATION.md` for GREEN/YELLOW/RED status.

**If GREEN**: Ship with `CREATE_TAG=true SIGN_TAG=true TAG_NAME=v1.0.0 ./scripts/commit_push.sh`

