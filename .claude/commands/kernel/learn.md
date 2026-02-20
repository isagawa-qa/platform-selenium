# /kernel/learn

Update protocol AND hooks after fixing any failure. Make the same mistake impossible.

## Instructions

1. **Identify what failed:**
   - Error message
   - Root cause
   - How it was fixed

2. **Update protocol:**

   Open `.claude/protocols/[domain]-protocol.md` and add to "Lessons Learned":

   ```markdown
   ### [Date] [Issue Name]
   - **Issue:** What happened
   - **Root Cause:** Why it happened
   - **Fix:** How it was resolved
   - **Anti-Pattern Added:** What to avoid
   - **Quality Gate Added:** What to check
   ```

3. **Update hooks if enforceable:**

   If this failure could be automatically prevented:

   ```python
   # Add to PROTECTED_PATHS in [domain]-gate-enforcer.py
   PROTECTED_PATHS['new/path/'] = 'new_state_key'
   ```

4. **Create new command if recurring:**

   If this is a pattern that needs checking:
   - Create `.claude/commands/[domain]-check-[issue].md`

5. **Update state:**

   Update `.claude/state/session_state.json`:
   ```json
   {
     "needs_learn": false,
     "needs_learn_reason": null
   }
   ```

   Update `.claude/state/[domain]_workflow.json`:
   ```json
   {
     "lesson_recorded": true,
     "lessons_count": N,
     "last_lesson": "Issue name",
     "last_lesson_timestamp": "...",
     "hooks_updated": true | false
   }
   ```

6. **Report:**
   ```
   LESSON RECORDED

   Issue: [what failed]
   Root Cause: [why]
   Fix: [how resolved]

   Protocol updated:
   - Added anti-pattern: [description]
   - Added quality gate: [description]

   Hooks updated: [yes/no]
   - [what was added if yes]

   New command created: [yes/no]
   - [command name if yes]

   Proceeding.
   ```

## State File Location

`.claude/state/[domain]_workflow.json`

## When to Invoke

- After fixing any test failure
- After fixing any error
- After discovering an anti-pattern
- NEVER skip this after a fix
