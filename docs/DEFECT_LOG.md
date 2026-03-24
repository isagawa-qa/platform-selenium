# Defect Log

---

## DEF-001 — framework/__init__ absolute import path breaks test collection

**Date:** 2026-03-15
**Severity:** High (blocks all test execution)
**Status:** RESOLVED

**What happened:**
`pytest tests/update/test_pm_priority_update.py --env pm_hub` fails at conftest import with `ModuleNotFoundError: No module named 'framework'`.

**Expected:** conftest loads BrowserInterface successfully, tests collect and run.

**Actual:** `framework/interfaces/__init__.py` uses `from framework.interfaces.browser_interface import BrowserInterface`. Since `conftest.py` adds only `framework/` (not the project root) to `sys.path`, the module `framework` does not exist from inside the `framework/` tree.

**Location:** `framework/interfaces/__init__.py:8`

---
