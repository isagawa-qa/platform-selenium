# /kernel/anchor

Re-center on protocol. Invoke at session start, every 5 actions, or when context drifts.

## Instructions

### Part A: Refresh Protocol

1. **Read protocol:**
   - Open `.claude/protocols/[domain]-protocol.md`
   - Read entire file

2. **Summarize key points:**
   - Architecture patterns
   - Naming conventions
   - Quality gates
   - Anti-patterns to avoid

3. **Review Lessons Learned:**
   - Read "Lessons Learned" section
   - Note any recent additions
   - These are mistakes to avoid

### Part B: Check Recent Work (if any)

4. **Review recent work:**
   - What files were created/modified since last anchor?
   - If none, skip to Step 7

5. **Check against protocol:**

   | Check | Status |
   |-------|--------|
   | Naming conventions followed? | ✓/✗ |
   | Architecture patterns matched? | ✓/✗ |
   | Anti-patterns avoided? | ✓/✗ |
   | Quality gates passed? | ✓/✗ |

6. **If violation found:**
   - STOP
   - Set `needs_learn: true, needs_learn_reason: "anchor_violation"` in session_state.json
   - Fix the violation
   - Invoke `/kernel/learn` to record lesson (this clears the block)
   - Then continue

### Part C: Reset and Proceed

7. **State current task:**
   - What are you about to do?
   - How does it fit the protocol?

8. **Update state:**

   Update `.claude/state/[domain]_workflow.json`:
   ```json
   {
     "anchored": true,
     "anchor_timestamp": "...",
     "actions_since_anchor": 0
   }
   ```

   If resuming from restart, also update `.claude/state/session_state.json`:
   ```json
   {
     "needs_restart": false,
     "resume_after_restart": null
   }
   ```

9. **Confirm:**
   ```
   ANCHORED: [domain]

   Key patterns:
   - [pattern 1]
   - [pattern 2]

   Lessons to remember:
   - [lesson 1]
   - [lesson 2]

   Files checked: N (0 if fresh session)
   Violations: 0 | N

   Current task: [what you're doing]

   Proceeding with protocol.
   ```

## State File Location

`.claude/state/[domain]_workflow.json`

## When to Invoke

- After `/kernel/session-start` (mandatory - hook enforced)
- Every 5 actions (Write, Edit, Bash) - hook enforced
- After any failure (before fixing)
- When resuming from break
- When context seems off

## Unified Re-centering

This command combines:
- **Protocol refresh** (Part A)
- **Work quality check** (Part B - from old validate)

One command, one counter, one mechanism.
