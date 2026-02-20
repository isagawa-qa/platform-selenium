<!-- SPDX-License-Identifier: MIT -->

# Step 5: Test Execution & HITL Iteration

**Purpose:** Execute test, validate results with HITL triage for failures, iterate through pair programming loop.

**Workflow Version:** v4.0 (5-Step Pair Programming Workflow)

---

## A. Identity & Flow

| Field | Value |
|-------|-------|
| **Step** | 5 - Test Execution & HITL Iteration |
| **Dependencies** | Step 4 complete (all modules generated and saved) |
| **Input** | Test files from Step 4, workflow state |
| **Output** | Test execution result, HITL triage decisions (if failure) |

---

## B. Persona Map

| Persona | Actions |
|---------|---------|
| **User** | Reviews results, makes triage decisions on failures |
| **AI** | Executes test, analyzes results, presents triage options |

---

## C. Skill Instruction

```
PRE-CHECK:
- Verify Step 4 complete (all files saved)
- Verify test file path exists

ACTION (2-STEP SEQUENCE):
1. EXECUTE pytest via Bash:
   - Command: python -m pytest {test_path} -v --env={env} --headless=False
   - Capture exit code and output
   - Construct test_result:
     {
       "status": "passed" | "failed" | "crashed",
       "exit_code": <exit_code>,
       "output": <stdout + stderr>,
       "duration": <execution time>,
       "failure_data": <parse from output if failed>
     }

2. VALIDATE test_result:
   - IF passed -> WORKFLOW COMPLETE
   - IF failed -> HITL triage workflow

HITL TRIAGE OPTIONS (on test failure):
1. Application Defect - Log defect, block workflow
2. Test Issue - AI fixes test code, retry
3. Investigate - Show full diagnostic data
4. Other - User describes action

RETRY POLICY:
- Error signature tracking (MD5 hash)
- Max 2 retries per unique error signature
- Flaky test detection (passes after retry)

COMPLETION CRITERIA:
- ONLY mark Step 5 complete if test passes
- DO NOT mark complete on failure
- Workflow status "AWAITING TRIAGE" until test passes
```

---

## D. State Management

| Field | Value |
|-------|-------|
| **State Saved** | `test_result`, `triage_decision`, `retry_count` |
| **When Saved** | After test execution |
| **State Location** | `tests/_state/workflow_state.json` |

**Pass State:**
```json
{
  "step": 5, "status": "complete",
  "data": {
    "test_result": {"status": "passed", "exit_code": 0, "duration": 2.3},
    "triage_decision": null,
    "retry_count": 0
  }
}
```

**Failure State:**
```json
{
  "step": 5, "status": "awaiting_triage",
  "data": {
    "test_result": {"status": "failed", "exit_code": 1, "failure_data": {...}},
    "diagnostic_data": {...},
    "ai_analysis": {"likely_cause": "...", "confidence": 75}
  }
}
```

---

## E. Teaching & Learning

**What Agent Learns:**

| Signal | Lesson |
|--------|--------|
| Test passes first time | Construction phase produced valid code |
| Element not found error | Locator may have changed or be dynamic |
| Assertion failed | Expected state doesn't match actual |
| Timeout error | Page load or element wait needs adjustment |
| Same error twice | This isn't a flaky test - need real fix |

**Lessons to Record:**
- Common failure patterns for this workflow
- Effective triage decisions
- Fixes that worked

---

## F. Validation Criteria

| Check | Rule | On Failure |
|-------|------|------------|
| `test_result.status` | Must be passed/failed/crashed | Report error |
| `test_result.exit_code` | Must be present | Report error |
| Test passes | status == "passed" | Trigger HITL triage |

**Blocking Rule:** Workflow cannot complete until test passes.

---

## G. HITL Triage Protocol (MANDATORY - NO AUTONOMOUS FIXES)

**CRITICAL: Agent MUST stop and ask on EVERY failure. No exceptions.**

**CHECKPOINT:** On ANY failure, invoke `/qa-on-failure` command FIRST.

This checkpoint provides the exact failure report format and response protocol. Do not skip this checkpoint.

### On Test Failure - STOP IMMEDIATELY

