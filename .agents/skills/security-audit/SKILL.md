---
name: security-audit
description: Use to perform a thorough, read-only security audit of the repository, diff, or specific module. Identifies injection, authentication bypasses, path traversal, and secret exposure. Does not edit code.
---

# Security Audit Workflow

A three-layer security inspection workflow inspired by defense-in-depth principles:
1. Cheap lexical scans for suspicious sinks and dangerous primitives.
2. In-depth taint analysis by the `security-auditor` subagent.
3. Verification and secret masking before reporting.

## Steps

1. **Lead Generation (Cheap Lexical Scan)**:
   - Run grep searches for high-risk patterns:
     - Code execution: `eval\(`, `exec\(`, `pickle\.loads`
     - Command injection: `subprocess\.`, `os\.system`, `shell=True`
     - SQL injection: `execute\(f["']`, `cursor\.execute\(.*%`
     - File system: `open\(.*request`, `os\.path\.join\(.*filename`
     - Cryptography: `md5`, `sha1`, `Crypto\.`

2. **Invoke Security Auditor**:
   - Call `invoke_subagent security-auditor` with the leads found and candidate files.
   - The auditor verifies whether user input can reach any of these sinks and checks for missing authorization or validation.

3. **Re-Check & Sanitize Findings**:
   - For every reported vulnerability, use `view_file` to confirm the quoted line exists.
   - Confirm the taint path: Is the source actually untrusted input, or is it internal/hardcoded?
   - If secrets or tokens are present in the report, mask them (e.g. `sk-live-****`).

4. **Audit Report**:
   - Deliver findings ranked by severity (CRITICAL, HIGH, MEDIUM) with remediation steps.
   - **Never edit files**. Present the audit report to the user and wait.
