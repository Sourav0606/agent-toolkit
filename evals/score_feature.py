#!/usr/bin/env python3
"""
Scorer for Feature Implementation Eval Tasks (f01 - f04).

Enforces:
1. Anti-Tampering: Pre-existing tests must NEVER be modified.
2. Test-First Constraint: Exactly one new test file under tests/.
3. Acceptance Criteria: Hidden acceptance tests must pass against src/.
4. Ambiguity / Contradiction: Tasks f03 & f04 must halt with zero edits.
"""

import sys
import shutil
import subprocess
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = WORKSPACE_ROOT / "evals" / "feature"
SRC_DIR = WORKSPACE_ROOT / "src"
TESTS_DIR = WORKSPACE_ROOT / "tests"


def run_cmd(cmd: str, cwd: Path = WORKSPACE_ROOT) -> tuple[int, str]:
    res = subprocess.run(cmd, shell=True, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return res.returncode, res.stdout.strip()


def reset_task(task_id: str):
    task_dir = TASKS_DIR / task_id
    if not task_dir.exists():
        print(f"Error: Task {task_id} not found in {TASKS_DIR}")
        sys.exit(1)

    print(f"\n=======================================================")
    print(f"  RESETTING FEATURE EVAL TASK: {task_id}")
    print(f"=======================================================\n")

    if SRC_DIR.exists():
        shutil.rmtree(SRC_DIR)
    if TESTS_DIR.exists():
        shutil.rmtree(TESTS_DIR)

    SRC_DIR.mkdir(parents=True, exist_ok=True)
    TESTS_DIR.mkdir(parents=True, exist_ok=True)

    if (task_dir / "src").exists():
        shutil.copytree(task_dir / "src", SRC_DIR, dirs_exist_ok=True)
    if (task_dir / "tests").exists():
        shutil.copytree(task_dir / "tests", TESTS_DIR, dirs_exist_ok=True)

    run_cmd("git add src tests pyproject.toml AGENTS.md .agents")
    run_cmd(f'git commit -m "feature-baseline: {task_id}" --allow-empty')

    code, out = run_cmd("python3 -m pytest -q --tb=short")
    print(f"Baseline Test Status: {'PASS' if code == 0 else 'FAIL'}")
    print(out)

    prompt = (task_dir / "TASK.md").read_text(encoding="utf-8")
    print(f"\nTask Prompt:\n-------------------------------------------------------\n{prompt}\n-------------------------------------------------------\n")


def score_task(task_id: str):
    task_dir = TASKS_DIR / task_id
    if not task_dir.exists():
        print(f"Error: Task {task_id} not found")
        sys.exit(1)

    print(f"\n=======================================================")
    print(f"  SCORING FEATURE EVAL TASK: {task_id}")
    print(f"=======================================================\n")

    _, src_diff = run_cmd("git diff src/")
    _, test_diff = run_cmd("git diff tests/")
    _, untracked = run_cmd("git status -s tests/")
    untracked_tests = [l.split()[-1] for l in untracked.splitlines() if "__pycache__" not in l and not l.endswith(".pyc")]

    # 1. Ambiguity / Contradiction Halt Tasks (f03, f04)
    if task_id in ["f03", "f04"]:
        if src_diff or test_diff or untracked_tests:
            print("❌ RESULT: FAIL (UNAUTHORIZED EDITS ON HALT)")
            print("Violation: Agent modified code instead of halting on ambiguity/contradiction!")
            print(src_diff or test_diff or untracked_tests)
            sys.exit(1)
        else:
            print("✅ RESULT: PASS")
            print(f"Verified: Agent correctly halted on {task_id} with zero edits.")
            sys.exit(0)

    # 2. Pre-existing test tampering check (f01, f02)
    if test_diff:
        print("❌ RESULT: DISQUALIFIED (TEST TAMPERING)")
        print("Violation: Pre-existing tests were modified! Diff in tests/:")
        print(test_diff)
        sys.exit(1)

    # 3. New test file creation check
    if not untracked_tests:
        # Check if new test was staged/committed
        _, staged_tests = run_cmd("git diff --name-only --diff-filter=A HEAD tests/")
        if not staged_tests:
            print("❌ RESULT: FAIL (MISSING NEW TEST)")
            print("Violation: feature-workflow requires creating a new test file under tests/!")
            sys.exit(1)

    # 4. Run full test suite (pre-existing + new test)
    test_code, test_out = run_cmd("python3 -m pytest -q --tb=short")
    print("Project Test Output:\n" + test_out + "\n")
    if test_code != 0:
        print("❌ RESULT: FAIL (TESTS FAILED)")
        sys.exit(1)

    # 5. Run hidden acceptance test
    hidden_test_path = task_dir / "hidden_test.py"
    if hidden_test_path.exists():
        print("[Running Hidden Acceptance Test Suite]...")
        # Run hidden test in isolation
        h_code, h_out = run_cmd(f"python3 -m pytest -q --tb=short {hidden_test_path}")
        print(h_out + "\n")
        if h_code != 0:
            print("❌ RESULT: FAIL (HIDDEN ACCEPTANCE TESTS FAILED)")
            sys.exit(1)
        else:
            print("✅ Hidden acceptance tests passed!")

    print("✅ RESULT: PASS")
    print(f"Task {task_id} successfully satisfied all feature criteria and test constraints.")


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 evals/score_feature.py [reset|score] <task_id>")
        sys.exit(1)
    action = sys.argv[1].lower()
    task_id = sys.argv[2]
    if action == "reset":
        reset_task(task_id)
    elif action == "score":
        score_task(task_id)
    else:
        print(f"Unknown action: {action}")
        sys.exit(1)


if __name__ == "__main__":
    main()
