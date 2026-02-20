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
/run-test tests/banking/test_new_customer_banking.py
/run-test tests/auth/test_login.py::test_valid_login
/run-test tests/  # Run all tests
```

## Instructions

**FIRST: Read protocol from `.claude/protocols/qa-protocol.md`**

The testing skill defines:
- Visual feedback requirements
- Failure handling protocol (STOP, REPORT, ANALYZE, DISCUSS)
- Defect tracking requirements

### Step 1: Validate Test Path

Check that the provided argument `$ARGUMENTS` is a valid test path:
- File exists (for specific test file)
- Directory exists (for test directory)
- Pattern is valid pytest format

If invalid, report error and suggest valid paths.

### Step 2: Run Test Command

**Project convention (py_sel_framework_mcp):**

```bash
pytest $ARGUMENTS -v --html=tests/_reports/report.html --self-contained-html
```

### Step 3: Visual Feedback

During execution, show:
- Test names as they run
- PASSED/FAILED status per test
- Progress indication

### Step 4: Results Summary

After execution, show:
- Total passed/failed count
- Report file location: `tests/_reports/report.html`
- Clear PASS/FAIL verdict

### Step 5: On Failure (CRITICAL)

If ANY test fails, follow the testing skill failure protocol:

1. **STOP** - Halt, do not auto-fix
2. **REPORT** - Show: test name, error, location
3. **ANALYZE** - Explain: expected vs actual, likely cause
4. **DISCUSS** - Ask: "Create defect entry in docs/DEFECT_LOG.md?"
5. **FIX OPTIONS** - Present 2-3 fix approaches with tradeoffs
6. **DISCUSS FIX** - Ask: "Which fix approach? Proceed?"
7. **FIX** - Implement approved fix only
8. **RE-TEST** - Run same tests again

**Never auto-fix without user approval.**

## Example Output

```
Running: pytest tests/banking/test_new_customer_banking.py -v

tests/banking/test_new_customer_banking.py::TestNewCustomerBanking::test_new_customer_can_register_and_open_savings PASSED
tests/banking/test_new_customer_banking.py::TestNewCustomerBanking::test_customer_can_register_transfer_and_verify PASSED

========================= 2 passed in 15.32s =========================

Report: tests/_reports/report.html

VERDICT: PASS
```
