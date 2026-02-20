<!-- SPDX-License-Identifier: MIT -->

# Step 3: AI Processing

**Purpose:** Transform user requirement into structured metadata (BDD scenarios, expected states, intent).

**Workflow Version:** v4.0 (5-Step Pair Programming Workflow)

---

## A. Identity & Flow

| Field | Value |
|-------|-------|
| **Step** | 3 - AI Processing |
| **Dependencies** | Step 2 complete |
| **Input** | Step 1-2 state (persona, URL, role_name, workflow, raw_requirement) |
| **Output** | `bdd_scenarios`, `expected_states`, `intent` |

---

## B. Persona Map

| Persona | Actions |
|---------|---------|
| **User** | None (unless AI fails 3 times, then user decides resolution) |
| **AI** | Creates BDD scenario, extracts expected_states, determines intent, validates, saves state |

---

## C. Skill Instruction

```
PRE-CHECK:
- Verify Step 2 complete (persona, URL, role_name, workflow exist in state)

ACTION:
- READ raw_requirement from state
- CREATE BDD scenario with Given/When/Then structure
- EXTRACT expected_states from "Then" clauses (DD-09)
- DETERMINE intent (action verb from requirement)

VALIDATE (see Section F):
- BDD structure must be valid
- At least one expected_state
- Intent must be present
- Save state on validation pass

RETRY:
- If validation FAIL: AI retries processing (max 3 attempts)
- After 3 failures: STOP → REPORT → USER DECIDES

POST-ACTION:
- WRITE transcript entry to tests/_reports/<run_id>/workflow_transcript.md
```

---

## D. State Management

| Field | Value |
|-------|-------|
| **State Saved** | `bdd_scenarios`, `expected_states`, `intent` |
| **When Saved** | After validation passes |
| **State Location** | `tests/_state/workflow_state.json` |

```json
{
  "step": 3,
  "status": "complete",
  "data": {
    "bdd_scenarios": [
      {
        "given": "I am on the login page",
        "when": ["I enter valid email", "I enter valid password", "I click login"],
        "then": ["I should see my account dashboard", "I should see logout link"]
      }
    ],
    "expected_states": ["is_on_dashboard", "is_logout_visible"],
    "intent": "login"
  }
}
```

---

## E. Teaching & Learning

**What Agent Learns:**

| Signal | Lesson |
|--------|--------|
| "Then" clause doesn't map to state method | Improve extraction pattern |
| Intent extraction fails | Requirement may need clarification |
| BDD scenario too complex | Consider splitting into multiple scenarios |
| 3 failures in a row | This requirement pattern needs user guidance |

**Lessons to Record:**
- BDD patterns that work for this domain
- Common intent verbs for this workflow
- expected_state naming conventions

---

## F. Validation Criteria

| Field | Rule | On Failure |
|-------|------|------------|
| `bdd_scenarios` | Must have valid Given/When/Then | AI retries |
| `expected_states` | At least one state from "Then" | AI retries |
| `intent` | Action verb extracted | AI retries |

**Blocking Rule:** Cannot proceed to Step 4 until metadata complete.

---

## G. Error Handling

| Attempt | Behavior |
|---------|----------|
| 1-3 | Validation rejects → AI retries processing |
| After 3 | STOP → REPORT → USER DECIDES |

**Error Message Template (After 3 Failures):**
```
"I've attempted 3 times and cannot produce valid metadata.

Here's what I'm generating:
[show failing output]

Validation issue:
[show error]

How should we proceed?
1. Clarify requirement - Go back to Step 1
2. Abort workflow - Stop and log issue"
```

**Note:** No "proceed with incomplete" option. Incomplete data never propagates.

---

## H. BDD Scenario Format

```gherkin
Scenario: [Intent description]
  Given [precondition - page state]
  When [action 1]
  And [action 2]
  Then [expected outcome 1]
  And [expected outcome 2]
```

**Expected States Extraction (DD-09):**
- "I should see my dashboard" → `is_on_dashboard`
- "I should see logout link" → `is_logout_visible`
- "Order should be confirmed" → `is_order_confirmed`

---

## I. User Communication

**Output Format:**
```
✓ Step 3: AI Processing
  • Intent: login
  • Scenarios: 1
  • Expected states: 2 (is_on_dashboard, is_logout_visible)
```

---

## Flow Diagram

```
  Read raw_requirement from state
      │
      ▼
  AI creates BDD scenario
      │
      ▼
  Extract expected_states from "Then"
      │
      ▼
  Determine intent
      │
      ▼
  Validate metadata
      │
  ┌───┴───────────┐
  ▼               ▼
PASS          FAIL (retry)
  │               │
  │         ┌─────┴─────┐
  │         ▼           ▼
  │      Retry 1-3   After 3
  │         │           │
  │         │           ▼
  │         │     USER DECIDES
  │         │
  ▼         │
State saved ←┘
      │
      ▼
   STEP 4
```

---

*Next: Step 4 - Collaborative Construction*
