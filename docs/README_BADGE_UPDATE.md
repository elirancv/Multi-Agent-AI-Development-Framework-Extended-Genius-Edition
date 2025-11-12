# README Badge URL Update

## Important: Update Codecov Badge

The Codecov badge in `README.md` currently uses placeholder URLs. Update them with your actual repository information.

### Current (Placeholder)

```markdown
[![Coverage](https://codecov.io/gh/your-org/AgentsSystemV2/branch/main/graph/badge.svg)](https://codecov.io/gh/your-org/AgentsSystemV2)
```

### Replace With

```markdown
[![Coverage](https://codecov.io/gh/<owner>/<repo>/branch/main/graph/badge.svg)](https://codecov.io/gh/<owner>/<repo>)
```

**Example**:
- Owner: `myusername`
- Repo: `multiagent-framework`
- URL: `https://codecov.io/gh/myusername/multiagent-framework/branch/main/graph/badge.svg`

### All Badges to Update

Check these badges in `README.md`:

1. **Version**: `your-org/AgentsSystemV2` → `<owner>/<repo>`
2. **Coverage**: `your-org/AgentsSystemV2` → `<owner>/<repo>`
3. **CI**: Verify workflow path is correct
4. **Other badges**: Update if they reference repository

### Quick Find & Replace

```bash
# Find all badge URLs
grep -n "your-org\|AgentsSystemV2" README.md

# Replace (adjust owner/repo)
sed -i 's/your-org\/AgentsSystemV2/<owner>\/<repo>/g' README.md
```

### Verification

After updating:
1. View README on GitHub
2. Click badges to verify they link correctly
3. Check Codecov badge shows coverage (after first CI run)
