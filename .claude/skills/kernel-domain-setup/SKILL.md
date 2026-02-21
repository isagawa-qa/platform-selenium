# Kernel Domain Setup

Set up QA Test Automation domain enforcement by discovering and indexing repo content.

## Overview

This skill guides the agent through setting up domain-specific enforcement for the QA test automation framework. It creates an indexed protocol, wraps commands for kernel loop enforcement, and establishes the self-improvement infrastructure.

## Steps

| Step | Action | Reference |
|------|--------|-----------|
| 1 | Verify prerequisites | → `references/step-01-prerequisites.md` |
| 1b | Verify CLAUDE.md | → `references/step-01b-verify-claude-md.md` |
| 2 | Discover repo structure | → `references/step-02-discover.md` |
| 3 | Read reference code | → `references/step-03-read.md` |
| 4 | Extract patterns | → `references/step-04-extract.md` |
| 5 | Understand enforcement | → `references/step-05-enforcement.md` |
| 6 | Read workflow | → `references/step-06-workflow.md` |
| 7 | Build protocol | → `references/step-07-protocol.md` |
| 8 | Wrap commands | → `references/step-08-commands.md` |
| 9 | Update state | → `references/step-09-state.md` |
| 10 | Report & restart | → `references/step-10-report.md` |

## Execution

1. **Check for resume state:**
   - Read `.claude/state/session_state.json`
   - If `resume_step` exists, skip to that step
   - Clear `resume_step` after reading

2. **Execute steps sequentially:**
   - Read each reference file before executing that step
   - If restart needed mid-skill, set `resume_step` in state

## Key Principles

- **Protocol = Index** - Point to files, don't duplicate content
- **200-line threshold** - Split files when they exceed this
- **Dynamic categories** - Create new folders for emerging content
- **Self-improvement** - Lessons learned accumulate via `/kernel/learn`

## Outcome

After completion:
- Protocol created at `.claude/protocols/qa-protocol.md`
- Lessons folder at `.claude/lessons/`
- Commands wrapped for kernel loop enforcement
- State files updated
- **Restart required** for hooks to load
