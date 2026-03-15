# Platform Selenium Protocol

**Domain:** platform_selenium
**Type:** Indexed
**Created:** 2026-03-15

---

## References

### Code Patterns

| Category | Reference |
|----------|-----------|
| Test structure | `tests/pm_assistant/test_pm_assistant_priorities.py` |
| Hook enforcement | `.claude/hooks/universal-gate-enforcer.py` |
| Test failure detection | `.claude/hooks/test-failure-detector.py` |
| VS Code extension | `vscode-extension/src/extension.ts` |

### Architecture

→ `docs/getting-started.md`

### Workflow

| File | Purpose |
|------|---------|
| `.claude/skills/autonomous-cycling/SKILL.md` | Cycling loop behavior |
| `.claude/skills/autonomous-cycling/workflow.md` | Task pick → implement → verify → advance |

### Entry Points

| Command | Purpose |
|---------|---------|
| `/run-test` | Run tests with protocol enforcement |
| `/qa-workflow` | 5-step QA test generation |
| `/kernel/anchor` | Re-read protocol + validate state |
| `/kernel/learn` | Record lesson after fix |
| `/kernel/complete` | Final gate before marking task done |
| `/kernel/autonomous-cycle` | Cycle through all tasks in `tasks/` |

### Task Queue

→ `tasks/` (4 tasks: event stream → status bar → webview → skill palette)

### Lessons Learned

→ `.claude/lessons/lessons.md`

---

*Protocol is an INDEX. Agent reads referenced files during /kernel/anchor.*
