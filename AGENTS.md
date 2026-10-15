# Engineering & Agent Guidelines

## 1. Project Philosophy & Core Rules
- **The Ponytail Rule**: Write the minimum code necessary to solve the task. The best code is the code you never wrote.
  - Before creating new abstractions, helper wheels, or external dependencies, reuse existing project functions or language standard library built-ins.
  - Avoid speculative generalizations, unrequested options, and wrapper bloat.
- **Surgical Changes**: Keep edits small and localized. Never reformat adjacent code or touch lines unrelated to the change.

## 2. Full-Stack Engineering Standards
- **Frontend & UI/UX**:
  - Follow intentional design principles (Anthropic): curated palettes (HSL/OKLCH), responsive typography rhythm, and WCAG AA accessibility. Avoid generic "AI tells".
  - Add snappy micro-interactions and smooth layout transitions using Motion/Framer Motion.
  - Build accessible forms with explicit label bindings, schema validation, and focus-on-error management.
- **Backend & APIs**:
  - Keep domain logic clean and decoupled from frameworks.
  - Use structured API patterns: idempotency keys on mutations, RFC 7807 error envelopes, and consistent pagination.
- **Databases**:
  - Follow zero-downtime migration standards (Expand-Contract pattern, non-blocking DDL).
  - Optimize queries with proper indexing (equality first, range second) and eliminate N+1 queries.

## 3. Verification & Testing
- **Test-First Discipline**: For new features or bug fixes, write the failing test first, verify failure, then write minimal implementation to turn it green.
- **Deterministic Proof**: Trust test runner exit codes and compiler/build output (`npm test`, `pytest`, `npm run build`), not assumptions.
- **Never Weaken Tests**: Never remove existing assertions or add skip/xfail markers to force a passing run.

## 4. Protected Paths & Secrets
- Never commit secrets, tokens, or credentials.
- Protected files: `.env*`, `.github/`, `.gitlab/`, and package lockfiles (`package-lock.json`, `poetry.lock`, etc.) require explicit user confirmation to modify.

## 5. Failure Escalation
- Maximum 3 fix attempts per task before stopping to report the exact blocker.
- If requirements are ambiguous or key context is missing, stop and interview the user rather than guessing.
