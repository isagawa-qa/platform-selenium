# Mission Control: VS Code Webview Panel

## Context
A VS Code WebviewPanel that tails `events.jsonl` and displays a live timeline of kernel activity. This is the observability layer — see exactly what the agent is doing, task-by-task.

## Requirements
- Add a WebviewPanel to the VS Code extension (sidebar view or panel command)
- Tails `.claude/state/events.jsonl` via file watcher
- Shows a scrolling timeline of events with color coding
- Shows current task from `platform_selenium_workflow.json` if cycling is active

## UI Layout

```
┌─────────────────────────────────────┐
│ MISSION CONTROL          [↺] [⏸]   │
├─────────────────────────────────────┤
│ ⚓ Anchored  │ 4/10 actions          │
│ Domain: platform_selenium            │
├─────────────────────────────────────┤
│ LIVE EVENTS                         │
│ 10:01:44  ✓ Write  framework/...   │
│ 10:01:55  ✓ Bash   pytest tests/   │
│ 10:02:01  ✗ BLOCKED anchor needed  │
│ 10:02:05  ⚓ anchor invoked         │
│ 10:02:10  ✓ Edit   .claude/hooks/  │
└─────────────────────────────────────┘
```

## Acceptance Criteria
- [ ] Panel opens via command palette: "Mission Control: Open"
- [ ] Shows current anchored state and actions counter
- [ ] Events stream in real-time as `events.jsonl` is appended
- [ ] Color coding: green=pass, red=blocked/fail, blue=anchor/learn
- [ ] Pause button stops auto-scroll (allows reading history)
- [ ] Refresh button reloads state from disk

## Completion Signal
When all acceptance criteria are met, invoke `/kernel/complete`.
