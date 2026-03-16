# Platform Selenium Protocol

**Domain:** platform_selenium
**Type:** Indexed
**Created:** 2026-03-15

---

## Architecture

4-layer POM pattern (bottom to top):

```
BrowserInterface  ←  Selenium WebDriver wrapper (DO NOT modify)
     ↑
   Pages          ←  Page Object Models (atomic UI actions)
     ↑
   Tasks          ←  Orchestrate pages for domain operations
     ↑
   Roles          ←  Orchestrate tasks for business workflows
     ↑
   Tests          ←  Pytest tests using Role + POM state-checks
```

Each layer composes the layer below it. **No layer skips.**

---

## References

### Canonical Code Patterns

| Layer | Reference File |
|-------|---------------|
| BrowserInterface | `framework/interfaces/browser_interface.py` |
| POM (Page) | `framework/_reference/pages/login_page.py` |
| Task | `framework/_reference/tasks/employee_management_tasks.py` |
| Role | `framework/_reference/roles/employee_manager.py` |
| Test | `framework/_reference/tests/test_e2e_create_employee_and_assign_task.py` |

*Read these during `/kernel/anchor` — they are the source of truth for patterns.*

### Live Implementation Examples

| Feature | Pages | Tasks | Roles | Tests |
|---------|-------|-------|-------|-------|
| PM Assistant | `framework/pages/pm_assistant/` | `framework/tasks/pm_assistant/` | `framework/roles/pm_assistant/` | `tests/pm_assistant/` |
| Update | `framework/pages/update/` | `framework/tasks/update/` | — | `tests/update/` |

### QA Workflow Skill

→ `.claude/skills/qa-management-layer/SKILL.md`
→ `.claude/skills/qa-management-layer/workflow.md`
→ `.claude/skills/qa-management-layer/gate-contract.md`
→ `.claude/skills/qa-management-layer/steps/` (step-01 through step-05)
→ `.claude/skills/qa-management-layer/checkpoints/` (pre-construction, on-failure, propose-fix)

### Lessons Learned

→ `.claude/lessons/lessons.md`

---

## Layer Patterns (Summary — read references for full detail)

### BrowserInterface

- Composition only — never inherit
- Text entry method: `browser.type(by, value, text)`
- NO `implicitly_wait` — use `WebDriverWait` (explicit waits only)
- `wait_for_element_visible` and `is_element_displayed` ignore `StaleElementReferenceException` and `AttributeError`

### POM Layer (`framework/pages/**/*.py`)

- NO `@autologger` decorators
- Locators as class constants: `LOCATOR_NAME = (By.CSS_SELECTOR, "...")`
- Atomic methods (one UI action) returning `self` for chaining
- State-check methods (`is_*`, `has_*`, `get_*`) for assertions
- Compose `BrowserInterface` — NO inheritance
- NEVER contain `By.` imports beyond locator constants

### Task Layer (`framework/tasks/**/*.py`)

- `@autologger.automation_logger("Task")` on every method
- NO decorator on `__init__`
- Methods return `None` — no return values
- Compose Pages only — NO Role imports
- One domain operation per method

### Role Layer (`framework/roles/**/*.py`)

- `@autologger.automation_logger("Role")` on workflow methods
- `@autologger.automation_logger("Role Constructor")` on `__init__`
- Methods return `None` — no return values
- Compose Tasks only — NO Page imports
- Orchestrates MULTIPLE task calls

### Test Layer (`tests/**/*.py`)

- `@autologger.automation_logger("Test")` on test methods
- `@pytest.mark.<marker>` for categorization (auto-registered by conftest)
- AAA pattern: Arrange → Act → Assert
- Imports Roles for Act, POMs for Assert (state-check methods only)
- Fixtures from `tests/conftest.py`: `browser`, `config`, `test_users`
- Reports: `tests/_reports/report.html`

### Import Convention (inside framework/)

- Always use relative imports: `from .module import X`
- NEVER use `from framework.module import X` inside `framework/`

### Locator Strategy

- Prefer `data-testid` CSS selectors
- For modern JS apps (inline-style layouts): use inline-style XPath, NOT class-based
- DOM-inspect before writing any locator — never assume class names

---

## File Naming Conventions

| Layer | Convention | Example |
|-------|-----------|---------|
| Pages | `{feature}_page.py` | `assistant_page.py` |
| Tasks | `{feature}_tasks.py` | `pm_assistant_tasks.py` |
| Roles | `{persona}_role.py` | `product_manager_role.py` |
| Tests | `test_{feature}.py` | `test_pm_assistant_priorities.py` |
| Workflow folders | `{workflow}/` | `pm_assistant/`, `update/` |

---

## Test Infrastructure

| File | Purpose |
|------|---------|
| `tests/conftest.py` | Fixtures: browser, config, test_users |
| `tests/data/test_users.json` | Test user credentials |
| `framework/resources/config/environment_config.json` | Environments: DEFAULT, parabank, pm_hub |
| `tests/_state/workflow_state.json` | QA workflow step state |
| `tests/_reports/report.html` | HTML test report |

### Run Tests

```bash
pytest tests/ -v --html=tests/_reports/report.html --self-contained-html
pytest tests/pm_assistant/ -v --env=pm_hub
```

---

## Anti-Patterns

| Anti-Pattern | Why |
|-------------|-----|
| `time.sleep()` | Non-deterministic — use BrowserInterface wait methods |
| `implicitly_wait` + `WebDriverWait` | Causes unpredictable Selenium behavior (LESSON 004) |
| Locators in Task layer | Task layer must only call POM methods |
| Page imports in Role layer | Roles must only compose Tasks |
| `from framework.X import Y` inside framework/ | ModuleNotFoundError — use relative imports (LESSON 005) |
| `cd subdir && command` in Bash | Breaks hook relative paths (LESSON 003) |
| Class-based selectors on JS apps | Modern JS uses inline styles — DOM-inspect first (LESSON 002) |
| `enter_text()` method | Does not exist on BrowserInterface — use `type()` (LESSON 001) |

---

## Entry Points

| Command | Purpose |
|---------|---------|
| `/qa-workflow` | Run 5-step QA test generation workflow (production) |
| `/qa-workflow-dev` | Run 5-step workflow (development mode, full access) |
| `/run-test` | Run pytest with HITL failure protocol |
| `/pr` | Code review against framework patterns |
| `/qa-pre-construction` | Pre-construction checkpoint (read before Step 4) |
| `/qa-on-failure` | On-failure HITL checkpoint |
| `/qa-propose-fix` | Propose fix before applying |
| `/qa-reuse-check` | Scan for duplicate modules |

---

*Protocol is an INDEX. Agent reads referenced files during `/kernel/anchor`.*
