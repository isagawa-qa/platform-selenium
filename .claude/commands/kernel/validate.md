# /kernel/validate

## ⚠️ DEPRECATED

**This command has been merged into `/kernel/anchor` (Part B).**

- 5-action re-centering → use `/kernel/anchor`
- Quality check before done → anchor Part B covers this
- Final gate → use `/kernel/complete`

**Do NOT use this command. It will be removed in a future version.**

---

## Original Documentation (for reference only)

Check work against protocol. Invoke every 5 files or when unsure.

## Instructions

1. **Read protocol:**
   - Open `.claude/protocols/[domain]-protocol.md`
   - Focus on: Anti-Patterns, Quality Gates

2. **Review recent work:**
   - What files were created/modified since last anchor?
   - List them

3. **Check against protocol:**

   | Check | Status |
   |-------|--------|
   | Naming conventions followed? | ✓/✗ |
   | Architecture patterns matched? | ✓/✗ |
   | Anti-patterns avoided? | ✓/✗ |
   | Quality gates passed? | ✓/✗ |

4. **If violation found:**
   - STOP
   - Fix the violation
   - Invoke `/kernel/learn` to record lesson
   - Then continue

5. **Update state:**
   ```json
   {
     "last_validate": "...",
     "files_since_validate": 0,
     "violations_found": 0 | N
   }
   ```

6. **Report:**
   ```
   VALIDATE: [domain]

   Files checked: N
   Violations: 0 | N

   [If violations:]
   - [violation 1] → Fixed, invoking /kernel/learn

   [If clean:]
   Continuing.
   ```

## When to Invoke

- After every 5 files written
- Before `/kernel/complete`
- When something feels off
- After complex changes

## Self-Catch Mechanism

This is where you catch your own mistakes:
- Protocol tells you what's right
- You compare your work
- Violations trigger `/kernel/learn`

No hook can catch everything. This is your self-discipline checkpoint.
