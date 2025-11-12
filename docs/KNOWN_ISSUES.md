# Known Issues and Quick Fixes

Common issues and their solutions for the Multi-Agent AI Development Framework.

## Windows PowerShell Separators

### Issue
PowerShell uses `;` as command separator, not `&&`.

### Solution
```powershell
# Use semicolon instead of &&
python cli.py --pipeline pipeline/production.yaml --dry-run; python cli.py --version
```

Or use separate commands:
```powershell
python cli.py --pipeline pipeline/production.yaml --dry-run
python cli.py --version
```

## Graphviz Not Found

### Issue
Error: `graphviz` command not found when exporting pipeline graphs.

### Solution

**Windows:**
1. Download from: https://graphviz.org/download/
2. Install and add to PATH
3. Restart terminal

**Linux (Debian/Ubuntu):**
```bash
sudo apt-get update
sudo apt-get install graphviz
```

**macOS:**
```bash
brew install graphviz
```

**Verify:**
```bash
dot -V
```

## pdoc Not Installed

### Issue
API documentation generation fails with "pdoc not found".

### Solution
```bash
pip install pdoc
```

Or skip API docs generation (it's optional):
```bash
# API docs are optional, pipeline will continue without them
```

## pre-commit Not Found

### Issue
Pre-commit hooks fail or are skipped.

### Solution
```bash
pip install pre-commit
pre-commit install
```

Or skip pre-commit (it's optional):
```bash
# Pre-commit is optional, code will still work
```

## Python Version < 3.8

### Issue
Framework requires Python 3.8+.

### Solution
Upgrade Python:
- Download from: https://www.python.org/downloads/
- Or use pyenv: `pyenv install 3.11`

Verify:
```bash
python --version
```

## Write Permissions Error

### Issue
Cannot write to `out/` directory.

### Solution

**Linux/macOS:**
```bash
chmod -R 755 out/
```

**Windows:**
- Check folder permissions in Properties → Security
- Ensure user has Write permissions

**All platforms:**
```bash
# Create directory if missing
mkdir -p out
```

## Missing Dependencies

### Issue
Import errors for required modules.

### Solution
```bash
pip install -r requirements.txt
```

Verify installation:
```bash
python -c "import jinja2, yaml, pydantic; print('OK')"
```

## Environment Variables Not Set

### Issue
ORCH_* environment variables not recognized.

### Solution
Set variables before running:
```bash
# Linux/macOS
export ORCH_ENDPOINT="http://localhost:4318/v1/traces"
python cli.py --pipeline pipeline/production.yaml

# Windows PowerShell
$env:ORCH_ENDPOINT="http://localhost:4318/v1/traces"
python cli.py --pipeline pipeline/production.yaml
```

Or use CLI flags instead:
```bash
python cli.py --pipeline pipeline/production.yaml --otel-endpoint "http://localhost:4318/v1/traces"
```

## Pipeline Validation Errors

### Issue
YAML pipeline fails validation.

### Solution
1. Validate YAML syntax:
   ```bash
   python cli.py --pipeline pipeline/production.yaml --dry-run
   ```

2. Check YAML indentation (must be 2 spaces)

3. Verify agent/advisor names match Python class names (PascalCase)

4. Check for missing required fields:
   - `name`
   - `agent`
   - `advisor`
   - `output`

## Checkpoint Store Errors

### Issue
SQLite checkpoint store fails.

### Solution
1. Ensure SQLite is available (usually built-in with Python)

2. Check write permissions for `out/` directory

3. Use filesystem store as fallback:
   ```bash
   python cli.py --pipeline pipeline/production.yaml --checkpoint-store fs
   ```

## Smoke Tests Fail

### Issue
Smoke tests fail without artifacts.

### Solution
This is expected in dry-run mode. Smoke tests require actual pipeline execution:
```bash
# Run actual pipeline (not dry-run)
python cli.py --pipeline pipeline/production.yaml --save-artifacts

# Then run smoke tests
python scripts/smoke_test.py
```

## Doctor Command Not Found

### Issue
`multiagent doctor` command not available.

### Solution
Run directly:
```bash
python scripts/doctor.py
```

Or add to CLI (planned for v1.1):
```bash
python cli.py doctor
```

## Getting Help

If you encounter an issue not listed here:

1. Run doctor command:
   ```bash
   python scripts/doctor.py --verbose
   ```

2. Check logs in `out/` directory

3. Open an issue on GitHub with:
   - Error message
   - Python version
   - Operating system
   - Steps to reproduce

## See Also

- [Quickstart Guide](QUICKSTART.md)
- [Release Verification](RELEASE_VERIFICATION.md)
- [Scripts Usage](SCRIPTS_USAGE.md)
