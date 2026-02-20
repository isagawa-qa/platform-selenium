<!-- SPDX-License-Identifier: MIT -->

# Step 1: User Input

**Purpose:** Capture test requirement, persona, URL, and workflow identifier from user.

**Workflow Version:** v4.0 (5-Step Pair Programming Workflow)

---

## A. Identity & Flow

| Field | Value |
|-------|-------|
| **Step** | 1 - User Input |
| **Dependencies** | None (first step) |
| **Input** | User describes test requirement |
| **Output** | `persona`, `URL`, `role_name`, `workflow`, `raw_requirement`, `detected_env_id` |

---

## B. Persona Map

| Persona | Actions |
|---------|---------|
| **User** | Describes test requirement (persona, action, URL) |
| **AI** | Asks questions, extracts data, auto-detects environment, validates, saves state |

---

## C. Skill Instruction

```
PRE-CHECK:
- DEF-063: Clear session marker if starting NEW workflow (not retry)
  - If tests/_state/.current_run_id exists and previous workflow completed Step 1
    → delete marker

ACTION:
- ASK user: "What test do you want to create?"
  Format: "As a [persona], I want to [action]"
  Example: "As a sales representative, I want to submit a service inquiry"

- ASK user: "What is the URL for this action?"

- ASK user: "Workflow identifier?"
  Explanation: "Creates folders at framework/pages/{workflow}/ and tests/{workflow}/"

- EXTRACT from requirement:
  - persona: From "As a [X]" pattern
  - role_name: PascalCase conversion (sales representative → SalesRepresentative)
  - raw_requirement: Full user requirement verbatim

- AUTO-DETECT environment:
  - Check URL against framework/resources/config/environment_config.json
  - If match found → detected_env_id = environment name
  - If no match → ASK user: "Unknown environment. Create config for '{domain}'?"

VALIDATE (see Section F):
- All required fields present and valid
- Save state on validation pass
- Block Step 2 until validation passes

CROSS-WORKFLOW DUPLICATE CHECK (after workflow identified):
- RUN: find framework/pages -name "*.py" -not -name "__init__.py"
- RUN: find framework/tasks -name "*.py" -not -name "__init__.py"
- RUN: find framework/roles -name "*.py" -not -name "__init__.py"
- CHECK: Same filename in different workflow folders = DUPLICATE
- IF DUPLICATE FOUND in ANY layer: Present HITL (see Section J)
- This runs ONCE per workflow, not per test

RETRY:
- If validation FAIL: RE-ASK the invalid/missing field
- No max retries (user provides input)
```

---

## D. State Management

| Field | Value |
|-------|-------|
| **State Saved** | `persona`, `URL`, `role_name`, `workflow`, `raw_requirement`, `detected_env_id` |
| **When Saved** | After validation passes |
| **State Location** | `tests/_state/workflow_state.json` |

```json
{
  "step": 1,
  "status": "complete",
  "data": {
    "persona": "sales representative",
    "URL": "https://example.com/inquiries",
    "role_name": "SalesRepresentative",
    "workflow": "helios8",
    "raw_requirement": "As a sales representative, I want to submit a service inquiry",
    "detected_env_id": "helios1"
  }
}
```

---

## E. Teaching & Learning

**What Agent Learns:**

| Signal | Lesson |
|--------|--------|
| User provides incomplete persona | Re-ask with example format - users need guidance |
| URL doesn't match known environment | Opportunity to expand environment config |
| Workflow name conflicts with existing | Check existing structure before creating new |

**Lessons to Record:**
- Common persona patterns for this domain
- URL patterns that map to environments
- Workflow naming conventions that work

---

## F. Validation Criteria

| Field | Rule | On Failure |
|-------|------|------------|
| `persona` | Must be present, from "As a [X]" pattern | RE-ASK with example |
| `URL` | Must be valid HTTP/HTTPS URL | RE-ASK for valid URL |
| `role_name` | Must be PascalCase conversion | Auto-fix from persona |
| `workflow` | Alphanumeric + hyphen/underscore | RE-ASK with examples |

**Blocking Rule:** Cannot proceed to Step 2 until all fields valid.

---

## G. Error Handling

| Issue | Behavior |
|-------|----------|
| User skips persona | RE-ASK: "I need a persona. Example: 'As a sales representative, I want to...'" |
| Missing URL | RE-ASK: "What is the URL where this action happens?" |
| Invalid URL format | RE-ASK: "Please provide a valid HTTP/HTTPS URL" |
| Missing workflow | RE-ASK: "What workflow identifier? (e.g., helios7, checkout-v2)" |
| Unknown environment | ASK: "Create environment config for '{domain}'? (yes/no)" |

---

## H. Environment Auto-Detection

1. Extract domain from URL
2. Check `framework/resources/config/environment_config.json` for matching base_url
3. If match found → `detected_env_id` = environment name
4. If no match → Ask user to create new environment config

---

## I. User Communication

**Output Format:**
```
✓ Step 1: User Input
  • Persona: sales representative
  • Role: SalesRepresentative
  • Workflow: helios8
  • Environment: helios1
```

---

## Flow Diagram

```
  User describes requirement
      │
      ▼
  AI extracts persona, asks for URL, workflow
      │
      ▼
  Auto-detect environment
      │
      ▼
  Validate all fields
      │
  ┌───┴───┐
  ▼       ▼
PASS    FAIL → RE-ASK
  │
  ▼
State saved → STEP 2
```

---

## J. Cross-Workflow Duplicate Check

**When:** After workflow is identified, before proceeding to Step 2.

**Scan all three layers:**
```bash
find framework/pages -name "*.py" -not -name "__init__.py"
find framework/tasks -name "*.py" -not -name "__init__.py"
find framework/roles -name "*.py" -not -name "__init__.py"
```

**Check for duplicates:** Same filename in different workflow folders.

**If duplicates found, present HITL:**

```
CROSS-WORKFLOW DUPLICATES DETECTED
==================================

Layer: Pages
  login_page.py exists in:
    → framework/pages/goal_management/login_page.py
    → framework/pages/lead_capture/login_page.py

Layer: Tasks
  (none found)

Layer: Roles
  (none found)

Generic modules should be consolidated to common/ folders.

OPTIONS:
1. CONSOLIDATE NOW - Move duplicates to common/, update all imports
2. CONTINUE - Proceed with workflow, consolidate later (technical debt)

Which option? (1/2):
```

**If user chooses CONSOLIDATE:**
1. Create `framework/pages/common/`, `framework/tasks/common/`, `framework/roles/common/` as needed
2. Move duplicate module to common/ folder
3. Update ALL imports across ALL workflows
4. Delete the duplicates
5. Run tests to verify nothing broke

**Generic modules (should be in common/):**
- Pages: LoginPage, LogoutPage, NavigationPage, HeaderPage, SearchPage
- Tasks: AuthTasks (login/logout), NavigationTasks
- Roles: (typically workflow-specific, but shared auth roles could be common)

---

*Next: Step 2 - Pre-flight Configuration*
