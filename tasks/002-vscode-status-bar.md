# VS Code Status Bar: Kernel State Indicator

## Context
With the event stream in place (Task 001), the VS Code extension can watch `.claude/state/session_state.json` and `events.jsonl` to show real-time kernel state in the status bar — always visible without opening any panel.

## Requirements
- Add a status bar item to the existing `vscode-extension/src/extension.ts`
- Watch `.claude/state/session_state.json` and `platform_selenium_workflow.json` for changes
- Update status bar on file change (no polling)
- Status bar item is clickable → opens the state JSON in editor

## Display Format

| State | Display |
|-------|---------|
| Not started | `⊘ kernel` |
| Anchored, actions 0-7 | `⚓ 4/10` |
| Anchored, actions 8-9 | `⚠ 9/10` (yellow) |
| Needs anchor | `🔴 anchor needed` |
| Needs learn | `🔴 learn needed` |
| Test running | `⟳ testing` |

## Acceptance Criteria
- [ ] Status bar item appears when workspace contains `.claude/state/`
- [ ] Shows current `actions_since_anchor` / `actions_limit`
- [ ] Turns yellow at 80% of limit, red when blocked
- [ ] Shows `needs_learn` state when set
- [ ] Updates within 1 second of state file change
- [ ] Clicking opens `.claude/state/platform_selenium_workflow.json`

## Completion Signal
When all acceptance criteria are met, invoke `/kernel/complete`.
