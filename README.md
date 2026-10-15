# Full-Stack AI Coding Agent Toolkit

A universal, production-grade pair-programming and engineering agent toolkit. Equipped with **29 skills**, **10 permission-bounded subagents**, **7 industry reference checklists**, and **Chrome DevTools MCP integration**.

---

## Architecture Overview

```
                               ┌────────────────────────────────┐
                               │           AGENTS.md            │
                               │  (Ponytail & Full-Stack Rules) │
                               └───────────────┬────────────────┘
                                               │
                                               ▼
                               ┌────────────────────────────────┐
                               │       MASTER ORCHESTRATOR      │
                               │   (.agents/skills/orchestrator)│
                               └───────────────┬────────────────┘
                                               │
           ┌───────────────────────┬───────────┴───────────┬───────────────────────┐
           ▼                       ▼                       ▼                       ▼
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│  Frontend & UI/UX   │ │   Backend & APIs    │ │ Databases & Data    │ │  Verification & QA  │
│ • frontend-design   │ │ • api-design        │ │ • db-migration      │ │ • test-driven-dev   │
│ • ui-engineering    │ │ • clean-arch        │ │ • query-opt         │ │ • e2e-playwright    │
│ • framer-motion     │ │ • resilience        │ │ • perf-optimization │ │ • doubt-driven-dev  │
│ • forms-validation  │ │ • bugfix-workflow   │ │ • devtools-mcp      │ │ • security-audit    │
│ • data-fetching     │ │ • feature-workflow  │ │ • wiki / adr        │ │ • code-simplify     │
└─────────────────────┘ └─────────────────────┘ └─────────────────────┘ └─────────────────────┘
```

---

## The 5 Master Execution Pipelines

