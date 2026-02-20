<!-- SPDX-License-Identifier: MIT -->

# Step 2: Pre-flight Configuration

**Purpose:** Establish credential strategy before test construction begins.

**Workflow Version:** v4.0 (5-Step Pair Programming Workflow)

---

## A. Identity & Flow

| Field | Value |
|-------|-------|
| **Step** | 2 - Pre-flight Configuration |
| **Dependencies** | Step 1 complete |
| **Input** | Step 1 output (persona, URL, workflow) |
| **Output** | `credential_strategy` |

---

## B. Persona Map

| Persona | Actions |
|---------|---------|
| **User** | Answers credential question |
| **AI** | Asks question, validates, scaffolds if needed, saves state |

---

## C. Skill Instruction

```
PRE-CHECK:
- Verify Step 1 complete (persona, URL, workflow exist in state)
- Browser MUST be running (always visible, no headless)

ACTION:
- ASK user: Credential strategy?
  1. Static        - Use existing account from test_users.json
  2. Dynamic       - Register fresh user, save for later tests
  3. Self-contained - Register and use within same test
  4. None needed   - Test doesn't require credentials

DEFAULTS (no questions):
- Browser: Always visible (headless=false)
- Test data: Workflow-specific (tests/{workflow}/data/)

VALIDATE (see Section E):
- Credential strategy must be valid option
- Save state on validation pass
- Scaffold infrastructure if needed

RETRY:
- If validation FAIL: RE-ASK credential question
```

---

## D. State Management

| Field | Value |
|-------|-------|
| **State Saved** | `credential_strategy` |
| **When Saved** | After validation passes |
| **State Location** | `tests/_state/workflow_state.json` |

```json
{
  "step": 2,
  "status": "complete",
  "data": {
    "credential_strategy": "static | dynamic | self-contained | none"
  }
}
```

---

## E. Validation Criteria

| Field | Rule | On Failure |
|-------|------|------------|
| `credential_strategy` | Must be: static, dynamic, self-contained, none | RE-ASK |

**Blocking Rule:** Cannot proceed to Step 3 until credential strategy valid.

---

## F. Teaching & Learning

**What Agent Learns:**

| Signal | Lesson |
|--------|--------|
| User chooses static | Domain has existing test accounts |
| User chooses dynamic | Domain needs registration flow |
| User chooses self-contained | Test is independent |
| User chooses none | No auth required for this test |

---

## G. Infrastructure Scaffolding

| Strategy | Infrastructure Created |
|----------|----------------------|
| `static` or `dynamic` | `tests/data/test_users.json` if missing |
| `self-contained` or `none` | None needed |

---

## H. User Communication

**Output Format:**
```
✓ Step 2: Pre-flight
  • Credentials: static (use existing account)
```

---

## Flow Diagram

```
  Verify browser running
      │
      ▼
  ASK credential strategy
      │
      ▼
  Validate answer
      │
  ┌───┴───────┐
  ▼           ▼
PASS        FAIL
  │           │
  ▼           ▼
Save      RE-ASK
  │
  ▼
STEP 3
```

---

*Next: Step 3 - AI Processing*
