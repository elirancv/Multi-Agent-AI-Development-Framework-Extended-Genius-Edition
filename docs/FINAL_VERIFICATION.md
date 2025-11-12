# Final Verification - Pre-Tag Checklist

Quick commands to verify everything is ready before tagging v1.0.0.

## ✅ Required Checks (1-2 minutes)

### Version Check
```bash
python cli.py --version
```
**Expected**: `1.0.0`

### Dry-Run Pipeline
```bash
python cli.py --pipeline pipeline/production.yaml --dry-run --export-graph out/pipeline.dot
```
**Expected**: Pipeline validates, graph exported to `out/pipeline.dot`

### Smoke Tests
```bash
python scripts/smoke_test.py --skip-slow --json
```
**Expected**: Tests pass (may fail without artifacts in dry-run - OK)

### Coverage (Local Check)
```bash
pip install coverage
coverage run -m pytest
coverage xml -o coverage.xml
coverage report
```
**Expected**: Coverage report generated, no critical failures

## ✅ Plugin Loader Self-Test

### Quick Test
```bash
python - <<'PY'
from src.orchestrator.plugin_loader import load_plugins

agents = load_plugins("multiagent.agents")
advs = load_plugins("multiagent.advisors")

print("Agents:", list(agents.keys())[:5])
print("Advisors:", list(advs.keys())[:5])
PY
```

**Expected**: Empty lists if no external plugins installed (OK), or plugin names if installed

### Full Test
```bash
python -c "
from src.orchestrator.factory import agent_factory, advisor_factory
from src.orchestrator.plugin_loader import get_agent_plugins, get_advisor_plugins

print('Core agents:', len(get_agent_plugins()))
print('Core advisors:', len(get_advisor_plugins()))

# Test factory
try:
    agent = agent_factory('RequirementsDraftingAgent')
    print('✅ Agent factory works')
except Exception as e:
    print(f'❌ Agent factory error: {e}')

try:
    advisor = advisor_factory('RequirementsAdvisor')
    print('✅ Advisor factory works')
except Exception as e:
    print(f'❌ Advisor factory error: {e}')
"
```

## ✅ CI Secrets Checklist

Before pushing, verify these secrets are configured in GitHub:

- [ ] **CODECOV_TOKEN** (if private repo) - Optional, public repos don't need it
- [ ] **PYPI_TOKEN** (for v1.1+) - Format: `pypi-...` token from PyPI
- [ ] **GPG Signing Key** (optional) - If enforcing signed tags

### Setting Secrets

1. Go to: Repository Settings → Secrets and variables → Actions
2. Add repository secret:
   - Name: `CODECOV_TOKEN` or `PYPI_TOKEN`
   - Value: Your token

## ✅ README Badge Patch

**Important**: Update Codecov badge URL in `README.md`:

Replace:
```markdown
[![Coverage](https://codecov.io/gh/your-org/AgentsSystemV2/branch/main/graph/badge.svg)](https://codecov.io/gh/your-org/AgentsSystemV2)
```

With your actual org/repo:
```markdown
[![Coverage](https://codecov.io/gh/<owner>/<repo>/branch/main/graph/badge.svg)](https://codecov.io/gh/<owner>/<repo>)
```

## ✅ Final Git Status

```bash
# Check what will be committed
git status

# Review changes
git diff --cached --stat

# Verify no temporary files
git diff --cached --name-only | grep -E "(tmp|temp|\.log|\.tmp)"
```

## ✅ Ready to Tag

Once all checks pass:

```bash
# Bash
CREATE_TAG=true SIGN_TAG=true TAG_NAME=v1.0.0 ./scripts/commit_push.sh

# PowerShell
.\scripts\commit_push.ps1 -CreateTag:$true -SignTag:$true -TagName "v1.0.0"
```

## See Also

- [Pre-Release Sanity](PRE_RELEASE_SANITY.md)
- [Release Checklist](RELEASE_CHECKLIST_v1.0.0.md)
- [Definition of Done](DEFINITION_OF_DONE_v1.0.md)

