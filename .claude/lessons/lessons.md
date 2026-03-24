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

## LESSON 004 — selenium-python314-none-return — 2026-03-16

**What failed:** `AttributeError: 'NoneType' object has no attribute 'is_displayed'` inside `EC.visibility_of_element_located` during `wait_for_hub_loaded`. Test failed in 6s despite a 15s timeout.

**Root cause:** Two compounding issues:
1. Selenium 4.41.0 + Python 3.14.3 — `find_element()` inside the `EC.visibility_of_element_located` predicate returns `None` instead of raising `NoSuchElementException`. `WebDriverWait` only catches `WebDriverException` subclasses; `AttributeError` is not one, so it propagates immediately without retrying.
2. `driver.implicitly_wait(10)` set in `create_driver()` conflicts with explicit `WebDriverWait` usage. Mixing implicit and explicit waits is a Selenium anti-pattern that can cause unpredictable behaviour.

DOM inspection via Playwright confirmed `a[href='/assistant']` IS present and visible — the locator is correct. The failure is purely a Selenium/Python version compatibility issue.

**Fix applied:** Remove `driver.implicitly_wait(10)` from `create_driver()`. Add `StaleElementReferenceException` and `AttributeError` to `WebDriverWait`'s `ignored_exceptions` in `wait_for_element_visible` and `is_element_displayed` in `BrowserInterface`, or wrap the EC predicate call to catch `AttributeError` and treat it as not-yet-ready.

**Prevention:**
- Never mix `implicitly_wait` with `WebDriverWait` explicit waits — remove implicit wait from `create_driver()`.
- When upgrading Selenium or Python, run the full test suite immediately to catch EC predicate behaviour changes.
- Use Playwright browser inspection to confirm locators are correct before debugging Selenium internals.

---

## LESSON 005 — framework-init-absolute-import — 2026-03-15

**What failed:** `ModuleNotFoundError: No module named 'framework'` during pytest collection. All tests blocked.

**Root cause:** `framework/interfaces/__init__.py` used `from framework.interfaces.browser_interface import BrowserInterface`. `conftest.py` adds `framework/` (not project root) to `sys.path`, so `framework` is not a discoverable module from within its own tree.

**Fix applied:** Changed to relative import: `from .browser_interface import BrowserInterface` in `framework/interfaces/__init__.py`.

**Anti-Pattern:** Never use absolute `from framework.X import Y` paths inside `framework/` package files. When `framework/` is the sys.path root, `framework` is not a module — its children are the top-level modules.

**Quality Gate:** When writing or editing any `framework/**/__init__.py`, imports must use relative form (`from .module import X`) not absolute `from framework.module import X`.

---

## LESSON 006 — playwright-snapshot-shows-values-not-text — 2026-03-16

**What failed:** `NoSuchElementException` from `select.select_by_visible_text('PRODUCT')` — option not found in the project filter `<select>`.

**Root cause:** Playwright's accessibility snapshot reports `<option>` elements by their accessible *name* (which defaults to the option's `value` attribute when no explicit label is set), NOT the visible text that `select_by_visible_text` matches against. The actual visible text of the options was "Product Management", "RLC Pro AI", etc. — not the shortcodes "PRODUCT", "RLCAI" seen in the Playwright snapshot.

**Fix applied:** Used `document.querySelectorAll('select')` via `mcp__playwright__browser_evaluate` to read the true `<option>` text values. Updated the test to use the correct visible text `"Product Management"`.

**Prevention:** When using Playwright DOM inspection to derive `<select>` option text for `select_by_visible_text`, ALWAYS verify with `browser_evaluate` JavaScript (`Array.from(s.options).map(o => o.text)`) rather than trusting the accessibility snapshot, which shows the `value` attribute / accessible name, not the displayed text.

---

## LESSON 007 — xpath-apostrophe-in-dynamic-string — 2026-03-16

**What failed:** `is_quick_action_visible("Today's schedule")` silently returned False — the button was present but the visibility check reported it absent.

**Root cause:** Dynamic XPath generation using f-string with single-quoted XPath literal:
```python
f"//button[normalize-space(text())='{action_name}']"
```
When `action_name = "Today's schedule"`, the generated XPath becomes:
`//button[normalize-space(text())='Today's schedule']` — the apostrophe breaks the XPath string literal, making the expression invalid. Selenium's `is_element_displayed` catches the resulting `InvalidSelectorException` and returns `False`.

**Fix applied:** In `AssistantPage.is_quick_action_visible()`, replaced dynamic XPath f-string with a dict lookup against the pre-defined class-level locators (same dict used by `click_quick_action`). This eliminates runtime XPath string construction entirely.

**Prevention:** Never construct XPath string literals dynamically using f-strings when the input value may contain apostrophes or special characters. Use a pre-defined locator dict keyed on the label, OR escape with `concat()`:
```python
# Safe: dict lookup
action_map = {"Today's schedule": self.QUICK_ACTION_SCHEDULE, ...}
# Unsafe: f-string XPath
f"//button[normalize-space(text())='{label}']"  # breaks on apostrophe
```

---

## LESSON 008 — new-button-auto-thinking — 2026-03-16

**What failed:** `assert not self.assistant_page.is_thinking()` failed after clicking the "New" button — `is_thinking()` returned True.

**Root cause:** The "New" button does not just clear the chat — it starts a new conversation which causes Tiffany to auto-generate a welcome message, triggering a "Thinking" indicator immediately. The test asserted negative thinking state right after clicking New, but the app design fires off a new AI call on reset.

**Fix applied:** Removed the `not is_thinking()` assertion from `test_new_button_resets_conversation`. The meaningful assertions are: (1) URL is still `/assistant`, and (2) the chat input is ready (confirmed by `wait_for_assistant_page()` inside `start_new_conversation`).

**Prevention:** Do not assert `not is_thinking()` immediately after triggering any action that may cause the assistant to auto-generate. If you need to verify "Tiffany is not thinking", first wait for any in-progress thinking to resolve with `wait_for_response()` before asserting. Prefer asserting the positive desired state (e.g., input is ready, URL is correct) over asserting the absence of a transient state.

---
