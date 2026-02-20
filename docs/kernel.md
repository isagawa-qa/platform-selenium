# The Isagawa Kernel

## What It Is

The Isagawa Kernel is a self-building, self-improving, safety-first enforcement system that runs **inside** AI agents. It's not a separate tool or dashboard — it's an operating system for AI execution.

The kernel manages AI behavior through two primitives:

| Primitive | What It Does |
|-----------|-------------|
| **Hook** | Fires on every write/edit, blocks if state is wrong, forces the agent back on track |
| **Anchor** | Reads the protocol, updates state, re-centers the agent on its domain knowledge |

The hook is the enforcement. The anchor is the correction. Together they form the loop.

## How It Works

### The Loop

```
session-start → anchor → WORK → complete
                  ↑         ↓        ↑
                  └── every 10 actions ┘
                           ↓
                 failure? → fix → learn
```

1. **Session start** — check state, restore context from prior sessions
2. **Anchor** — read protocol, verify recent work, re-center
3. **Work** — write code, run tests, iterate
4. **Complete** — save context, run final quality gate

Every 10 actions (writes, edits, shell commands), the hook forces an anchor. This prevents context drift — the AI re-reads its protocol and checks its own work.

### Two-Tier Enforcement

The kernel enforces quality at two levels simultaneously:

**Protocol (soft enforcement):**
- Written in markdown
- The AI reads it and follows it
- Contains architecture patterns, naming conventions, anti-patterns
- Updated after every failure

**Hooks (hard enforcement):**
- Python scripts that fire on Claude Code tool events
- `PreToolUse` — gates writes/edits before they happen
- `PostToolUse` — detects test failures after commands run
- Cannot be bypassed by the AI
- Updated after every failure

### The Learning Cascade

When something goes wrong:

```
Test fails
  → Agent STOPS (doesn't loop)
  → Human reviews the failure
  → Fix is applied
  → Protocol is updated (new pattern or anti-pattern)
  → Hook is updated (new check or gate)
  → The same failure can never happen again
```

This is the key insight: **every failure makes the system permanently stronger in two ways**.

Protocol growth over sessions:

| Session | Protocol Lines | Lessons | Blocked Mistake Types |
|---------|---------------|---------|----------------------|
| 1 | ~80 | 0 | 0 |
| 2 | ~138 | 3 | 3 |
| 5 | ~200+ | 8 | 8+ |
| 10 | ~400+ | 15+ | 15+ |

### Smart Gates

When a hook blocks the AI, it doesn't just say "no." It tells the AI exactly how to fix the problem:

```
BLOCKED: Lesson not recorded (trigger: test_failure)

FIX:
1. Invoke /kernel/learn
2. Record what you learned from the fix
3. Then retry your write

Command: /kernel/learn
```

This is "block + teach" — not just prevention, but guidance.

### Self-Building

The kernel builds its own governance:

1. You start with a blank repo
2. Run `/kernel/domain-setup`
3. The AI analyzes your codebase, extracts patterns, and creates:
   - A protocol file (markdown) with your architecture rules
   - Hook scripts that enforce those rules
   - Commands that manage the workflow
4. From that point on, the AI operates within its self-built structure

The protocol is written in markdown — not code. This means:
- Zero marginal cost to add new rules
- Community members can contribute patterns
- The AI itself proposes updates after failures

## Hooks

### Gate Enforcer (`universal-gate-enforcer.py`)

Runs before every Write, Edit, or Bash command. Checks:

- Has the session been started?
- Is the agent anchored (protocol read)?
- Are there unrecorded lessons (must learn before continuing)?
- Has the action limit been reached (forces re-anchor)?

### Test Failure Detector (`test-failure-detector.py`)

Runs after every Bash command. Checks:

- Did a test command just fail (non-zero exit)?
- If yes, sets `needs_learn: true` in state
- This blocks further writes until the agent records the lesson

## Commands

| Command | Purpose |
|---------|---------|
| `/kernel/session-start` | Check state, restore context, resume |
| `/kernel/anchor` | Re-read protocol, check work, reset counter |
| `/kernel/domain-setup` | Analyze codebase, create protocol + hooks |
| `/kernel/learn` | Record lesson, update protocol + hooks |
| `/kernel/fix` | Impact assessment before any fix |
| `/kernel/complete` | Save context, run final quality gate |

## State Files

All kernel state is stored in JSON files under `.claude/state/`:

- `session_state.json` — session status, context, restart flags
- `[domain]_workflow.json` — anchor status, action counter, lesson tracking

State is explicit, inspectable, and versioned. It proves work was done — no state can be faked because hooks verify it.
