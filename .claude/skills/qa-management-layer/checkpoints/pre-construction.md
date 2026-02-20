# Pre-Construction Checkpoint

**Invoke:** Before writing ANY code in Step 4 (Construction Phase)

---

## MANDATORY: Complete Before Writing Code

### 0. Reuse Check — MANDATORY SCAN (ALL THREE LAYERS)

**⛔ BLOCKING: Scan pages, tasks, AND roles. Show output. Check for duplicates.**

```
ACTION REQUIRED — RUN ALL THREE COMMANDS:

1. find framework/pages -name "*.py" -not -name "__init__.py"
2. find framework/tasks -name "*.py" -not -name "__init__.py"
3. find framework/roles -name "*.py" -not -name "__init__.py"

SHOW all output. CHECK each layer for duplicates.
```

**Duplicate = same filename in different workflows:**
- `framework/pages/workflow_A/login_page.py` + `framework/pages/workflow_B/login_page.py` → DUPLICATE
- `framework/tasks/workflow_A/auth_tasks.py` + `framework/tasks/workflow_B/auth_tasks.py` → DUPLICATE

**When ANY duplicate found in ANY layer, STOP and ask:**

```
DUPLICATES DETECTED
===================

PAGES:
  login_page.py exists in:
    → framework/pages/goal_management/login_page.py
    → framework/pages/lead_capture/login_page.py

TASKS:
  (check for duplicates)

ROLES:
  (check for duplicates)

OPTIONS:
1. CONSOLIDATE NOW - Move ALL duplicates to common/, update imports
2. CONTINUE - Proceed, consolidate later (adds technical debt)

Which option?
```

**Generic modules (consolidate to common/):**
- Pages: LoginPage, LogoutPage, NavigationPage, HeaderPage, SearchPage
- Tasks: AuthTasks, NavigationTasks (login/logout flows)
- Roles: Shared authentication roles

**Workflow-specific (keep separate):** GoalsPage, BookingPage, domain-unique modules

---

### 1. Read Lessons Learned FIRST

**⛔ BEFORE writing ANY code, read lessons.md:**

```
.claude/lessons/lessons.md
```

**Extract and APPLY all lessons to your code:**
- Wait patterns (wait before click, wait before assert)
- XPath patterns (element-agnostic, @role, @data-testid)
- Anti-patterns to avoid
- Quality gates that were added

**DO NOT repeat mistakes that are already documented.**

---

### 2. Read Reference Files

You MUST read these files NOW (not from memory):

```
framework/_reference/pages/*.py   → POM patterns
framework/_reference/tasks/*.py   → Task patterns
framework/_reference/roles/*.py   → Role patterns
framework/_reference/tests/*.py   → Test patterns
```

**Read each file. Extract patterns. Apply to your code.**

### 3. Check BrowserInterface Methods

Before writing ANY interaction logic:

1. **READ** `framework/interfaces/browser_interface.py`
2. **LIST** methods available (click, type, wait, etc.)
3. **USE** existing methods - do not create workarounds

### 4. Forbidden Patterns

Do NOT use these in generated code:

```python
# FORBIDDEN in POMs:
import time
time.sleep(...)           # Use BrowserInterface wait methods

# FORBIDDEN in Tasks:
from selenium.webdriver.common.by import By
By.ID, By.XPATH, etc.     # Locators belong in POMs only

# FORBIDDEN everywhere:
try:
    ...
except:                   # Never bare except
    pass
```

### 5. Layer Rules Reminder

| Layer | Returns | Contains |
|-------|---------|----------|
| POM | `self` | Locators, atomic methods, state-check methods |
| Task | `None` | Workflow orchestration, @autologger decorator |
| Role | `None` | Multi-task workflows, @autologger decorator |
| Test | N/A | ONE role call, assertions via POM state methods |

---

## Confirmation

**You MUST confirm each item was DONE (not just understood):**

- [ ] I RAN `find` on all 3 layers and SHOWED output
- [ ] I CHECKED for duplicate filenames, PRESENTED HITL if found
- [ ] I READ lessons.md and will APPLY all lessons to my code
- [ ] I READ reference files (not from memory)
- [ ] I CHECKED BrowserInterface methods

**If you skipped lessons.md, GO BACK AND READ IT.**

**Now proceed with code generation.**
