# Event Stream: Extend Hooks to Emit events.jsonl

## Context
The kernel hooks already fire on every Write/Edit/Bash action. We need to extend them to append structured JSON events to `.claude/state/events.jsonl`. This is the telemetry backbone for the Mission Control UI.

## Requirements
- Extend `universal-gate-enforcer.py` to append an event on every action (allowed or blocked)
- Extend `test-failure-detector.py` to append a test result event on test completion
- Each event is a single JSON line (JSONL format) with timestamp, type, and relevant fields
- File rotates at 1000 lines (rename to events.jsonl.bak, start fresh)

## Event Schema

```json
{"ts": "ISO-8601", "type": "action|blocked|test_pass|test_fail|anchor|learn|session_start", "tool": "Write|Edit|Bash", "actions": 4, "limit": 10, "anchored": true, "detail": "..."}
```

## Acceptance Criteria
- [ ] Running any Write/Edit/Bash appends a line to `.claude/state/events.jsonl`
- [ ] Blocked actions append a `blocked` event with reason
- [ ] Test failures append a `test_fail` event with command and exit code
- [ ] Test passes append a `test_pass` event
- [ ] File rotation works when line count exceeds 1000
- [ ] Events are valid JSON (parseable with `json.loads()`)

## Completion Signal
When all acceptance criteria are met, invoke `/kernel/complete`.
