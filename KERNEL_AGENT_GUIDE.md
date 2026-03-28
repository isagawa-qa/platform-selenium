# Isagawa Kernel — Agent Guide

You are an AI agent operating within the Isagawa QA Platform. This file defines how you select the correct framework repo, initialize it, and operate within it. Read this before taking any action in an isagawa-qa workspace.

---

## Step 1: Identify the Correct Framework Repo

Use this decision table to determine which repo applies to the current task:

| If the project needs... | Use this repo |
|------------------------|---------------|
| Browser UI testing (Python) | `isagawa-qa/platform-selenium` |
| Browser UI testing (TypeScript) | `isagawa-qa/platform-playwright` |
| Docker container image validation | `isagawa-qa/platform-docker` |
| SSH-accessible Linux image validation | `isagawa-qa/platform-ssh` |
| LLM pipeline / AI output evaluation | `isagawa-qa/test-platform-deepeval` |

If unclear, ask the developer before proceeding. Do not guess.

---

## Step 2: Verify Checkout

Confirm the repo is checked out locally before taking any action:

```bash
ls /path/to/framework-repo/CLAUDE.md
```

If the file does not exist, the repo is not checked out. Stop and instruct the developer:

```
The [REPO_NAME] repository must be checked out locally before tests can be generated or run.

Clone it:
  git clone https://github.com/isagawa-qa/[REPO_NAME].git

Then activate your Python environment and install dependencies per SETUP.md.
```

---

## Step 3: Initialize

Once checked out, read the framework's integration context:

```
[FRAMEWORK_ROOT]/INTEGRATION.md
```

This file defines:
- How to register the developer's app
- How to run tests
- How to generate tests
- Failure protocol
- Framework constraints (what you may and may not modify)

Do not proceed past this step until you have read `INTEGRATION.md`.

---

## Step 4: Understand the Kernel

Every isagawa-qa framework repo contains the **Isagawa Kernel** — a hook-based enforcement system in `.claude/`. It governs your behavior automatically.

### What the Kernel Does

| Trigger | Effect |
|---------|--------|
| Session start | Requires `/kernel/session-start` before any work |
| Every 10 actions | Blocks writes until you invoke `/kernel/anchor` |
| Test failure | Sets `needs_learn: true`, blocks writes until `/kernel/learn` |
| Anchor violation | Requires `/kernel/learn` before continuing |

### When You See `BLOCKED:`

The kernel has stopped you. The message always includes the exact command to run. Run it immediately. Do not work around it.

```
BLOCKED: 10 actions since last anchor

FIX:
1. Invoke /kernel/anchor
→ /kernel/anchor
```

### Kernel Commands

| Command | When to invoke |
|---------|---------------|
| `/kernel/session-start` | First action of every session |
| `/kernel/anchor` | Every 10 actions (hook-enforced) or when context drifts |
| `/kernel/learn` | After any test failure fix |
| `/kernel/fix` | Before applying any fix — impact assessment |
| `/kernel/complete` | When a task is fully done |

---

## Step 5: Operate Within Framework Constraints

Each repo defines what you may and may not modify. Always read `INTEGRATION.md` for the current repo's constraint list. The general rule across all repos:

**You may generate or modify:**
- Test files (`tests/`)
- Page/module layer files (`framework/pages/` or equivalent)
- Task layer files (`framework/tasks/`)
- Role layer files (`framework/roles/`)
- Test data (`tests/data/`)

**You must not modify:**
- The interface/infrastructure layer (`framework/interfaces/`)
- Core utilities (`framework/resources/`)
- Kernel files (`.claude/`)
- `CLAUDE.md`

---

## Step 6: Document Coverage in the Developer's Project

After generating or running tests, create or update `QA_COVERAGE.md` in the developer's application repo:

```markdown
# QA Coverage

Tests for this project live in the Isagawa [framework-name] framework.
[framework-repo] must be checked out locally to run tests.

## Coverage Map

| Feature | User Story | Test Location |
|---------|-----------|----------------|
| [Feature] | As a [persona], I want to [action] | tests/[appname]/test_[feature].py |

## Running Tests

See [framework-repo]/DEVELOPER_GUIDE.md for setup and execution instructions.
```

This is the only test-related file that belongs in the developer's project.

---

## Failure Protocol

On any test failure, follow HITL — do not auto-fix:

1. **STOP** — halt immediately
2. **REPORT** — test name, error, file location
3. **ANALYZE** — expected vs actual, likely cause
4. **DISCUSS** — ask: log defect in `docs/DEFECT_LOG.md`?
5. **PRESENT OPTIONS** — 2-3 fix approaches with tradeoffs
6. **WAIT FOR APPROVAL** — do not fix until approved
7. **FIX + RE-TEST** — implement approved fix, re-run same tests
8. **LEARN** — invoke `/kernel/learn` to record the lesson

---

## CI/CD Awareness

If the developer asks about running tests in a pipeline, flag this:

> The framework repo must be available in the CI environment. Options:
> - **Git submodule** (recommended) — pins the tested version
> - **Pipeline checkout step** — clones the framework repo before tests run
> - **Shared runner** — machine with all repos permanently available

You cannot configure this automatically. Raise it with the developer.

---

## Reference

| Resource | Location |
|----------|----------|
| Org-level platform guide | `isagawa-qa/.github/PLATFORM_GUIDE.md` |
| Repo setup instructions | `[FRAMEWORK_ROOT]/SETUP.md` |
| Human developer guide | `[FRAMEWORK_ROOT]/DEVELOPER_GUIDE.md` |
| Cross-workspace context | `[FRAMEWORK_ROOT]/INTEGRATION.md` |
| Kernel state | `[FRAMEWORK_ROOT]/.claude/state/` |
| Lessons log | `[FRAMEWORK_ROOT]/.claude/lessons/lessons.md` |
