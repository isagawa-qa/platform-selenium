# Reference Implementation

**Purpose:** Canonical code patterns for AI to learn from before generating any layer code.

---

## AI Instructions

**BEFORE generating any POM, Task, Role, or Test code, you MUST read these files:**

| Layer | File to Read | Learn |
|-------|--------------|-------|
| **POM** | `pages/inquiry_form_page.py` | Locators, atomic methods, state-check methods, return self |
| **Task** | `tasks/reference_tasks.py` | @autologger, POM composition, no returns, fluent API |
| **Role** | `roles/reference_role.py` | @autologger, Task composition, workflow orchestration |
| **Test** | `tests/test_reference_workflow.py` | AAA pattern, fixtures, Role calls, POM assertions |

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
# Call ONE Role workflow method
# Assert via Page Object state-check methods
# NO orchestration (Role handles workflow)
```

---

## File Structure

```
_reference/
├── README.md                      ← You are here
├── __init__.py
├── pages/
│   ├── __init__.py
│   ├── inquiry_form_page.py       ← POM pattern
│   ├── customer_search_page.py
│   ├── customer_details_page.py
│   ├── contacts_page.py
│   └── address_page.py
├── tasks/
│   ├── __init__.py
│   └── reference_tasks.py         ← Task pattern
├── roles/
│   ├── __init__.py
│   └── reference_role.py          ← Role pattern
└── tests/
    ├── __init__.py
    └── test_reference_workflow.py ← Test pattern
```

---

## Key Rules (from patterns)

| Rule | Enforced In |
|------|-------------|
| NO locators in Tasks/Roles | Task, Role |
| NO return values from Tasks/Roles | Task, Role |
| Return `self` from POM atomic methods | POM |
| Assert via POM state-check methods | Test |
| ONE Role workflow call per test | Test |
| @autologger on Task/Role/Test methods | All |

---

*This is the authoritative source for code patterns. When in doubt, read these files.*
