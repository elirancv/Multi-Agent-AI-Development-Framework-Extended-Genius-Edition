# GitHub Branch and Tag Protection Setup

This guide explains how to set up branch and tag protection rules for the repository.

## Branch Protection (main)

### Required Settings

1. **Navigate to**: Repository Settings → Branches → Add rule
2. **Branch name pattern**: `main`
3. **Enable the following**:

#### ✅ Required Settings

- **Require a pull request before merging**
  - Required number of approvals: `1` (or more)
  - Dismiss stale pull request approvals when new commits are pushed
  - Require review from Code Owners (if CODEOWNERS file exists)

- **Require status checks to pass before merging**
  - Require branches to be up to date before merging
  - Required status checks:
    - `CI` (or your main CI workflow)
    - `Smoke Tests`
    - `Tests` (if separate)

- **Require conversation resolution before merging**

- **Do not allow bypassing the above settings** (for administrators)

#### 🔒 Additional Security (Optional)

- **Require signed commits** (if using GPG signing)
  - This requires all commits to be signed with GPG

- **Require linear history**
  - Prevents merge commits, enforces rebase-only workflow

- **Include administrators**
  - Applies rules to repository administrators

### Recommended Configuration

```
Branch name pattern: main

✅ Require a pull request before merging
   ✅ Require approvals: 1
   ✅ Dismiss stale pull request approvals when new commits are pushed
   ✅ Require review from Code Owners

✅ Require status checks to pass before merging
   ✅ Require branches to be up to date before merging
   Required checks:
   - CI
   - Smoke Tests
   - Tests

✅ Require conversation resolution before merging

✅ Do not allow bypassing the above settings

✅ Include administrators
```

## Tag Protection (v*)

### Required Settings

1. **Navigate to**: Repository Settings → Tags → Add rule
2. **Tag name pattern**: `v*`
3. **Enable the following**:

#### ✅ Required Settings

- **Restrict creation of matching tags**
  - Only users with write access can create tags matching this pattern

- **Restrict deletion of matching tags**
  - Prevents accidental or malicious tag deletion

- **Restrict update of matching tags**
  - Prevents overwriting existing tags

### Recommended Configuration

```
Tag name pattern: v*

✅ Restrict creation of matching tags
   ✅ Only users with write access

✅ Restrict deletion of matching tags

✅ Restrict update of matching tags
```

## GPG Commit Signing (Optional)

If you want to require signed commits:

1. **Set up GPG signing**:
   ```bash
   # Generate GPG key (if needed)
   gpg --full-generate-key

   # Add to Git config
   git config --global user.signingkey YOUR_KEY_ID
   git config --global commit.gpgsign true
   ```

2. **Add GPG key to GitHub**:
   - Settings → SSH and GPG keys → New GPG key
   - Paste your public key: `gpg --armor --export YOUR_KEY_ID`

3. **Enable in Branch Protection**:
   - Check "Require signed commits" in branch protection rules

## Verification

After setting up protection:

1. **Test Branch Protection**:
   - Try to push directly to `main` (should fail)
   - Create a PR and verify checks are required

2. **Test Tag Protection**:
   - Try to delete a tag: `git push origin :refs/tags/v1.0.0` (should fail)
   - Try to overwrite a tag (should fail)

## References

- [GitHub Branch Protection](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches)
- [GitHub Tag Protection](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/configuring-tag-protection-rules)
- [GPG Commit Signing](https://docs.github.com/en/authentication/managing-commit-signature-verification)
