---
name: plan
description: Use before any non-trivial change (new feature, refactor, multi-file change) to clarify requirements and write an implementation plan. Don't use for one-line bug fixes or when an approved plan already exists.
---

# Plan Workflow

A disciplined two-phase workflow for planning changes before writing code.

## Phase 1: Clarify & Discover

1. **Review Rules**: Read [AGENTS.md](../../../AGENTS.md). Restate the user's goal in 2 concise lines and explicitly list your initial assumptions.
2. **Explore Codebase**: Call `invoke_subagent scout` to locate all affected files, direct callers, dependencies, and relevant existing tests.
3. **Resolve Ambiguities**: If requirements are underspecified or architectural decisions are unmade, ask the user at most 3 questions. Ask **only** questions whose answers materially change the technical design. If no questions are needed, state your assumptions clearly and proceed.

## Phase 2: Implementation Plan

4. **Document Plan**: Create `docs/plans/<slug>.md` with the following structure:
   - **Goal & Scope**: What problem this solves and explicit non-goals.
   - **Affected Files & Symbols**: Complete list of files to modify or create.
   - **Numbered Steps**: Small, sequentially verifiable execution increments.
   - **Test Strategy**: Tests to add (for features) or existing tests to run.
   - **Ponytail Check**: Verification that no unnecessary abstractions or external dependencies are introduced.
   - **Risks & Rollback Plan**: Key failure modes and how to revert.

5. **Approval Gate**: **STOP**. Make **ZERO** code edits. Present the plan to the user and wait for explicit approval before invoking any implementation workflows.
