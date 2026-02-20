---
description: Instant PR review - validates code against framework patterns like a senior SDET would
---

# /pr - Instant Code Review

What takes 30-60 min in a PR cycle, done in 5 seconds.

---

## Instructions

### 1. Scan Directories

Scan all framework layers:
- `framework/pages/` - Page Objects (POMs)
- `framework/tasks/` - Task modules
- `framework/roles/` - Role modules
- `tests/` - Test files (exclude conftest.py, __init__.py)

### 2. Layer Architecture Checks

#### POM Layer (`framework/pages/**/*.py`)
- [x] Has locators as class constants (tuples with By.*)
- [x] Has atomic methods returning `self`
- [x] Has state-check methods (`is_*`, `get_*`, `has_*`)
- [ ] VIOLATION: Has `@autologger` decorator (POMs don't use it)
- [ ] VIOLATION: Imports from tasks/ or roles/
- [ ] VIOLATION (DD-49): Hardcoded URLs - must use `self.browser.config['url']`

#### Task Layer (`framework/tasks/**/*.py`)
- [x] Has `@autologger.automation_logger("Task")` decorator
- [x] Methods return `None` (no return statements with values)
- [x] Imports from pages/ only
- [ ] VIOLATION (DD-27): Contains `By.` imports or locator tuples
- [ ] VIOLATION: Imports from roles/
- [ ] VIOLATION (DD-49): Direct navigation - Tasks must call POM navigate()

#### Role Layer (`framework/roles/**/*.py`)
- [x] Has `@autologger.automation_logger("Role")` decorator
- [x] Methods return `None` (no return statements with values)
- [x] Imports from tasks/ only
- [ ] VIOLATION: Contains `By.` imports or locator tuples
- [ ] VIOLATION: Imports from pages/ directly
- [ ] VIOLATION (DD-49): Direct navigation - Roles must NOT navigate

#### Test Layer (`tests/**/*.py`)
- [x] Has `@autologger.automation_logger("Test")` decorator
- [x] Imports Role from roles/
- [x] Imports POM from pages/ (for assertions only)
- [x] Uses POM state-check methods in assertions
- [ ] VIOLATION: Contains `By.` imports or locator tuples
- [ ] VIOLATION: Imports from tasks/ directly
- [ ] VIOLATION: Calls multiple Role methods (should call ONE workflow method)

### 3. Senior SDET Quality Checks

#### Code Quality (Any violation triggers HITL)
- [ ] VIOLATION: `time.sleep()` calls - use BrowserInterface wait methods instead
- [ ] VIOLATION: Hardcoded credentials - use config/fixtures (unless user specifies otherwise)
- [ ] VIOLATION: Magic numbers without explanation - use constants or inline comments (e.g., `timeout=30` needs `# 30s for slow AJAX`)
- [ ] VIOLATION: Missing docstrings - all methods require docstrings (see reference modules in `framework/`)
- [ ] VIOLATION: Complex logic without inline comments explaining why

#### Naming Conventions
- [ ] VIOLATION: Methods not snake_case
- [ ] VIOLATION: Classes not PascalCase
- [ ] VIOLATION: Locator constants not SCREAMING_SNAKE_CASE

#### Test Quality
- [ ] VIOLATION: Test without assertions
- [ ] VIOLATION: Test depends on another test's state
- [ ] VIOLATION: Bare `except:` without specific exception

#### Wait Patterns
- [ ] VIOLATION: Implicit waits mixed with explicit waits
- [ ] VIOLATION: No timeout parameter on wait calls

#### BrowserInterface Usage
- [ ] VIOLATION: Wrapping BrowserInterface methods instead of calling directly
- [ ] VIOLATION: Creating new wait/click/type methods when BrowserInterface already has them
- [ ] NOTE: If a needed method doesn't exist in BrowserInterface, trigger HITL to discuss adding it

---

## CRITICAL: HITL Protocol

**On ANY violation found, you MUST follow this protocol:**

### Rule: STOP on Violation

When violations are found:
1. **STOP** - Do not attempt autonomous fixes
2. **REPORT** - Show violations with file:line references
3. **WAIT** - Get human decision before proceeding

### What NOT To Do

- Do NOT auto-fix violations without asking
- Do NOT assume you know the right fix
- Do NOT skip violations and continue
- Do NOT loop trying different fixes

---

## Report Format

### If All Pass:
```
PR REVIEW: APPROVED
============================

PASS: framework/pages/testparabank1/login_page.py
PASS: framework/tasks/testparabank1/parabank_tasks.py
PASS: framework/roles/testparabank1/customer.py
PASS: tests/testparabank1/test_customer_workflow.py

Summary: 4 files checked, 0 violations

Ready to merge.
```

### If Violations Found (HITL Triggered):
```
PR REVIEW: CHANGES REQUESTED
============================

PASS: framework/pages/testparabank1/login_page.py
PASS: framework/roles/testparabank1/customer.py
FAIL: framework/tasks/testparabank1/parabank_tasks.py
  - Line 9: VIOLATION (DD-27) - Has `from selenium.webdriver.common.by import By`
  - Line 84: VIOLATION (DD-27) - Uses `By.ID` locator in Task layer
FAIL: tests/testparabank1/test_customer_workflow.py
  - Line 23: VIOLATION - `time.sleep(5)` - use explicit wait

Summary: 4 files checked, 2 failed, 3 violations

==========================================

HOW SHOULD WE PROCEED?

1. Fix All
   -> AI fixes each violation
   -> Re-runs /pr after fixes

2. Fix Specific
   -> You specify which violations to fix
   -> AI applies only those fixes

3. Explain
   -> AI explains why each is a violation
   -> You decide what to do

4. Ignore + Approve
   -> Skip these violations (document reason)
   -> Proceed anyway

5. Other
   -> Describe what you want to do

Enter choice (1-5):
```

---

## HITL Response Protocol

When violations are found:

1. **Present violations clearly**
   - File path and line number
   - Violation type and rule (DD-XX if applicable)
   - Brief explanation

2. **Present numbered options (1-5)**
   - Always include all 5 options
   - Wait for user input

3. **Handle user decision**
   - Option 1 (Fix All): Fix each violation, re-run /pr
   - Option 2 (Fix Specific): Ask which ones, fix only those
   - Option 3 (Explain): Explain each violation's impact
   - Option 4 (Ignore): Document reason, mark as approved with exceptions
   - Option 5 (Other): Follow user's instructions

4. **After fixes applied**
   - Re-run /pr to verify
   - Report new results
   - Repeat until clean or user approves

**Key Rule:** AI must NOT fix without user decision. Present options, wait for input.

---

## Severity Levels

| Severity | Description | Examples |
|----------|-------------|----------|
| **CRITICAL** | Breaks architecture, must fix | Locators in Task, Role imports pages |
| **HIGH** | Best practice violation | time.sleep(), hardcoded creds |
| **MEDIUM** | Code quality issue | Missing docstring, naming convention |
| **LOW** | Style/preference | Minor formatting |

Report violations grouped by severity, CRITICAL first.