The agent routes incoming prompts through deterministic pipeline playbooks defined in [`orchestrator`](file:///.agents/skills/orchestrator/SKILL.md):

1. **Full-Stack Feature Pipeline**:
   `interview` (95% confidence stop) $\rightarrow$ `architecture` (ADR) $\rightarrow$ `plan` (**Approval Gate**) $\rightarrow$ `test-driven-development` $\rightarrow$ `clean-architecture` $\rightarrow$ `review` $\rightarrow$ `wiki`
2. **Frontend Experience Pipeline**:
   `frontend-design` (tokens) $\rightarrow$ `frontend-ui-engineering` (responsive components) $\rightarrow$ `framer-motion` (springs & layout morphs) $\rightarrow$ `forms-and-validation` $\rightarrow$ `client-data-fetching` $\rightarrow$ `browser-testing-with-devtools` (live Chrome inspection)
3. **Bounded Bug-Fix Pipeline**:
   `scout` (locate) $\rightarrow$ `debugging-and-error-recovery` (isolate) $\rightarrow$ `fixer` (surgical edit) $\rightarrow$ `test-auditor` (classify) $\rightarrow$ `doubt-driven-development` (verify)
4. **Performance & Refactor Pipeline**:
   `performance-optimization` (measure first) $\rightarrow$ `query-optimization` (`EXPLAIN ANALYZE`) $\rightarrow$ `code-simplification` (clean complexity) $\rightarrow$ `reviewer`
5. **Production Release Pipeline**:
   `security-audit` (taint analysis) $\rightarrow$ `db-migration-safety` (non-blocking DDL) $\rightarrow$ `definition-of-done` $\rightarrow$ `git-workflow-and-versioning`

---

## Subagents & Permission Boundaries

Located in [`.agents/agents/`](file:///.agents/agents/):

| Subagent | Access Level | Permitted Tools | Core Responsibility |
| :--- | :--- | :--- | :--- |
| **`scout`** | Read-Only | `view_file`, `grep_search`, `list_dir` | Code exploration, finding symbols, tracing callers and DB queries without polluting context. |
| **`reviewer`** | Read-Only | `view_file`, `grep_search` | Evaluates diffs for bugs, edge cases, doubt-driven review, and Ponytail simplicity. |
| **`security-auditor`**| Read-Only | `view_file`, `grep_search` | Deep taint-tracking, SSRF, injection vectors, and DB migration lock safety. |
| **`arch-auditor`** | Read-Only | `view_file`, `grep_search`, `list_dir` | Reviews system boundaries, cyclic dependencies, and Architecture Decision Records (ADRs). |
| **`doc-auditor`** | Read-Only | `view_file`, `grep_search`, `list_dir` | Verifies documentation and wikis against live code to prevent documentation drift. |
| **`test-auditor`** | Read-Only | `view_file`, `grep_search` | Analyzes test output to classify root causes (`impl_bug`, `test_bug`, `env_issue`). |
| **`interviewer`** | Read-Only | `view_file`, `grep_search`, `list_dir` | Conducts pre-build requirements interviews with multiple-choice questions. |
| **`frontend-designer`**| Read-Only | `view_file`, `grep_search`, `list_dir` | Generates UI design tokens, component hierarchies, and WCAG AA accessibility specs. |
| **`test-writer`** | Write Tests | `view_file`, `grep_search`, `write_to_file` | Creates new unit tests and Playwright E2E browser tests without editing source code. |
| **`fixer`** | Surgical Edits | `view_file`, `replace_file_content` | Writes minimal, high-precision code fixes adhering to the Ponytail rule. |

---

## Reference Checklists

Located in [`.agents/references/`](file:///.agents/references/):

* **[accessibility-checklist.md](file:///.agents/references/accessibility-checklist.md)**: WCAG 2.1 AA, keyboard focus, ARIA live regions.
* **[definition-of-done.md](file:///.agents/references/definition-of-done.md)**: Production readiness verification standards.
* **[observability-checklist.md](file:///.agents/references/observability-checklist.md)**: Structured JSON logging, tracing, and metric instrumentation.
* **[orchestration-patterns.md](file:///.agents/references/orchestration-patterns.md)**: Agent coordination principles and anti-patterns.
* **[performance-checklist.md](file:///.agents/references/performance-checklist.md)**: Core Web Vitals (LCP, INP, CLS), TTFB, and database bottlenecks.
* **[security-checklist.md](file:///.agents/references/security-checklist.md)**: STRIDE threat modeling, OWASP, and authentication.
* **[testing-patterns.md](file:///.agents/references/testing-patterns.md)**: Unit, integration, and mocking patterns.

---

## Toolkit Validation & Health Check

Run the self-test script anytime to verify that all 29 skills, 10 subagents, and configurations are completely valid:

```bash
python3 .agents/scripts/validate_toolkit.py
```

---

## Starting a New Project

When you are ready to build an application, prompt the agent with your goal:

* **Frontend**: *"Initialize a Next.js (or Vite) app with responsive dark mode and Framer Motion animations."*
* **Full-Stack**: *"Build a FastAPI backend with PostgreSQL and a React dashboard."*
* **Bug Fix**: *"Fix the race condition in the search input."*

The master **`orchestrator`** will automatically select the right pipeline, deploy the proper subagents, and enforce the Ponytail simplicity standard.

---

## Using in Other Repositories & Apps

### 1. As a GitHub Template (New Projects)
1. Go to repository **Settings** on GitHub and enable **☑ Template repository**.
2. Click **Use this template** → **Create a new repository** for each new project.

### 2. Fast Drop-In (Existing Projects)
Run this inside any existing project folder to inject the entire toolkit:
```bash
git clone --depth 1 https://github.com/Sourav0606/agent-toolkit.git /tmp/toolkit
cp -r /tmp/toolkit/.agents ./
cp /tmp/toolkit/AGENTS.md ./
rm -rf /tmp/toolkit
```

### 3. Git Submodule (Auto-Updating)
Keep your project synchronized with upstream toolkit improvements:
```bash
git submodule add https://github.com/Sourav0606/agent-toolkit.git .agent-toolkit
ln -s .agent-toolkit/.agents .agents
ln -s .agent-toolkit/AGENTS.md AGENTS.md

# Update anytime:
git submodule update --remote
```

### 4. Global Machine Install (Active Everywhere)
Make all skills available across all projects on your machine without copying files:
```bash
# Global Antigravity config
mkdir -p ~/.gemini/config/skills ~/.gemini/config/agents
cp -r .agents/skills/* ~/.gemini/config/skills/
cp -r .agents/agents/* ~/.gemini/config/agents/

# Global Claude Code config
mkdir -p ~/.claude/skills
cp -r .agents/skills/* ~/.claude/skills/
```
