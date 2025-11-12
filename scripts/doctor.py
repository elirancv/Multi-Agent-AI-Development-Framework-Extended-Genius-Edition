"""Doctor command - Environment diagnostics for multi-agent framework."""

from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List

# Exit codes
EXIT_OK = 0
EXIT_WARNINGS = 1
EXIT_ERRORS = 2


def check_python_version() -> tuple[bool, str]:
    """Check Python version >= 3.8."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    return False, f"Python {version.major}.{version.minor}.{version.micro} (requires >= 3.8)"


def check_module(module_name: str, optional: bool = False) -> tuple[bool, str]:
    """Check if a Python module is importable."""
    try:
        __import__(module_name)
        return True, f"{module_name} installed"
    except ImportError:
        if optional:
            return False, f"{module_name} not installed (optional)"
        return False, f"{module_name} not installed (required)"


def check_command(command: str, optional: bool = False) -> tuple[bool, str]:
    """Check if a command is available in PATH."""
    if shutil.which(command):
        return True, f"{command} found in PATH"
    if optional:
        return False, f"{command} not found (optional)"
    return False, f"{command} not found (required)"


def check_write_permissions(path: Path) -> tuple[bool, str]:
    """Check write permissions for a directory."""
    try:
        test_file = path / ".doctor_test"
        test_file.touch()
        test_file.unlink()
        return True, f"Write permissions OK: {path}"
    except (PermissionError, OSError) as e:
        return False, f"No write permissions: {path} ({e})"


def check_disk_space(path: Path, min_gb: float = 0.1) -> tuple[bool, str]:
    """Check available disk space."""
    try:
        stat = shutil.disk_usage(path)
        free_gb = stat.free / (1024**3)
        if free_gb >= min_gb:
            return True, f"Disk space OK: {free_gb:.2f} GB free"
        return False, f"Low disk space: {free_gb:.2f} GB free (need {min_gb} GB)"
    except OSError as e:
        return False, f"Cannot check disk space: {e}"


def check_env_vars() -> tuple[bool, List[str]]:
    """Check ORCH_* environment variables."""
    orch_vars = {k: v for k, v in os.environ.items() if k.startswith("ORCH_")}
    if not orch_vars:
        return True, []
    
    issues = []
    for key, value in orch_vars.items():
        if not value or value.strip() == "":
            issues.append(f"{key} is empty")
        elif " " in value and "=" not in value:
            issues.append(f"{key} may have invalid format")
    
    if issues:
        return False, issues
    return True, [f"{k}={v[:50]}..." if len(v) > 50 else f"{k}={v}" for k, v in orch_vars.items()]


def check_cli_version() -> tuple[bool, str]:
    """Check if cli.py --version works."""
    try:
        import sys
        from pathlib import Path
        # Add project root to path
        project_root = Path(__file__).parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        from src import __version__
        return True, f"CLI version: {__version__}"
    except Exception as e:
        return False, f"Cannot get CLI version: {e}"


def run_doctor(verbose: bool = False, json_output: bool = False) -> int:
    """Run doctor diagnostics."""
    checks: Dict[str, Any] = {
        "errors": [],
        "warnings": [],
        "info": [],
    }
    
    # Python version
    ok, msg = check_python_version()
    if ok:
        checks["info"].append({"check": "python_version", "status": "ok", "message": msg})
    else:
        checks["errors"].append({"check": "python_version", "status": "error", "message": msg})
    
    # Required modules
    required_modules = ["jinja2", "yaml", "pydantic"]
    for module in required_modules:
        ok, msg = check_module(module, optional=False)
        if ok:
            checks["info"].append({"check": f"module_{module}", "status": "ok", "message": msg})
        else:
            checks["errors"].append({"check": f"module_{module}", "status": "error", "message": msg})
    
    # Optional modules
    optional_modules = [("graphviz", True), ("pdoc", True), ("pre_commit", True)]
    for module, is_optional in optional_modules:
        ok, msg = check_module(module.replace("_", ""), optional=is_optional)
        if ok:
            checks["info"].append({"check": f"module_{module}", "status": "ok", "message": msg})
        else:
            checks["warnings"].append({"check": f"module_{module}", "status": "warning", "message": msg})
    
    # Commands
    optional_commands = [("graphviz", True), ("pdoc", True), ("pre-commit", True)]
    for cmd, is_optional in optional_commands:
        ok, msg = check_command(cmd, optional=is_optional)
        if ok:
            checks["info"].append({"check": f"command_{cmd}", "status": "ok", "message": msg})
        else:
            checks["warnings"].append({"check": f"command_{cmd}", "status": "warning", "message": msg})
    
    # Write permissions
    out_dir = Path("out")
    out_dir.mkdir(exist_ok=True)
    ok, msg = check_write_permissions(out_dir)
    if ok:
        checks["info"].append({"check": "write_permissions", "status": "ok", "message": msg})
    else:
        checks["errors"].append({"check": "write_permissions", "status": "error", "message": msg})
    
    # Disk space
    ok, msg = check_disk_space(out_dir, min_gb=0.1)
    if ok:
        checks["info"].append({"check": "disk_space", "status": "ok", "message": msg})
    else:
        checks["warnings"].append({"check": "disk_space", "status": "warning", "message": msg})
    
    # Environment variables
    ok, env_info = check_env_vars()
    if ok:
        if env_info:
            checks["info"].append({"check": "env_vars", "status": "ok", "message": f"Found {len(env_info)} ORCH_* variables"})
        else:
            checks["info"].append({"check": "env_vars", "status": "ok", "message": "No ORCH_* variables set"})
    else:
        checks["warnings"].append({"check": "env_vars", "status": "warning", "message": "; ".join(env_info)})
    
    # CLI version
    ok, msg = check_cli_version()
    if ok:
        checks["info"].append({"check": "cli_version", "status": "ok", "message": msg})
    else:
        checks["errors"].append({"check": "cli_version", "status": "error", "message": msg})
    
    # Output
    if json_output:
        result = {
            "status": "ok" if not checks["errors"] else "error",
            "errors": len(checks["errors"]),
            "warnings": len(checks["warnings"]),
            "checks": checks["errors"] + checks["warnings"] + checks["info"],
        }
        print(json.dumps(result, indent=2))
    else:
        if checks["errors"]:
            print("❌ Errors:", file=sys.stderr)
            for err in checks["errors"]:
                print(f"  • {err['message']}", file=sys.stderr)
        
        if checks["warnings"]:
            print("⚠️  Warnings:", file=sys.stderr)
            for warn in checks["warnings"]:
                print(f"  • {warn['message']}", file=sys.stderr)
        
        if verbose and checks["info"]:
            print("✅ OK:", file=sys.stderr)
            for info in checks["info"]:
                print(f"  • {info['message']}", file=sys.stderr)
        
        if not checks["errors"] and not checks["warnings"]:
            print("✅ All checks passed!", file=sys.stderr)
    
    # Exit code
    if checks["errors"]:
        return EXIT_ERRORS
    if checks["warnings"]:
        return EXIT_WARNINGS
    return EXIT_OK


def main() -> int:
    """Main entry point for doctor command."""
    import argparse
    
    ap = argparse.ArgumentParser(description="Diagnose environment for multi-agent framework")
    ap.add_argument("--json", action="store_true", help="Output JSON format")
    ap.add_argument("--verbose", "-v", action="store_true", help="Show all checks")
    
    args = ap.parse_args()
    return run_doctor(verbose=args.verbose, json_output=args.json)


if __name__ == "__main__":
    sys.exit(main())

