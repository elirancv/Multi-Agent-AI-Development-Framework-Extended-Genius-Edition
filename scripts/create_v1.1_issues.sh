#!/usr/bin/env bash

set -euo pipefail

# Create v1.1 milestone and issues via GitHub CLI
# Requires: gh CLI installed and authenticated
# Usage: ./scripts/create_v1.1_issues.sh

MILESTONE="v1.1.0"

echo "Creating v1.1.0 milestone and issues..."
echo ""

# Create milestone
echo "[1/6] Creating milestone..."
gh milestone create "$MILESTONE" -d "See docs/V1.1_ROADMAP.md" || echo "Milestone may already exist"

# Issue 1: Promote multiagent new to GA
echo "[2/6] Creating issue: Promote multiagent new to GA..."
gh issue create \
  -t "[v1.1] Promote multiagent new from preview to GA" \
  -b "See .github/ISSUES/v1.1-detailed-issues.md#issue-1-promote-multiagent-new-to-ga" \
  -l "enhancement,v1.1,feature,cli" \
  -m "$MILESTONE" || echo "Issue may already exist"

# Issue 2: Pipelines Gallery
echo "[3/6] Creating issue: Pipelines Gallery..."
gh issue create \
  -t "[v1.1] Create Pipelines Gallery with 5 Reference Examples" \
  -b "See .github/ISSUES/v1.1-detailed-issues.md#issue-2-pipelines-gallery" \
  -l "enhancement,v1.1,gallery,documentation,examples" \
  -m "$MILESTONE" || echo "Issue may already exist"

# Issue 3: Plugin API Tests
echo "[4/6] Creating issue: Plugin API Tests..."
gh issue create \
  -t "[v1.1] Add External Test Plugin for CI Validation" \
  -b "See .github/ISSUES/v1.1-detailed-issues.md#issue-3-plugin-api-tests" \
  -l "enhancement,v1.1,plugin-api,test,ci" \
  -m "$MILESTONE" || echo "Issue may already exist"

# Issue 4: PyPI Publishing
echo "[5/6] Creating issue: PyPI Publishing..."
gh issue create \
  -t "[v1.1] Publish to PyPI" \
  -b "See .github/ISSUES/v1.1-detailed-issues.md#issue-4-pypi-publishing" \
  -l "enhancement,v1.1,pypi,release" \
  -m "$MILESTONE" || echo "Issue may already exist"

# Issue 5: Artifact Retention Policy v2
echo "[6/6] Creating issue: Artifact Retention Policy v2..."
gh issue create \
  -t "[v1.1] Enhanced Artifact Retention Policy" \
  -b "See .github/ISSUES/v1.1-detailed-issues.md#issue-5-artifact-retention-policy-v2" \
  -l "enhancement,v1.1,feature,retention" \
  -m "$MILESTONE" || echo "Issue may already exist"

echo ""
echo "✅ Milestone and issues created!"
echo ""
echo "View milestone:"
echo "  gh milestone view $MILESTONE"
echo ""
echo "List issues:"
echo "  gh issue list -m $MILESTONE"

