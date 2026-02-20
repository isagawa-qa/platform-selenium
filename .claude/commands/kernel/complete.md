# /kernel/complete

Final gate before marking work done.

## Instructions

1. **Check state:**

   | Gate | Required |
   |------|----------|
   | Protocol created | `protocol_created: true` |
   | Anchored | `anchored: true` |

2. **Update state:**
   ```json
   {
     "complete": true,
     "complete_timestamp": "..."
   }
   ```

3. **Report:**
   ```
   COMPLETE

   Domain: [domain]
   Task: [what was done]
   Files created/modified: [count]
   Lessons learned: [count]

   Done.
   ```

## When to Invoke

- ALWAYS before saying "done"
- NEVER skip this gate
