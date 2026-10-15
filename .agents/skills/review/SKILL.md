---
name: review
description: Use to review a diff, branch, or file for bugs, security vulnerabilities, edge cases, and maintainability before merging. Read-only. Don't use to implement fixes.
---

# Code Review Workflow

A structured procedure for reviewing proposed code changes prior to merge.

## Steps

1. **Obtain Diff**:
   - Run `git diff` against the target branch or review the uncommitted working tree diff.
   - Run the existing test suite once (`python3 -m pytest -q --tb=short`) to verify baseline test status.

2. **Invoke Reviewer Subagent**:
   - Call `invoke_subagent reviewer` passing:
     - The diff and list of changed files.
     - The conventions specified in [AGENTS.md](../../../AGENTS.md).
     - Context on whether tests passed or failed.

3. **Verify Findings**:
   - For each finding reported by `reviewer`, independently check using `view_file` that the quoted code line exists and matches the line in the target file.
   - Discard any finding that cannot be verified against the file contents.

4. **Verdict Summary**:
   - Conclude the review with an explicit overall status:
     - **`BLOCK`**: 1 or more Blocker findings (crashes, regressions, severe security flaws).
     - **`CHANGES_REQUESTED`**: Major bugs or missing edge-case handling.
     - **`APPROVE`**: Clean diff or only minor/optional notes.
   - **Never edit files**. Present findings to the user and wait.
