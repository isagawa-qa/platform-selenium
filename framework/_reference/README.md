# Reference Implementation

**Purpose:** Canonical code patterns for AI to learn from before generating any layer code.

---

## AI Instructions

**BEFORE generating any POM, Task, Role, or Test code, you MUST read these files:**

| Layer | File to Read | Learn |
|-------|--------------|-------|
| **POM** | `pages/employees_page.py` | Locators, atomic methods, state-check methods, return self |
| **Task** | `tasks/employee_management_tasks.py` | @autologger, POM composition, no returns, fluent API |
| **Role** | `roles/employee_manager.py` | @autologger, Task composition, workflow orchestration |
| **Test** | `tests/test_e2e_create_employee_and_assign_task.py` | AAA pattern, fixtures, Role calls, POM assertions |

---

## 4-Layer Pattern Summary

### POM (Page Object Model)
```python
# NO decorators
# Locators as class constants
# Atomic methods (one UI action)
# Return self for chaining
# State-check methods for assertions
```

### Task
```python
# @autologger("Task") on methods
# NO decorator on constructor
# Composes Page Objects
# One domain operation per method
# NO return values
```

### Role
```python
# @autologger("Role") on workflow methods
# @autologger("Role Constructor") on __init__
# Composes Task modules
# Workflow methods call MULTIPLE tasks
# NO return values
```

### Test
```python
# @autologger("Test") decorator
# Call Role workflow methods (chain when workflow requires it)
# Assert via Page Object state-check methods
# NO test-level orchestration (belongs in Role layer)
```

---

## File Structure

```
_reference/
├── README.md                                          ← You are here
├── __init__.py
├── pages/
│   ├── __init__.py
│   ├── login_page.py                                  ← POM pattern (login)
│   ├── employees_page.py                              ← POM pattern (employees)
│   └── tasks_page.py                                  ← POM pattern (tasks)
├── tasks/
│   ├── __init__.py
│   ├── employee_management_tasks.py                   ← Task pattern (employee mgmt)
│   └── task_management_tasks.py                       ← Task pattern (task mgmt)
├── roles/
│   ├── __init__.py
│   ├── employee_manager.py                            ← Role pattern (employee manager)
│   └── task_manager.py                                ← Role pattern (task manager)
└── tests/
    ├── __init__.py
    └── test_e2e_create_employee_and_assign_task.py    ← Test pattern (integration)
```

---

## Key Rules (from patterns)

| Rule | Enforced In |
|------|-------------|
| NO locators in Tasks/Roles | Task, Role |
| NO return values from Tasks/Roles | Task, Role |
| Return `self` from POM atomic methods | POM |
| Assert via POM state-check methods | Test |
| `@autologger` on Task/Role/Test methods | All |
| Multi-role workflows supported | Test |
| `_continue` variants skip login for shared sessions | Role |

---

*This is the authoritative source for code patterns. When in doubt, read these files.*
