---
name: orchestrator
description: Master pipeline coordinator. Maps user requests to the optimal sequence of skills and subagents across full-stack feature development, UI/UX engineering, performance optimization, bug-fixing, and production shipping.
---

# Master Orchestration Playbook

A structured decision and routing engine that sequences the repository's 28 skills and 10 subagents into clean, deterministic execution pipelines.

The governing rule: **Avoid bureaucratic wrapper bloat.** The main agent coordinates the workflow directly; subagents are invoked only for isolated research (`scout`), surgical editing (`fixer`), test authoring (`test-writer`), or read-only governance (`reviewer`, `security-auditor`).

---

## 1. Intent Classification Matrix

Identify the user's intent and select the matching pipeline:

| User Intent / Trigger | Primary Pipeline | Key Skills Chained | Subagents Deployed |
| :--- | :--- | :--- | :--- |
| **"Build X"**, **"Add an endpoint"**, **"New feature"** | **1. Full-Stack Feature** | `interview` → `architecture` → `plan` → `test-driven-development` → `clean-architecture` → `review` → `wiki` | `interviewer`, `test-writer`, `fixer`, `reviewer` |
| **"Build UI"**, **"Make it modern / animated"**, **"Mobile responsive"** | **2. Frontend Experience** | `frontend-design` → `frontend-ui-engineering` → `framer-motion` → `forms-and-validation` → `client-data-fetching` → `browser-testing` | `frontend-designer`, `fixer` |
| **"Fix this bug"**, **"Test is failing"**, **"Unexpected error"** | **3. Bounded Bug-Fix** | `debugging-and-error-recovery` → `bugfix-workflow` → `ponytail` → `doubt-driven-development` | `scout`, `fixer`, `test-auditor` |
| **"This is slow"**, **"Optimize query"**, **"Clean up code"** | **4. Performance & Refactor** | `performance-optimization` → `query-optimization` → `code-simplification` → `doubt-driven-development` | `scout`, `fixer`, `reviewer` |
| **"Ready to ship"**, **"Deploy"**, **"Run migration"** | **5. Production Release** | `security-audit` → `db-migration-safety` → `definition-of-done` → `git-workflow-and-versioning` | `security-auditor`, `reviewer` |

---

## 2. The 5 Pipeline Definitions

### Pipeline 1: Full-Stack Feature Delivery
```
[interview] ──> [architecture / plan] ──[GATE]──> [TDD] ──> [clean-arch / fixer] ──> [review / security] ──> [wiki]
```
1. **Clarify**: If requirements are underspecified, invoke `interview` (`interview-me`) with attached hypotheses until confidence is $\ge 95\%$.
2. **Design & Plan**: If cross-module boundaries or new patterns are introduced, write an ADR (`architecture`); generate step-by-step increments (`plan`).
3. **Approval Gate**: **STOP**. Obtain explicit user sign-off on the plan before writing code.
4. **Test-First**: Delegate to `test-writer` to create failing tests (`test-driven-development`). Verify tests fail on unmodified code.
5. **Implement**: Delegate to `fixer` to write minimal code adhering to `clean-architecture` and the `ponytail` rule.
6. **Verify & Audit**: Delegate diff review to `reviewer` and `security-auditor`.
7. **Document**: Synchronize living documentation via `wiki`.

---

### Pipeline 2: Frontend Experience & UI/UX
```
[frontend-design] ──> [ui-engineering] ──> [framer-motion] ──> [forms / data-fetching] ──> [devtools-mcp]
```
1. **Aesthetic Tokens**: Establish custom properties (HSL/OKLCH palette, type scales) using `frontend-design`. Eliminate generic AI tells.
2. **Responsive Hierarchy**: Build mobile-first layouts (320px to 1440px) using `frontend-ui-engineering` and `accessibility-checklist.md`.
3. **Motion Polish**: Add physics-based springs, hover/tap gestures, and layout morphs (`layoutId`) using `framer-motion`.
4. **Resilient Inputs & Network**: Wire up accessible Zod validation (`forms-and-validation`) and race-condition prevention via `AbortController` (`client-data-fetching`).
5. **Live Verification**: Open the dev server and inspect computed styles, console logs, and network waterfalls using `browser-testing-with-devtools` via Chrome DevTools MCP.

---

### Pipeline 3: Bounded Bug-Fix & Error Recovery
```
[scout] ──> [debugging-and-error-recovery] ──> [fixer] ──> [test-auditor] ──> [doubt-driven-dev]
```
1. **Locate**: Delegate to `scout` to find symbols, direct callers, and baseline test status without guessing.
2. **Isolate**: Formulate a hypothesis and minimal reproduction using `debugging-and-error-recovery`.
3. **Surgical Fix**: Delegate to `fixer` to apply the minimal root-cause edit. Never touch unrelated lines or format adjacent code (`ponytail`).
4. **Deterministic Run**: Execute the test runner (`run_command`). If it fails, delegate to `test-auditor` to classify the failure (`impl_bug` vs `test_bug`). Cap attempts at 3.
5. **Adversarial Check**: Subject the fix to `doubt-driven-development` to ensure no silent regressions or edge cases were introduced.

---

### Pipeline 4: Performance & Refactoring
```
[performance-optimization] ──> [query-optimization] ──> [code-simplification] ──> [reviewer]
```
1. **Measure First**: Profile TTFB, Core Web Vitals (LCP, INP, CLS), or server latency using `performance-optimization` and `performance-checklist.md`. Never optimize without metrics.
2. **Database Tuning**: If database-bound, run `EXPLAIN (ANALYZE, BUFFERS)` via `query-optimization`. Fix N+1 queries, add composite indexes (equality first, range second), or tune connection pools.
3. **Simplify**: Strip dead code paths, flatten nested conditionals, and reduce cyclomatic complexity using `code-simplification`.
4. **Adversarial Diff Review**: Call `reviewer` with `doubt-driven-development` to prove performance improved without altering business logic contracts.

---

### Pipeline 5: Production Shipping & Release
```
[security-audit] ──> [db-migration-safety] ──> [definition-of-done] ──> [git-workflow]
```
1. **Security Audit**: Delegate taint analysis and sink verification to `security-auditor`. Check against `security-checklist.md` and `security_guidance_patterns.py`.
2. **Migration Safety**: If migrations exist, verify zero-downtime rules (`db-migration-safety`): lock timeouts set, non-blocking indexes (`CONCURRENTLY`), and expand-contract compatibility.
3. **Quality Gate**: Verify against `definition-of-done.md`.
4. **Ship**: Create atomic conventional commits and semantic version tags using `git-workflow-and-versioning`.

---

## 3. Core Invariants for the Orchestrator

1. **The Ponytail Rule Overrides Everything**: The shortest, simplest correct solution wins. Do not build an entire pipeline when a single one-line fix solves the task.
2. **Never Skip Approval Gates**: Any multi-file refactor, architecture change, or schema migration MUST halt for user approval before modifying code.
3. **Subagent Boundaries are Absolute**:
   - Auditing subagents (`reviewer`, `security-auditor`, `arch-auditor`, `doc-auditor`) must NEVER receive edit tools.
   - Execution subagents (`fixer`, `test-writer`) must only touch designated targets.
