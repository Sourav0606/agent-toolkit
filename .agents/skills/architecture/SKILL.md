---
name: architecture
description: Use when designing new subsystems, evaluating major refactors, establishing cross-module boundaries, or writing Architecture Decision Records (ADRs).
---

# Architecture Workflow

A structured procedure for high-level system design, boundary enforcement, and ADR creation prior to planning implementation.

## Phase 1: Boundary & Dependency Discovery
1. **Read Guidelines**: Review [AGENTS.md](../../../AGENTS.md) for constraints and the Ponytail rule (minimum necessary code and abstractions).
2. **Inspect Call Graph & Module Boundaries**:
   - Call `invoke_subagent arch-auditor` with the proposed architectural change or new subsystem.
   - Map existing packages, inbound/outbound dependencies, and layer responsibilities in `src/`.
   - Identify risk areas: circular dependencies, abstraction leaks, or unnecessary external packages.

## Phase 2: Architectural Decision Record (ADR)
3. If introducing a new pattern, external dependency, or subsystem boundary, write an ADR at `docs/adr/NNNN-<slug>.md` using the standard format ([docs/adr/template.md](../../../docs/adr/template.md)):
   - **Status**: Proposed | Accepted | Rejected | Superseded
   - **Context**: Problem statement, constraints, and driving technical requirements.
   - **Decision**: The architectural choice, component contracts, and public APIs.
   - **Ponytail Verification**: Explicit justification for why existing modules / stdlib cannot fulfill this need.
   - **Consequences**: Positive and negative trade-offs (performance, testability, complexity).
   - **Component Diagram**: Mermaid diagram of module interactions and data flow.

## Phase 3: Architecture Approval Gate
4. **STOP**: Make **ZERO** code edits.
5. Present the ADR and boundary analysis to the user.
6. Await explicit approval before invoking the [plan](../plan/SKILL.md) skill to transition from architecture to tactical execution.
