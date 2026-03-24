---
description: Run the Isagawa QA Kernel inside Antigravity — generates 5-layer Selenium test suites with enforced architectural discipline, self-anchoring, and human-in-the-loop triage. No Claude Code hooks required.
---

# Isagawa Pilot Workflow (Antigravity Adaptation)

## Purpose

This workflow emulates the **Isagawa Kernel** inside Google Antigravity.

In Claude Code, the Kernel uses `.claude/hooks` to hard-block writes at the OS level.
In Antigravity, enforcement is achieved through **mandatory checkpointing** — the agent
MUST complete each gate before proceeding. Any step marked `[GATE]` is non-negotiable.

**Platform:** Python + Selenium (5-layer architecture)
**Repo:** `/Users/briandawson/workspace/platform-selenium`
**Target:** Configurable — set `TARGET_URL` in Step 1.

---

## Pre-Conditions

Before invoking this workflow, ensure:
- [ ] Local dev server for target app is running (or staging URL is accessible)
- [ ] Python venv is active: `source venv/bin/activate`
- [ ] `.env` is configured with `BROWSER`, `HEADLESS`, and `TEST_ENV`
- [ ] `environment_config.json` has the correct URL for `TEST_ENV`

---

## Phase 0: Kernel Initialization (Session Start)

**This phase is mandatory. Do NOT skip.**

1. Read the full architecture definition:
   - `README.md` — 5-layer overview and key rules
   - `docs/architecture.md` — complete layer specifications with code examples
   - `CONTRIBUTING.md` — layer rules and key constraints
   - `framework/_reference/pages/*.py` — canonical POM patterns
   - `framework/_reference/tasks/*.py` — canonical Task patterns
   - `framework/_reference/roles/*.py` — canonical Role patterns
   - `framework/_reference/tests/*.py` — canonical Test patterns

2. Read the kernel commands to understand enforcement intent:
   - `.claude/commands/qa-workflow.md`
   - `.claude/skills/qa-management-layer/SKILL.md`
   - `.claude/commands/kernel/anchor.md`

3. Internalize and confirm the following **Non-Negotiable Rules** before proceeding:
   ```
   [KERNEL INITIALIZED]
   Rules confirmed:
   - Locators live ONLY in Page Objects (By.* constants)
   - Tasks and Roles NEVER return values
   - Return `self` from all POM atomic methods (fluent API)
   - Tests assert ONLY via POM state-check methods (is_*, has_*, get_*)
   - @autologger on every Task, Role, and Test method (NOT on POM methods)
   - No time.sleep() — use BrowserInterface explicit waits only
   - Read reference files BEFORE writing any code (never from memory alone)
   ```

4. State the target application and workflow to be tested.

---

## Phase 1: Requirement Capture [GATE]

Ask the user for the test requirement in User Story format:

```
What test do you want to generate?

Provide:
- Persona      — e.g., "admin", "sales rep", "guest user"
- Target URL   — e.g., "https://staging.myapp.com" or "http://localhost:3000"
- Action       — e.g., "submit a service inquiry"
- Workflow ID  — e.g., "inquiry_submission" (used for folder naming)

Format: "As a [persona], I want to [action] on [URL]"
```

**[GATE]:** Do NOT proceed to Phase 2 until requirement is captured and confirmed.

---

## Phase 2: Pre-Flight Configuration [GATE]

1. Run the configuration check:
   ```bash
   cd /Users/briandawson/workspace/platform-selenium
   python -m pytest --collect-only 2>&1 | head -30
   ```
   - Confirm pytest can find and collect test files without import errors.
   - If errors exist → STOP and report. Do NOT proceed until resolved.

2. Verify environment config matches target URL:
   - Read `framework/resources/config/environment_config.json`
   - Confirm the `TEST_ENV` key maps to the correct URL from the requirement

3. Confirm browser driver is available:
   ```bash
   ls framework/resources/chromedriver/
   ```

**[GATE]:** All checks must pass. If any fail, report to user and wait for resolution.

---

## Phase 3: Discovery (Playwright MCP) [GATE]

Use the Playwright MCP to perform live page inspection on the target URL.

For each page involved in the workflow (login page, target page, modal dialogs, etc.):

1. Navigate to the page using Playwright MCP browser tools
2. Capture all interactive elements:
   - Buttons, links, inputs, selects, checkboxes
   - Preferred: `data-testid` attributes (most stable)
   - Fallback: CSS selectors, ARIA roles, XPath (last resort)
3. Identify toast/notification elements for assertions
4. Map each UI element to its proposed locator constant name

Output a **Discovery Report**:
```
DISCOVERY REPORT — [Workflow ID]

Page: [Page Name] ([URL])
─────────────────────────────
Element: [Description]
  Locator Strategy: [By.CSS_SELECTOR / By.XPATH / etc.]
  Selector: "[selector string]"
  Constant Name: [PROPOSED_CONSTANT_NAME]

... (repeat for all elements)

State-Check Elements (for assertions):
  [element] → [is_* method name]
```

**[GATE]:** Present Discovery Report to user. Wait for confirmation before Phase 4.

---

## Phase 4: Construction (5-Layer Code Generation) [CHECKPOINT AFTER EACH LAYER]

**MANDATORY PRE-CONSTRUCTION CHECK:**
Before writing any code, re-read the matching reference file for each layer.
State which reference file you read. Do NOT write code from memory.

### Layer 1 of 5: Page Object(s)

File location: `framework/pages/{workflow_id}/{page_name}_page.py`

