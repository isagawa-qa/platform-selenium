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
- [ ] VIOLATION: Hardcoded URLs - must use `self.browser.config['url']` or parameter

#### Task Layer (`framework/tasks/**/*.py`)
- [x] Has `@autologger.automation_logger("Task")` decorator on methods
- [x] Methods return `None` (no return statements with values)
- [x] Imports from pages/ only
- [ ] VIOLATION: Contains `By.` imports or locator tuples
- [ ] VIOLATION: Imports from roles/

#### Role Layer (`framework/roles/**/*.py`)
- [x] Has `@autologger.automation_logger("Role")` decorator on workflow methods
- [x] Has `@autologger.automation_logger("Role Constructor")` on `__init__`
- [x] Methods return `None` (no return statements with values)
- [x] Imports from tasks/ only
- [ ] VIOLATION: Contains `By.` imports or locator tuples
- [ ] VIOLATION: Imports from pages/ directly

#### Test Layer (`tests/**/*.py`)
- [x] Has `@autologger.automation_logger("Test")` decorator on test methods
- [x] Imports Role from roles/
- [x] Imports POM from pages/ (for assertions only)
- [x] Uses POM state-check methods in assertions
- [ ] VIOLATION: Contains `By.` imports or locator tuples
- [ ] VIOLATION: Imports from tasks/ directly

### 3. Senior SDET Quality Checks

#### Code Quality (Any violation triggers HITL)
- [ ] VIOLATION: `time.sleep()` calls - use BrowserInterface wait methods instead
- [ ] VIOLATION: Missing docstrings - all methods require docstrings
- [ ] VIOLATION: Complex logic without inline comments

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

#### Import Patterns
- [ ] VIOLATION: `from framework.X import Y` inside framework/ package (use relative imports)

#### BrowserInterface Usage
- [ ] VIOLATION: Using `enter_text()` - the correct method is `type()`
- [ ] VIOLATION: Wrapping BrowserInterface methods instead of calling directly
- [ ] NOTE: If a needed method doesn't exist in BrowserInterface, trigger HITL to discuss adding it

---

## CRITICAL: HITL Protocol

**On ANY violation found:**

1. **STOP** - Do not attempt autonomous fixes
2. **REPORT** - Show violations with file:line references
3. **WAIT** - Get human decision before proceeding

### Report Format (Violations Found)

```
PR REVIEW: CHANGES REQUESTED
============================

FAIL: framework/tasks/[workflow]/[file].py
  - Line 9: VIOLATION - Has `from selenium.webdriver.common.by import By`
  - Line 84: VIOLATION - Uses `By.ID` locator in Task layer

Summary: X files checked, Y failed, Z violations

HOW SHOULD WE PROCEED?

1. Fix All
2. Fix Specific
3. Explain
4. Ignore + Approve
5. Other

Enter choice (1-5):
```

### Report Format (All Pass)

```
PR REVIEW: APPROVED
============================

PASS: framework/pages/...
PASS: framework/tasks/...

Summary: X files checked, 0 violations

Ready to merge.
```

---

## Severity Levels

| Severity | Description | Examples |
|----------|-------------|---------|
| CRITICAL | Breaks architecture | Locators in Task/Role, wrong layer imports |
| HIGH | Best practice violation | time.sleep(), wrong method names |
| MEDIUM | Code quality issue | Missing docstring, naming convention |
| LOW | Style/preference | Minor formatting |

Report violations grouped by severity, CRITICAL first.
