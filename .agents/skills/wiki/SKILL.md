---
name: wiki
description: Use when creating, syncing, or auditing documentation, wikis, API guides, and architecture overviews against the current codebase.
---

# Wiki & Documentation Workflow

A documentation workflow ensuring project wikis, guides, and architectural overviews stay strictly synchronized with code reality.

## Phase 1: Source Verification (Code as Truth)
1. **Identify Documentation Target**: Locate the target document in `docs/` or `README.md`.
2. **Audit Claims Against Code**:
   - Call `invoke_subagent doc-auditor` with the doc path and target modules.
   - Validate every function signature, CLI argument, config key, and schema against active code in `src/`.
   - Never document unverified or hallucinated parameters.

## Phase 2: Documentation Synthesis
3. **Draft or Update**: Create or edit documents under `docs/wiki/` (e.g. `docs/wiki/<topic>.md`):
   - **Overview**: Core responsibility of the component and when to use it.
   - **Key Symbols & Entry Points**: Clickable links to primary functions/classes.
   - **Usage Examples**: Copy-pasteable snippets verified against existing tests in `tests/`.
   - **Architecture Diagram**: Mermaid sequence or class diagram if non-trivial.
4. **Maintain Index**: Ensure `docs/wiki/README.md` or table of contents references new pages.

## Phase 3: Integrity & Link Verification
5. Verify all relative markdown links and code paths exist.
6. Verify no secrets or sensitive environment variables are included in examples.
7. Present the doc diff or new page to the user.