Rules enforced:
- All locators are class-level `By.*` tuple constants (UPPER_SNAKE_CASE)
- `__init__` receives `BrowserInterface` via composition (NO inheritance)
- Atomic methods: one UI action per method, return `self`
- State-check methods: `is_*`, `has_*`, `get_*` — return bool or value
- NO `@autologger` on POM methods
- NO direct Selenium calls — ONLY `self.browser.*` BrowserInterface methods

**[CHECKPOINT]:** After writing POM code, self-review against rules above.
Report: `POM Layer: PASS` or list violations found.

### Layer 2 of 5: Task(s)

File location: `framework/tasks/{workflow_id}/{workflow_id}_tasks.py`

Rules enforced:
- `@autologger.automation_logger("Task")` on every method (NOT constructor)
- Composes Page Objects in `__init__` — instantiate ALL pages needed
- One domain operation per method
- Fluent POM chaining for readable sequences
- NEVER return values from Task methods

**[CHECKPOINT]:** After writing Task code, self-review against rules above.
Report: `Task Layer: PASS` or list violations found.

### Layer 3 of 5: Role(s)

File location: `framework/roles/{workflow_id}/{persona}_role.py`

Rules enforced:
- `@autologger.automation_logger("Role Constructor")` on `__init__`
- `@autologger.automation_logger("Role")` on workflow methods
- Composes Task modules in `__init__`
- Workflow methods call one or more Tasks
- NEVER return values from Role methods
- `_continue` variant skips login for multi-role integration tests

**[CHECKPOINT]:** After writing Role code, self-review against rules above.
Report: `Role Layer: PASS` or list violations found.

### Layer 4 of 5: Test

File location: `tests/{workflow_id}/test_{workflow_id}.py`

Rules enforced:
- `@autologger.automation_logger("Test")` decorator on test method
- `@pytest.fixture(autouse=True)` setup method wires browser, config, test_users
- AAA pattern: Arrange / Act / Assert clearly delineated with comments
- Asserts ONLY via POM state-check methods (no raw Selenium assertions)
- Multi-role workflows supported (two Role instances, one shared browser)

**[CHECKPOINT]:** After writing Test code, self-review against rules above.
Report: `Test Layer: PASS` or list violations found.

### Layer 5: BrowserInterface (Extension Only If Required)

File location: `framework/interfaces/browser_interface.py`

- DO NOT modify unless a new fundamental browser interaction is required
- If a required method doesn't exist: STOP and ASK USER before creating it
- Any new method must follow the existing wait + retry + logging pattern

---

## Phase 5: Architectural Review [GATE]

Before running any test, perform a full `/pr`-style review of ALL generated files:

For each file, verify:
| Check | Status |
|-------|--------|
| Layer separation respected? | ✓/✗ |
| Locators only in POM? | ✓/✗ |
| No return values from Tasks/Roles? | ✓/✗ |
| `return self` in all POM atomic methods? | ✓/✗ |
| `@autologger` correct per layer? | ✓/✗ |
| No `time.sleep()`? | ✓/✗ |
| BrowserInterface used (no raw Selenium in POM)? | ✓/✗ |

Output format:
```
ARCHITECTURE REVIEW — [Workflow ID]

framework/pages/.../page.py       → PASS
framework/tasks/.../tasks.py      → PASS
framework/roles/.../role.py       → PASS
tests/.../test_workflow.py        → PASS

Violations: 0
Ready to execute.
```

**[GATE]:** If ANY violation is found → fix it BEFORE running tests. Do NOT test broken architecture.

---

## Phase 6: Test Execution + Learn Loop

1. Run the test:
   ```bash
   cd /Users/briandawson/workspace/platform-selenium
   source venv/bin/activate
   pytest tests/{workflow_id}/ -v
   ```

2. **On PASS:**
   - Report results to user
   - Document what patterns worked well as a lesson
   - Workflow complete ✓

3. **On FAIL (Human-in-the-Loop Triage):**

   ```
   TEST FAILURE REPORT

   Test:    [test method name]
   Error:   [exception message]
   Line:    [file and line number]
   Layer:   [which layer failed — POM / Task / Role / Test / Browser]

   Likely cause: [root cause analysis]

   Options:
   A) Fix the locator (selector changed on page)
   B) Fix the wait condition (timing issue)
   C) Fix the layer violation (architecture error)
   D) Re-discover the page (UI changed significantly)

   Which option should I pursue? [Wait for user decision]
   ```

   **[GATE]:** NEVER auto-fix. ALWAYS wait for user direction.

4. **After Fix (Learn Ritual):**

   After every fix, mandatory lesson capture:
   ```
   LESSON LEARNED — [Workflow ID] — [Date]

   What failed: [description]
   Root cause:  [layer, type of error]
   Fix applied: [what was changed]
   Prevention:  [rule to add or reinforce going forward]
   ```

   Append this lesson to `.claude/lessons/lessons.md` in the platform repo.

---

## Completion Checklist

Before declaring the pilot complete:
- [ ] All 5 layers generated and passing Architecture Review
- [ ] Tests pass in headed mode (`HEADLESS=false`)
- [ ] Tests pass in headless mode (`HEADLESS=true`)
- [ ] Lessons from any failures documented in `lessons.md`
- [ ] Discovery Report saved to `docs/pilots/{workflow_id}_discovery.md`
- [ ] User has reviewed and approved the generated code

---

## Adapting This Workflow to Other Projects

To run this pilot against a different application (FACETS, Living Decks, SovAI):
1. Update `environment_config.json` with the new app's `url`
2. Set `TEST_ENV` in `.env` to match the new config key
3. Provide the new User Story in Phase 1
4. The 5-layer architecture and enforcement rules remain identical
