# Isagawa QA Platform — Lessons Learned

---

## LESSON 001 — pm_assistant_priorities — 2026-03-12

**What failed:** `browser.enter_text()` was called in the POM but does not exist on `BrowserInterface`.

**Root cause:** POM Layer — wrong method name. The canonical reference code uses `enter_text()` in `_reference/pages/*.py`, but the actual `BrowserInterface` class exposes `type()`. The reference files and the implementation were out of sync.

**Fix applied:** Replaced `self.browser.enter_text(...)` with `self.browser.type(...)` in `AssistantPage.enter_message()`.

**Prevention:** When writing POMs for this repo, always verify the method name exists in `framework/interfaces/browser_interface.py` before using it. The correct text-entry method is `browser.type(by, value, text)`.

---

## LESSON 002 — pm_assistant_priorities — 2026-03-12

**What failed:** `TimeoutException` — XPath `(//div[contains(@class,'message') and not(contains(@class,'user'))])[last()]` matched nothing after 60 seconds.

**Root cause:** POM Layer — incorrect locator. The PM Hub chat interface renders all message bubbles as unstyled `div` elements with **no CSS class names at all**. The layout is achieved entirely through inline styles: `justify-content: flex-start` for assistant messages and `justify-content: flex-end` for user messages. The inner bubble carries `background: var(--bg-card-alt)`.

**Fix applied:** Replaced class-based XPath with inline-style-based XPath:
```python
# New locators in AssistantPage
ANY_ASSISTANT_BUBBLE  = (By.XPATH, "//div[contains(@style,'flex-start')]//div[contains(@style,'background')]")
LAST_ASSISTANT_BUBBLE = (By.XPATH, "(//div[contains(@style,'flex-start')]//div[contains(@style,'background')])[last()]")
```
Also increased wait timeout from 60s to 90s to account for Tiffany's live AI response latency.

**Prevention:** For modern JS apps (Next.js, Vite), never assume class names on dynamic content. Always run a DOM inspection via Playwright/browser tools to confirm actual selectors before writing POMs. Pay special attention to CSS-in-JS and inline-style-based layouts which produce zero class names on rendered elements.

---

## LESSON 003 — hook-cwd-mismatch — 2026-03-15

**What failed:** PreToolUse/PostToolUse hooks errored: `can't open file '.claude/hooks/...py' [Errno 2]`. Compile itself succeeded (exit 0).

**Root cause:** Bash command used `cd vscode-extension && npm run compile`. The working directory persists between Bash calls in Claude Code — the CWD moved to `vscode-extension/` and hook commands using relative paths (`python .claude/hooks/...`) could no longer resolve the script. All subsequent Edit, Write, and Bash tool calls were blocked for the rest of the session.

**Fix applied:** Updated `.claude/settings.json` to use absolute paths for both hook commands. Also restores session by restarting Claude Code.

**Prevention:** Never use `cd subdir && command` when subdir is outside workspace root. Instead use `npm --prefix vscode-extension run compile` or equivalent flag that keeps CWD at the workspace root. Hook commands in settings.json must use absolute paths, not relative paths.

---
