---
description: Scan for duplicate modules and present consolidation options (HITL)
---

# /qa-reuse-check

**Purpose:** Force a reuse check scan before construction phase.

## Instructions

**1. RUN ALL THREE COMMANDS and SHOW output:**

```bash
find framework/pages -name "*.py" -not -name "__init__.py"
find framework/tasks -name "*.py" -not -name "__init__.py"
find framework/roles -name "*.py" -not -name "__init__.py"
```

**2. ANALYZE each layer for duplicates:**

Look for the SAME filename appearing in DIFFERENT workflow folders:
- `login_page.py` in `pm_assistant/` AND `update/` → DUPLICATE
- `auth_tasks.py` in multiple workflows → DUPLICATE
- `assistant_page.py` only in `pm_assistant/` → NOT a duplicate (workflow-specific)

**3. IF any duplicates found in ANY layer, PRESENT this to user:**

```
DUPLICATE MODULES FOUND
=======================

PAGES:
  [filename].py exists in:
    → framework/pages/[workflow1]/[filename].py
    → framework/pages/[workflow2]/[filename].py

OPTIONS:
1. CONSOLIDATE NOW - Move ALL duplicates to common/, update imports
2. SKIP FOR NOW - Continue, consolidate later

Which option? (1/2):
```

**4. WAIT for user response before proceeding.**

**5. If CONSOLIDATE chosen:**
- Create `framework/pages/common/`, `framework/tasks/common/`, `framework/roles/common/` as needed
- Move the modules there
- Update imports in ALL files that used the old paths
- Delete the duplicates
- Run tests to verify nothing broke

## Generic vs Workflow-Specific

**Generic (should be in common/):**
- Pages: LoginPage, LogoutPage, NavigationPage, HubPage
- Tasks: AuthTasks, NavigationTasks (login/logout flows)
- Roles: Shared authentication roles

**Workflow-specific (keep in workflow folder):**
- Pages: AssistantPage, HubDashboardPage
- Tasks: PmAssistantTasks, UpdateTasks
- Roles: Domain-specific user personas (ProductManagerRole)

## When to Use

Invoke `/qa-reuse-check` if:
- Starting a new workflow that might reuse existing modules
- Pre-construction checkpoint was skipped
- You suspect duplicates exist but weren't checked
