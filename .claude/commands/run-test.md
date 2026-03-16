---
description: Run tests with testing skill protocol (invoke with test path argument)
---

# Run Test Command

Execute tests following the testing skill protocol.

## Kernel Loop Integration

1. **Anchor first:** Invoke `/kernel/anchor` before executing tests
2. **On failure:** Invoke `/kernel/fix` then `/kernel/learn` after any fix
3. **On completion:** Invoke `/kernel/complete` when tests pass

## Usage

```
/run-test tests/pm_assistant/test_pm_assistant_priorities.py
/run-test tests/update/test_pm_priority_update.py
/run-test tests/  # Run all tests
```

## Instructions

**FIRST: Read protocol from `.claude/protocols/platform_selenium-protocol.md`**

The protocol defines:
- Layer architecture and patterns
- Failure handling protocol (STOP, REPORT, ANALYZE, DISCUSS)

### Step 1: Validate Test Path

Check that the provided argument `$ARGUMENTS` is a valid test path:
- File exists (for specific test file)
- Directory exists (for test directory)
- Pattern is valid pytest format

If invalid, report error and suggest valid paths.

### Step 2: Run Test Command

```bash
pytest $ARGUMENTS -v --html=tests/_reports/report.html --self-contained-html
```

Add `--env=pm_hub` for PM Hub tests (localhost:3000).

### Step 3: Visual Feedback

During execution, show:
- Test names as they run
- PASSED/FAILED status per test

### Step 4: Results Summary

After execution, show:
- Total passed/failed count
- Report file location: `tests/_reports/report.html`
- Clear PASS/FAIL verdict

### Step 5: On Failure (CRITICAL)

If ANY test fails, follow HITL protocol:

1. **STOP** - Halt, do not auto-fix
2. **REPORT** - Show: test name, error, location
3. **ANALYZE** - Explain: expected vs actual, likely cause
4. **DISCUSS** - Ask: "Create defect entry in docs/DEFECT_LOG.md?"
5. **FIX OPTIONS** - Present 2-3 fix approaches with tradeoffs
6. **DISCUSS FIX** - Ask: "Which fix approach? Proceed?"
7. **FIX** - Implement approved fix only
8. **RE-TEST** - Run same tests again

**Never auto-fix without user approval.**
