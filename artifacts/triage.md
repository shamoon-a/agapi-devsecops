# SAST Triage Report

Total findings: 3
Configured minimum severity: CRITICAL

## Counts by Severity

| Severity | Count |
|---|---:|
| CRITICAL | 0 |
| HIGH | 2 |
| MEDIUM | 1 |
| LOW | 0 |
| INFO | 0 |

## Counts by Category

| Category | Count |
|---|---:|
| code-injection | 1 |
| command-injection | 1 |
| weak-cryptography | 1 |

## Top 5 Findings

1. **HIGH** - code-injection
   - Rule: `config.python-dangerous-eval`
   - Location: `agapi_app/example.py:5`
   - Message: Avoid eval() on potentially untrusted input.

2. **HIGH** - command-injection
   - Rule: `config.python-shell-true`
   - Location: `agapi_app/example.py:8`
   - Message: Avoid executing commands with shell=True.

3. **MEDIUM** - weak-cryptography
   - Rule: `config.python-md5`
   - Location: `agapi_app/example.py:11`
   - Message: MD5 is not suitable for security-sensitive hashing.

## Summary

0 finding(s) meet or exceed the `CRITICAL` threshold.
