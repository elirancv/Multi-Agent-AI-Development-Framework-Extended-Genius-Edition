# SBOM (Software Bill of Materials) Generation

This document describes how to generate and maintain SBOM files for the Multi-Agent AI Development Framework.

## Overview

SBOM (Software Bill of Materials) provides a complete inventory of all dependencies, their versions, and licenses. This is essential for:
- Security vulnerability tracking
- License compliance
- Supply chain transparency
- Regulatory compliance (e.g., CISA, NIST)

## Tool: CycloneDX

We use [CycloneDX](https://cyclonedx.org/) format, which is an industry-standard SBOM format supported by:
- GitHub Dependency Graph
- Snyk, Sonatype, and other security tools
- CISA SBOM requirements

## Installation

```bash
# Install cyclonedx-bom
pip install cyclonedx-bom

# Or via requirements-dev.txt (if you have one)
pip install -r requirements-dev.txt
```

## Manual Generation

### Generate SBOM from requirements.txt

```bash
# Generate CycloneDX JSON
cyclonedx-py -r requirements.txt -o sbom.json

# Generate CycloneDX XML (alternative format)
cyclonedx-py -r requirements.txt -o sbom.xml --format xml
```

### Generate SBOM from installed packages

```bash
# Generate from current environment
cyclonedx-py -e -o sbom.json
```

## Automated CI Generation

The SBOM is automatically generated in CI/CD workflows. See `.github/workflows/sbom.yml` for details.

### Workflow Integration

The SBOM generation workflow:
1. Runs on every release (tag push)
2. Generates SBOM from `requirements.txt`
3. Uploads as release artifact
4. Optionally publishes to GitHub Dependency Graph

## SBOM Artifacts

Generated SBOM files are stored in:
- `sbom/` directory (local)
- GitHub Release artifacts (for releases)
- GitHub Dependency Graph (if enabled)

## File Locations

- **SBOM JSON**: `sbom/sbom.json`
- **SBOM XML**: `sbom/sbom.xml` (optional)
- **CI Artifact**: Available in GitHub Actions artifacts

## Verification

### Validate SBOM

```bash
# Install validator
pip install cyclonedx-python-lib

# Validate JSON
python -c "from cyclonedx.model import Bom; import json; Bom.from_json(json.load(open('sbom.json')))"
```

### View SBOM Contents

```bash
# Pretty print JSON
cat sbom/sbom.json | python -m json.tool | less

# Count dependencies
cat sbom/sbom.json | python -c "import json, sys; print(len(json.load(sys.stdin)['components']))"
```

## Release Process

When creating a release:

1. **Pre-release**: Generate SBOM manually or wait for CI
2. **Release**: CI automatically generates and attaches SBOM
3. **Post-release**: Verify SBOM is attached to release artifacts

## Security Scanning

SBOM files can be used with security scanners:

```bash
# Example: Scan with Snyk (if configured)
snyk test --file=sbom/sbom.json

# Example: Upload to Dependency-Track (if configured)
curl -X POST "https://dependency-track.example.com/api/v1/bom" \
  -H "X-Api-Key: YOUR_API_KEY" \
  -F "bom=@sbom/sbom.json"
```

## Maintenance

- **Update frequency**: SBOM regenerated on every release
- **Manual updates**: Run before major dependency changes
- **Validation**: Validate before committing SBOM files

## References

- [CycloneDX Specification](https://cyclonedx.org/specification/overview/)
- [CISA SBOM Requirements](https://www.cisa.gov/sbom)
- [GitHub Dependency Graph](https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-the-dependency-graph)
