"""Dependency audit - Freeze dependencies and check licenses."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

ALLOWED_LICENSES = {"MIT", "Apache-2.0", "Apache 2.0", "BSD-3-Clause", "BSD-2-Clause", "ISC"}


def freeze_dependencies() -> Dict[str, str]:
    """Freeze current dependencies using pip freeze."""
    try:
        result = subprocess.run(
            ["pip", "freeze"],
            capture_output=True,
            text=True,
            check=True,
        )
        deps = {}
        for line in result.stdout.strip().split("\n"):
            if "==" in line:
                name, version = line.split("==", 1)
                deps[name.lower()] = version
        return deps
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {}


def get_package_license(package_name: str) -> tuple[str | None, str]:
    """Get license for a package."""
    try:
        result = subprocess.run(
            ["pip", "show", package_name],
            capture_output=True,
            text=True,
            check=True,
        )
        for line in result.stdout.split("\n"):
            if line.startswith("License:"):
                license_text = line.split(":", 1)[1].strip()
                return license_text, "ok"
        return None, "no license info"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None, "not installed"


def check_license_allowed(license_text: str | None) -> bool:
    """Check if license is in allowed list."""
    if not license_text:
        return False
    license_upper = license_text.upper()
    return any(allowed.upper() in license_upper for allowed in ALLOWED_LICENSES)


def audit_dependencies() -> Dict[str, Any]:
    """Audit all dependencies."""
    frozen = freeze_dependencies()
    audit_result: Dict[str, Any] = {
        "total": len(frozen),
        "allowed": [],
        "unknown": [],
        "blocked": [],
        "frozen": frozen,
    }
    
    for package, version in frozen.items():
        license_text, status = get_package_license(package)
        if check_license_allowed(license_text):
            audit_result["allowed"].append({
                "package": package,
                "version": version,
                "license": license_text,
            })
        elif license_text:
            audit_result["unknown"].append({
                "package": package,
                "version": version,
                "license": license_text,
            })
        else:
            audit_result["blocked"].append({
                "package": package,
                "version": version,
                "status": status,
            })
    
    return audit_result


def generate_markdown_report(audit_result: Dict[str, Any]) -> str:
    """Generate markdown report."""
    lines = [
        "# Dependency Audit Report",
        "",
        f"**Total dependencies**: {audit_result['total']}",
        f"**Allowed licenses**: {len(audit_result['allowed'])}",
        f"**Unknown licenses**: {len(audit_result['unknown'])}",
        f"**Blocked/No license**: {len(audit_result['blocked'])}",
        "",
        "## Allowed Dependencies (MIT/Apache2/BSD)",
        "",
    ]
    
    for dep in audit_result["allowed"]:
        lines.append(f"- **{dep['package']}** {dep['version']} - {dep['license']}")
    
    if audit_result["unknown"]:
        lines.extend([
            "",
            "## Unknown Licenses (Review Required)",
            "",
        ])
        for dep in audit_result["unknown"]:
            lines.append(f"- **{dep['package']}** {dep['version']} - {dep['license']}")
    
    if audit_result["blocked"]:
        lines.extend([
            "",
            "## Blocked/No License Info",
            "",
        ])
        for dep in audit_result["blocked"]:
            lines.append(f"- **{dep['package']}** {dep['version']} - {dep['status']}")
    
    lines.extend([
        "",
        "## Frozen Dependencies",
        "",
        "```",
    ])
    for package, version in sorted(audit_result["frozen"].items()):
        lines.append(f"{package}=={version}")
    lines.append("```")
    
    return "\n".join(lines)


def main() -> int:
    """Main entry point."""
    print("Auditing dependencies...", file=sys.stderr)
    audit_result = audit_dependencies()
    
    # Save JSON
    json_path = Path("deps-audit.json")
    json_path.write_text(json.dumps(audit_result, indent=2))
    print(f"Saved JSON: {json_path}", file=sys.stderr)
    
    # Save Markdown
    md_path = Path("docs/deps-audit.md")
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(generate_markdown_report(audit_result))
    print(f"Saved Markdown: {md_path}", file=sys.stderr)
    
    # Summary
    print(f"\nSummary:", file=sys.stderr)
    print(f"  Total: {audit_result['total']}", file=sys.stderr)
    print(f"  Allowed: {len(audit_result['allowed'])}", file=sys.stderr)
    print(f"  Unknown: {len(audit_result['unknown'])}", file=sys.stderr)
    print(f"  Blocked: {len(audit_result['blocked'])}", file=sys.stderr)
    
    if audit_result["unknown"] or audit_result["blocked"]:
        print("\n⚠️  Review required for unknown/blocked licenses", file=sys.stderr)
        return 1
    
    print("\n✅ All dependencies have allowed licenses", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

