# Skill Palette: Bidirectional Skill Invocation from UI

## Context
Extend the Mission Control panel with a skill palette — clickable buttons that trigger kernel skills. Uses a file-based inbox pattern: UI writes a request to `.claude/state/inbox.json`, the PreToolUse hook detects it and tells the agent to invoke the skill.

## Requirements
- Add skill buttons to the Mission Control webview panel
- Clicking a button writes to `.claude/state/inbox.json`
- Extend `universal-gate-enforcer.py` to check inbox.json and block with the appropriate command
- Result is written to `.claude/state/outbox.json`
- Panel reads outbox.json and shows confirmation

## Skill Buttons

| Button | Skill | When Shown |
|--------|-------|------------|
| Anchor | `/kernel/anchor` | When `anchored: false` |
| Learn | `/kernel/learn` | When `needs_learn: true` |
| Run QA Workflow | `/qa-workflow` | Always |
| Run Tests | `/run-test` | Always |
| View State | inline | Always |

## Inbox Schema

```json
{"skill": "/kernel/anchor", "args": "", "requested_at": "ISO-8601", "status": "pending"}
```

## Acceptance Criteria
- [ ] Clicking "Anchor" writes to inbox.json with `skill: "/kernel/anchor"`
- [ ] Hook detects inbox.json with `status: "pending"` and blocks with the skill command
- [ ] Agent invokes the skill, hook clears inbox (status → "done")
- [ ] Panel updates within 2 seconds of outbox.json change
- [ ] Buttons are disabled (grayed) when a skill is already pending

## Completion Signal
When all acceptance criteria are met, invoke `/kernel/complete`.