```
1. STOP - Do not attempt ANY fix
2. REPORT - Show exact failure:

   ===== TEST FAILED =====
   Test: [test name]
   Error: [exact error message]
   Location: [file:line]

   AI Analysis: [likely cause]

   HOW SHOULD WE PROCEED?
   1. Application Defect - Log it, stop workflow
   2. AI Proposes Fix - I'll show you what I'd change (you approve)
   3. Investigate - Show me diagnostic data
   4. You Fix - Tell me exactly what to change
   5. Skip - Continue without this test

3. WAIT - Do not proceed without user choice
```

### What "AI Proposes Fix" Means (Option 2):

**CHECKPOINT:** When user selects option 2, invoke `/qa-propose-fix` command.

This checkpoint ensures you show the exact fix and wait for approval before applying.

```
User selects option 2
    │
    ▼
INVOKE /qa-propose-fix checkpoint
    │
    ▼
AI shows PROPOSED fix (does NOT apply it):
    "I would change:
     File: framework/pages/auth/login_page.py
     Line 45: Change XPath from text() to .

     Approve this fix? (yes/no)"
    │
    ├── User says YES → AI applies fix, re-runs test
    │
    └── User says NO → AI asks what to do instead
```

**AI NEVER applies fixes without explicit user approval.**

### Forbidden Behaviors:

- ❌ Attempting fix without showing user first
- ❌ Re-running test after autonomous fix
- ❌ Trying multiple solutions in a loop
- ❌ Assuming user wants AI to "just fix it"
- ❌ Making ANY code change without approval

### Triage Options (All Require User Choice):

| Option | Action | Requires Approval? |
|--------|--------|-------------------|
| **1. Application Defect** | Log to DEFECT_LOG.md, stop | YES (user confirms) |
| **2. AI Proposes Fix** | AI shows fix, waits for approval | YES (before applying) |
| **3. Investigate** | Show diagnostic data | YES (user requests) |
| **4. You Fix** | User describes the fix | YES (user provides) |
| **5. Skip** | Continue without this test | YES (user confirms) |

### Retry Policy:

| Scenario | Behavior |
|----------|----------|
| First failure | Full HITL - present all options |
| After approved fix | Re-run test, report result |
| Fix didn't work | HITL again - do NOT try another fix autonomously |
| Same error 3 times | Escalate - something fundamental is wrong |

---

## H. Diagnostic Data

See `step-05-diagnostics.md` for 7 diagnostic data types.

**Quick Reference:**
1. Error message and stack trace
2. Screenshot at failure point
3. Page HTML/DOM state
4. Network requests log
5. Console errors
6. Element state (visible, enabled, etc.)
7. Timing data (load times, wait times)

---

## I. User Communication

**In Progress:**
```
⚙ Step 5: Executing Test...
  • Test: tests/auth/test_login.py
  • Browser: visible
```

**Complete (Passed):**
```
✓ Step 5: Test Execution
  • Status: PASSED
  • Duration: 12.3s

5-Step QA Workflow Complete!
```

**Failed (Awaiting Triage):**
```
✗ Step 5: Test Execution - FAILED (Awaiting Triage)
  • Assertion: is_logged_in() returned False
  • Next: Choose (1: App Defect, 2: Test Issue, 3: Investigate)
  • Workflow Status: INCOMPLETE
```

---

## Flow Diagram

```
  Verify Step 4 complete
      │
      ▼
  Execute pytest via Bash
      │
      ▼
  Construct test_result
      │
      ▼
  Validate result
      │
  ┌───┴───────────┐
  ▼               ▼
PASSED        FAILED
  │               │
  │               ▼
  │         HITL TRIAGE
  │               │
  │         ┌─────┴─────┬─────────┐
  │         ▼           ▼         ▼
  │    Test Issue   App Defect  Investigate
  │         │           │         │
  │         ▼           ▼         ▼
  │    AI fixes      Log + STOP  Show data
  │    + retry
  │         │
  └─────────┘
      │
      ▼
 WORKFLOW COMPLETE
```

---

## Extended References

| Reference | Content |
|-----------|---------|
| `step-05-diagnostics.md` | 7 Diagnostic Data Types + AI Analysis |
| `step-05-hitl.md` | User Communication + HITL Response Protocol |

---

*Step 5 completes the 5-Step QA Workflow.*
