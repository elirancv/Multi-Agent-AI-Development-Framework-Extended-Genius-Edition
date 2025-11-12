# Rollback Plan for v1.0.0

## Quick Rollback Steps

If critical issues are discovered after release:

### 1. Immediate Hotfix (15 minutes)

```bash
# Identify the problematic commit
git log --oneline -5

# Revert the commit
git revert <commit_sha>

# Create hotfix tag
git tag v1.0.1
git push origin main --tags
```

### 2. Create Hotfix Release

- Go to GitHub → Releases → Draft new release
- Tag: `v1.0.1`
- Title: `Hotfix v1.0.1`
- Description: Brief explanation of the fix

### 3. Communication

- Update release notes with hotfix details
- Notify users if breaking change occurred (should not happen in 1.0.x)
- Document in CHANGELOG.md

## Compatibility Guarantees

**For 1.0.x series:**
- ✅ No breaking changes to CLI flags
- ✅ No breaking changes to Policy schema
- ✅ No breaking changes to Agent/Advisor contracts
- ✅ Backward compatible checkpoint formats

**If breaking change is absolutely necessary:**
- Document in CHANGELOG as "BREAKING"
- Provide migration guide
- Consider bumping to 1.1.0 instead

## Monitoring Post-Release

### First 24 Hours
- [ ] Monitor GitHub Issues for critical bugs
- [ ] Check CI/CD status (all tests passing)
- [ ] Verify nightly hard tests run successfully
- [ ] Check retention weekly job schedule

### First Week
- [ ] Review KPI metrics from nightly tests
- [ ] Check artifact cleanup reports
- [ ] Monitor error rates and timeouts
- [ ] Collect user feedback

### First Month
- [ ] Track adoption metrics
- [ ] Review performance trends
- [ ] Plan v1.1 features based on feedback

## Emergency Contacts

- **Critical Bugs**: Open GitHub Issue with `[CRITICAL]` prefix
- **Security Issues**: See [SECURITY.md](../SECURITY.md)
- **Breaking Changes**: Discuss in GitHub Discussions before implementing

## Prevention

To minimize rollback risk:

1. **Pre-release**: Run all Go/No-Go checks
2. **Testing**: Full smoke test suite passes
3. **Documentation**: All features documented
4. **Compatibility**: Verify backward compatibility
5. **Monitoring**: Set up alerts for critical metrics

---

**Remember**: v1.0.x is a stable release series. Breaking changes should be deferred to v1.1.0.

