<!-- SPDX-License-Identifier: MIT -->

# Step 4: Collaborative Construction (Playwright 2-Pass)

**Purpose:** Discover elements via Playwright, then construct POM/Task/Role/Test modules collaboratively.

**Workflow Version:** v4.0 (5-Step Pair Programming Workflow)

---

## A. Identity & Flow

| Field | Value |
|-------|-------|
| **Step** | 4 - Collaborative Construction |
| **Dependencies** | Step 3 complete (bdd_scenarios, expected_states, intent exist) |
| **Input** | State from Steps 1-3, Playwright browser |
| **Output** | `discovered_elements`, POM/Task/Role/Test files |

---

## B. Persona Map

| Persona | Actions |
|---------|---------|
| **User** | Watches browser, provides guidance on failures |
| **AI** | Navigates, discovers elements, constructs modules, validates |

---

## C. Discovery Phase (2-Pass)

```
PRE-CHECK:
- Verify Step 3 complete
- READ credential_strategy from Step 2 state

CREDENTIAL HANDLING:
- IF none: Skip to navigation
- IF static: Load creds from test_users.json, login
- IF dynamic: Register fresh user, save, login
- IF self-contained: Register, login (don't persist)

PASS 1 - INPUT ELEMENTS:
1. Navigate to target URL
2. Prepare page state (reveal forms)
3. Take Playwright snapshot
4. Extract INPUT elements (forms, buttons, textboxes)
5. Validate elements found

PASS 2 - OUTPUT ELEMENTS:
1. Submit form / trigger action
2. Take Playwright snapshot of result page
3. Extract OUTPUT elements (confirmations, messages)
4. Validate elements found

CHECKPOINT:
- All pages must have BOTH input AND output elements
- Block construction phase until discovery complete
```

See `step-04-twopass.md` for detailed 2-pass flow.
See `step-04-multipage.md` for multi-page workflows (DD-44).

---

## D. Construction Phase

### ⛔ BLOCKING GATE: Reuse Check Required (ALL THREE LAYERS)

**YOU CANNOT PROCEED TO D.3 WITHOUT COMPLETING THE REUSE CHECK.**

```
BEFORE writing ANY code, scan ALL THREE LAYERS:

1. RUN: find framework/pages -name "*.py" -not -name "__init__.py"
2. RUN: find framework/tasks -name "*.py" -not -name "__init__.py"
3. RUN: find framework/roles -name "*.py" -not -name "__init__.py"
4. SHOW: Display ALL output
5. CHECK: Look for same filename in different workflow folders (any layer)
6. IF DUPLICATE FOUND: Present HITL with consolidate options
7. WAIT: Get user decision before proceeding

❌ DO NOT skip any layer
❌ DO NOT assume no duplicates exist
❌ DO NOT proceed without showing scan results for ALL layers
```

**Commands:**
- `/qa-pre-construction` — Full checkpoint (includes reuse check)
- `/qa-reuse-check` — Standalone reuse check (if checkpoint was skipped)

**This gate blocks construction. No exceptions.**

---

### D.1 MANDATORY: Read Reference Files First

```
BEFORE writing ANY code:

1. READ reference files from protocol:
   - framework/_reference/pages/*.py   → POM patterns
   - framework/_reference/tasks/*.py   → Task patterns
   - framework/_reference/roles/*.py   → Role patterns
   - framework/_reference/tests/*.py   → Test patterns
   - framework/_reference/README.md    → Architecture + Anti-patterns

2. EXTRACT patterns:
   - Locator format (class constants, By tuples)
   - Method signatures (return self, no returns, decorators)
   - Composition pattern (how layers connect)
   - Import paths

3. APPLY patterns to generated code
   - Match reference structure exactly
   - Use same decorator patterns
   - Follow same naming conventions

DO NOT skip this step. DO NOT rely on memory. READ the files.
```

### D.2 MANDATORY: BrowserInterface Methods First

```
BEFORE writing ANY browser interaction in POM:

1. READ framework/interfaces/browser_interface.py
   - List all available methods
   - Understand what each does

2. FOR EACH interaction needed:
   - CHECK: Does BI already have this method?
   - IF YES: Use it directly
   - IF NO: STOP and ask user (see below)

3. NEVER write workarounds without asking:
   ❌ import time / time.sleep()
   ❌ Manual polling loops
   ❌ Direct WebDriver calls in POM
   ❌ Custom wait implementations

4. IF BI method missing, ASK USER:
   "Need BrowserInterface method: [description]

   Use case: [what you're trying to do]
   Proposed signature: [method_name(params)]

   Options:
   1. Add this method to BrowserInterface
   2. Use existing method [alternative] instead
   3. Other approach

   Which option?"

5. WAIT for user response before proceeding
```

### D.3 Build Modules

**⛔ PREREQUISITE: /qa-pre-construction checkpoint MUST be complete before this section.**

