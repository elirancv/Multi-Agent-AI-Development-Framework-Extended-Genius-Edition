#!/usr/bin/env bash

set -euo pipefail

# Post-release version bump script
# Bumps version to next dev version after release

CURRENT_VERSION="${1:-1.0.0}"
NEXT_VERSION="${2:-1.0.1-dev}"

echo "Bumping version from $CURRENT_VERSION to $NEXT_VERSION..."

# Update src/__init__.py
if [ -f "src/__init__.py" ]; then
    sed -i.bak "s/__version__ = \"$CURRENT_VERSION\"/__version__ = \"$NEXT_VERSION\"/" src/__init__.py
    rm -f src/__init__.py.bak
    echo "✅ Updated src/__init__.py"
fi

# Update pyproject.toml
if [ -f "pyproject.toml" ]; then
    sed -i.bak "s/version = \"$CURRENT_VERSION\"/version = \"$NEXT_VERSION\"/" pyproject.toml
    rm -f pyproject.toml.bak
    echo "✅ Updated pyproject.toml"
fi

# Verify
echo ""
echo "Verifying version bump:"
python -c "from src import __version__; print(f'Version: {__version__}')"

echo ""
echo "✅ Version bumped to $NEXT_VERSION"
echo ""
echo "Next steps:"
echo "  git add -A"
echo "  git commit -m 'chore: bump version to $NEXT_VERSION'"
echo "  git push"
