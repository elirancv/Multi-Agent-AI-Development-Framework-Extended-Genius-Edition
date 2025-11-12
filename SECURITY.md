# Security Policy

## Supported Versions

We currently support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.9.x   | :white_check_mark: |
| < 0.9.0 | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability, please follow these steps:

1. **Do not** open a public GitHub issue
2. Email security details to: [security@yourdomain.com] (replace with your actual security email)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Report

- Authentication/authorization bypasses
- Remote code execution (RCE)
- SQL injection or other injection vulnerabilities
- Cross-site scripting (XSS)
- Sensitive data exposure
- Denial of service (DoS) vulnerabilities
- Any other security-related issues

### What NOT to Report

- Issues that require physical access to the system
- Issues that require social engineering
- Issues that require already-compromised accounts
- Self-XSS (requires user interaction)
- Missing security headers without demonstrated impact

## Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity (typically 30-90 days)

## Security Best Practices

When using this system:

1. **Never commit secrets** to version control
2. **Use environment variables** for sensitive configuration
3. **Keep dependencies updated** (`pip install -r requirements.txt --upgrade`)
4. **Review pipeline YAML** before execution
5. **Limit network access** for agent execution
6. **Monitor event logs** for suspicious activity

## Disclosure Policy

- Vulnerabilities will be disclosed after a fix is available
- Credit will be given to reporters (unless requested otherwise)
- A CVE may be requested for significant vulnerabilities

## Security Updates

Security updates are released as patch versions (e.g., 0.9.1, 0.9.2). Always update to the latest patch version for security fixes.

## Contact

For security-related questions or concerns, contact: [security@yourdomain.com]

