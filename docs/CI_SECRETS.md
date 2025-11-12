# CI Secrets Configuration

Quick reference for required GitHub Actions secrets.

## Required Secrets

### Codecov Token (Optional)

**When needed**: Private repositories only (public repos don't need it)

**Name**: `CODECOV_TOKEN`

**How to get**:
1. Go to https://codecov.io
2. Sign in with GitHub
3. Add repository
4. Copy token from repository settings

**Set in GitHub**:
1. Repository Settings → Secrets and variables → Actions
2. New repository secret
3. Name: `CODECOV_TOKEN`
4. Value: Your token

### PyPI Token (v1.1+)

**When needed**: When publishing to PyPI

**Name**: `PYPI_TOKEN`

**How to get**:
1. Go to https://pypi.org/manage/account/token/
2. Create API token
3. Scope: Entire account (or specific project)
4. Copy token (starts with `pypi-`)

**Set in GitHub**:
1. Repository Settings → Secrets and variables → Actions
2. New repository secret
3. Name: `PYPI_TOKEN`
4. Value: `pypi-...` (your token)

**Usage in workflow**:
```yaml
env:
  TWINE_USERNAME: __token__
  TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
```

### GPG Signing Key (Optional)

**When needed**: If enforcing signed commits/tags

**Name**: Not a secret, but GPG key must be configured

**How to set up**:
1. Generate GPG key: `gpg --full-generate-key`
2. Export public key: `gpg --armor --export YOUR_KEY_ID`
3. Add to GitHub: Settings → SSH and GPG keys → New GPG key
4. Configure Git: `git config --global user.signingkey YOUR_KEY_ID`

**For CI**:
- Add private key as secret: `GPG_PRIVATE_KEY`
- Import in workflow: `gpg --import <(echo "${{ secrets.GPG_PRIVATE_KEY }}")`

## Verification

### Check Secrets Exist

```bash
# Via GitHub CLI (if installed)
gh secret list

# Or check in GitHub UI:
# Repository Settings → Secrets and variables → Actions
```

### Test Codecov

After setting `CODECOV_TOKEN`, push a commit and check:
- Codecov workflow runs
- Coverage report appears on codecov.io

### Test PyPI (v1.1+)

After setting `PYPI_TOKEN`, create a test release:
- Workflow should upload to PyPI
- Check PyPI for your package

## Security Best Practices

1. **Rotate tokens regularly** (every 90 days)
2. **Use least privilege** (project-specific tokens when possible)
3. **Never commit tokens** to repository
4. **Use environment-specific secrets** (if using multiple environments)

## Troubleshooting

### Codecov not uploading

- Check `CODECOV_TOKEN` is set (if private repo)
- Verify workflow has `contents: read` permission
- Check Codecov workflow logs

### PyPI upload fails

- Verify `PYPI_TOKEN` format (`pypi-...`)
- Check token hasn't expired
- Verify package name is available on PyPI

### GPG signing fails

- Verify GPG key is added to GitHub account
- Check Git config has signing key set
- Verify private key is correctly imported in CI

## See Also

- [GitHub Secrets Documentation](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Codecov Setup](https://docs.codecov.com/docs)
- [PyPI API Tokens](https://pypi.org/help/#apitoken)
