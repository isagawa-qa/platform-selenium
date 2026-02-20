<!-- SPDX-License-Identifier: MIT -->

# Gate Contract

**Purpose:** Define what an agent builds for each step's gate. Gates are executable - they run within the protocol, validate, teach, and enable learning.

---

## Gate Responsibilities

Every gate MUST do these 6 things:

| # | Action | Description |
|---|--------|-------------|
| 1 | **VALIDATE** | Check input data against criteria |
| 2 | **TEACH** | Record lesson on success or failure |
| 3 | **LEARN** | Send lesson to /kernel/learn for storage |
| 4 | **BLOCK** | Prevent next step if validation fails |
| 5 | **SAVE** | Persist state for next step |
| 6 | **LOOP** | Retry with teaching if recoverable failure |

---

## HITL Protocol (MANDATORY - NO EXCEPTIONS)

**Human-In-The-Loop is NOT optional. Agent MUST stop and ask.**

### On ANY Failure:

```
1. STOP IMMEDIATELY
   - Do NOT attempt autonomous fixes
   - Do NOT loop through solutions
   - Do NOT try "one more thing"

2. REPORT to user:
   "FAILURE at Step [N]: [brief description]

   Error: [exact message]
   Location: [file:line or URL]

   HOW SHOULD WE PROCEED?
   1. I'll fix it - tell me what to change
   2. You investigate - show me more context
   3. Skip this - continue without it
   4. Abort - stop workflow entirely"

3. WAIT for user response
   - Do NOT proceed without explicit user input
   - Do NOT assume user wants you to try fixes

4. ONLY THEN proceed based on user choice
```

### What Agent MUST NOT Do:

- ❌ Loop through multiple fix attempts without asking
- ❌ Try alternate solutions autonomously
- ❌ Assume it knows the right fix
- ❌ Continue past failures hoping they resolve
- ❌ Make more than ONE fix attempt before asking

### Why This Matters:

Pair programming means USER decides direction. Agent executes.
When agent loops autonomously, it's not pair programming - it's solo coding.

---

## BrowserInterface Methods First (MANDATORY)

**Before writing ANY interaction logic in POM:**

```
1. CHECK: Does BrowserInterface already have this method?
   - wait_for_element_visible()
   - wait_for_element_clickable()
   - wait_for_url_contains()
   - click()
   - type_text()
   - is_element_displayed()
   - etc.

2. IF YES: Use it directly
   - self.browser.wait_for_element_visible(*self.LOCATOR)
   - NOT: custom polling loops

3. IF NO: STOP and ask user:
   "Need BrowserInterface method: [description]

   Example: wait_for_new_tab(timeout)

   Should I add this to BrowserInterface?"

4. WAIT for user approval before:
   - Creating workaround code
   - Using time.sleep()
   - Writing manual polling loops
```

### Forbidden Patterns:

```python
# ❌ NEVER do this in POM:
import time
while len(self.browser.get_window_handles()) < 2:
    time.sleep(0.5)  # NO - ask for BI method instead

# ✓ CORRECT - use existing BI method or ask for new one:
self.browser.wait_for_new_window(timeout=10)
```

### Why This Matters:

- BrowserInterface is the single source of browser interaction patterns
- Custom workarounds create inconsistency and technical debt
- If BI is missing a method, adding it benefits ALL future tests

---

## The Learning Cycle

```
Gate executes
    │
    ▼
VALIDATE ──► outcome (pass/fail)
    │
    ▼
TEACH ──► create lesson from outcome
    │
    ▼
LEARN ──► /kernel/learn stores lesson
    │
    ▼
Next execution ──► agent APPLIES stored lessons
    │
    ▼
Better validation ──► fewer failures ──► agent improves
```

---

## Gate Execution Flow

```
Protocol invokes gate
    │
    ▼
APPLY lessons (from previous runs)
    │
    ▼
VALIDATE input against criteria
    │
    ├── PASS ──► TEACH success ──► LEARN ──► SAVE state ──► PROCEED
    │
    └── FAIL ──► Can recover?
                    │
                    ├── YES ──► TEACH fix ──► LEARN ──► LOOP (retry)
                    │
                    └── NO ──► TEACH failure ──► LEARN ──► BLOCK ──► ESCALATE
```

---

## Gate Interface

Agent builds gates as skills/commands:

```
GATE: step_N_gate

INPUT:
  - data: {} (from previous step or user)
  - state: {} (accumulated workflow state)
  - lessons: [] (from /kernel/learn)

OUTPUT:
  - status: PASS | FAIL | RETRY
  - state: {} (updated state to save)
  - lesson: {} (to send to /kernel/learn)
  - next_action: PROCEED | LOOP | BLOCK | ESCALATE
```

---

## Teaching Pattern

Gates create lessons:

```
LESSON:
  step: N
  signal: "What happened"
  outcome: "pass | fail | retry"
  insight: "What to learn"
  apply_when: "When to use this lesson"
```

Example:
```
LESSON:
  step: 1
  signal: "User provided 'login to site' without persona"
  outcome: "fail"
  insight: "Users often skip 'As a [role]' format"
  apply_when: "Step 1 input missing persona pattern"
```

---

## Learning Pattern

Gate sends lesson to /kernel/learn:

```
/kernel/learn receives lesson
    │
    ▼
Stores in domain knowledge (lessons.json or similar)
    │
    ▼
Next gate execution loads stored lessons
    │
    ▼
Gate APPLIES lessons before validating
```

Example application:
```
BEFORE (no lessons):
  - Gate asks "What test do you want to create?"
  - User says "login to site"
  - Gate fails (no persona)

AFTER (lesson applied):
  - Gate asks "What test? Format: 'As a [role], I want to [action]'"
  - User says "As a user, I want to login"
  - Gate passes
```

---

## Validation Criteria Pattern

```
CRITERIA:
  field_name:
    rule: "description of valid state"
    on_fail: "what to do if invalid"
    teach: "lesson to record"
```

---

## Loop Pattern

```
LOOP:
  max_retries: 3
  on_retry:
    - TEACH the fix
    - LEARN from failure
    - APPLY fix (if auto-fixable)
    - RE-VALIDATE
  on_max_retries:
    - TEACH escalation reason
    - LEARN from repeated failure
    - ESCALATE to user (HITL)
```

---

## State Persistence

```
STATE:
  location: "tests/_state/workflow_state.json"
  format:
    step: N
    status: "complete" | "failed" | "retry"
    data: {} (step output)

LESSONS:
  location: "domain lessons storage (via /kernel/learn)"
  format:
    step: N
    lessons: [] (accumulated insights)
```

---

## Building Gates During Domain-Setup

Agent reads workflow.md, then for each step:

1. **READ** step criteria from workflow.md
2. **LOAD** existing lessons from /kernel/learn
3. **BUILD** gate skill/command following this contract
4. **REGISTER** gate with protocol
5. **SAVE** gate to domain folder

---

## Gate Invocation in Protocol

```
/qa-workflow
    │
    ├── load lessons from /kernel/learn
    │
    ├── invoke step_1_gate(user_input, lessons)
    │       └── PASS ──► state saved, lesson sent to /kernel/learn
    │
    ├── invoke step_2_gate(state, lessons)
    │       └── PASS ──► state updated, lesson sent
    │
    └── ... continues through step 5
            │
            ▼
    workflow complete ──► all lessons stored ──► agent smarter next time
```

---

*Agent builds gates. Protocol runs gates. Gates teach. Agent learns. Agent improves.*