```
AFTER completing /qa-pre-construction checkpoint (including reuse check):

BUILD POM:
- Create page class with discovered elements as locators
- Add atomic action methods (enter_*, click_*)
- Add state-check methods from expected_states
- Use ONLY BrowserInterface methods for interactions
- Save to framework/pages/{workflow}/

BUILD TASK:
- Create task class composing the POM
- Add workflow method using POM actions
- NO locators in tasks (DD-27)
- NO direct browser calls - use POM methods only
- Save to framework/tasks/{workflow}/

BUILD ROLE:
- Create role class composing the Task
- Add role workflow method
- Save to framework/roles/{workflow}/

BUILD TEST:
- Create test using Role
- AAA pattern (Arrange/Act/Assert)
- Assert via POM state-check methods
- Save to tests/{workflow}/
```

---

## E. State Management

| Field | Value |
|-------|-------|
| **State Saved** | `discovered_elements`, `pom_path`, `task_path`, `role_path`, `test_path` |
| **When Saved** | After each module constructed |
| **State Location** | `tests/_state/workflow_state.json` |

```json
{
  "step": 4,
  "status": "complete",
  "data": {
    "discovered_pages": {
      "LoginPage": {
        "input_elements": [...],
        "output_elements": [...]
      }
    },
    "files_created": [
      "framework/pages/auth/login_page.py",
      "framework/tasks/auth/auth_tasks.py",
      "framework/roles/auth/registered_user.py",
      "tests/auth/test_login.py"
    ]
  }
}
```

---

## F. Teaching & Learning

**What Agent Learns:**

| Signal | Lesson |
|--------|--------|
| Element not found in snapshot | Page needs more preparation before snapshot |
| Dynamic element appears after action | Need to wait for async content |
| Form submission fails | Check credential strategy and test data |
| Same element found multiple times | Locator needs to be more specific |

**Lessons to Record:**
- Element patterns for this page type
- Wait strategies that work
- Locator patterns that are stable

---

## G. Validation Criteria

| Phase | Rule | On Failure |
|-------|------|------------|
| Discovery | At least 1 input element | AI retries preparation |
| Discovery | At least 1 output element | AI triggers action, retries |
| Construction | POM has locators | AI fixes module |
| Construction | Task has NO locators | AI fixes module |

**Blocking Rule:** Cannot proceed to Step 5 until all modules valid.

---

## H. HITL Triggers

**When ANY failure occurs during discovery:**
1. **STOP** - Do not attempt autonomous fixes
2. **REPORT** - Show user exactly what failed
3. **WAIT** - Get human decision before proceeding

```
===== DISCOVERY FAILURE =====
What happened: [Specific failure]
Where: [URL, element, action]
Error: [Exact error message]

HOW SHOULD WE PROCEED?
1. AI Investigates - I analyze and propose fix
2. Provide Guidance - You tell me what you see
3. Skip + Continue - Proceed without this element
4. Abort - Stop workflow entirely
```

---

## I. User Communication

**Discovery Progress:**
```
⚙ Step 4: Discovering Elements...
  • Page: LoginPage
  • URL: https://...
```

**Construction Progress:**
```
⚙ Step 4: Building POM...
  • Page: LoginPage
  • Elements: 18 inputs, 4 outputs
```

**Complete:**
```
✓ Step 4: Collaborative Construction
  • POM: LoginPage (18 elements)
  • Task: AuthTasks.login()
  • Role: RegisteredUser.login()
  • Test: test_login.py
```

---

## Flow Diagram

```
  Credential Handling
      │
      ▼
  PASS 1: Input Discovery
      │
      ▼
  PASS 2: Output Discovery
      │
      ▼
  Checkpoint (both passes complete?)
      │
  ┌───┴───┐
  ▼       ▼
 YES     NO → Continue discovery
  │
  ▼
  ⛔ /qa-pre-construction (BLOCKING)
      │
      ├── Step 0: Reuse Check
      │       │
      │   ┌───┴───┐
      │   ▼       ▼
      │  NONE   FOUND → HITL (reuse/consolidate/create)
      │   │       │
      │   └───┬───┘
      │       │
      ├── Step 1: Read References
      ├── Step 2: Check BrowserInterface
      └── Step 3: Confirm Checklist
           │
           ▼
  Construction Phase (D.3)
      │
  ┌───┴────┬────┬────┐
  ▼        ▼    ▼    ▼
 POM    Task  Role  Test
  │        │    │    │
  └────────┴────┴────┘
           │
           ▼
      Validate all modules
           │
       ┌───┴───┐
       ▼       ▼
     PASS    FAIL → HITL
       │
       ▼
    STEP 5
```

---

## Extended References

| Reference | Content |
|-----------|---------|
| `step-04-multipage.md` | DD-44 Multi-Page Scope Discovery |
| `step-04-twopass.md` | DEF-045 Two-Pass Discovery |
| `step-04-contracts.md` | Data Contracts |

---

*Next: Step 5 - Test Execution & HITL*
