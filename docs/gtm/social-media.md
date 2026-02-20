# Social Media GTM Content

Launch content for Isagawa QA Platform across LinkedIn, Reddit, Twitter, and Product Hunt.

---

## 1. LinkedIn Post (200-300 words)

**Target:** Engineering managers, QA leads, SDETs

---

When AI becomes the worker, management must become software.

That's not a metaphor—it's how we built our QA automation platform.

Six months ago, we started using Claude Code to build tests. Fast, productive, incredible velocity. Three months in, the codebase was a mess. Every session, the agent would forget our patterns. Every test looked different. Maintenance became impossible.

The problem wasn't the AI. It was us trying to manage AI like we manage humans—with documentation, code reviews, and hope.

So we built something different: **AI managing AI**. A kernel that runs inside the agent, not outside it. Hooks that enforce architecture at write-time. Protocols that evolve when the system learns from failures. The agent can't skip steps. It can't drift from patterns. It can only do QA right.

This is **AI Execution Management**—a new category that sits between your AI and your code. Not monitoring (watching what happened). Not governance (documenting what should happen). But enforcement: making it impossible for AI to work the wrong way.

We open-sourced the entire platform today:
→ 5-layer Selenium architecture (Interface, Browser, Page, Test, Runner)
→ Self-building governance kernel (the agent creates its own enforcement)
→ Learning loop (every test failure makes the system permanently smarter)
→ MIT license, production-ready

**If you're using AI to write code—any code—this pattern applies.**

Repo: github.com/isagawa-qa/platform
Free demo: We'll set up the kernel for your stack (reach out via Issues)

The future of AI isn't vibe coding. It's building AI that manages AI.

---

## 2. Reddit Posts (4 subreddits)

### r/QualityAssurance

**Title:** Open-sourced our AI-native QA framework. It enforces test architecture via hooks—AI can't skip steps.

---

We've been using Claude Code to generate Selenium tests for about six months. The velocity was incredible—until we hit three months and realized the codebase was unmaintainable. Every test was structured differently. The AI would "forget" our patterns between sessions.

We tried docs. We tried detailed prompts. Nothing stuck.

So we built enforcement at the agent level. It's called the **Isagawa Kernel**, and today we open-sourced the entire thing.

**How it works:**

- The agent has **hooks** that intercept Write/Edit/Bash operations
- Before any file is written, hooks check: Does this follow the architecture? Does it match naming conventions? Does it avoid known anti-patterns?
- If the check fails, the write is **blocked**—the agent physically can't create bad code
- When a test fails, the agent invokes `/kernel/learn`, which updates both the protocol (soft) and the hooks (hard)

**The stack:**

5-layer Selenium architecture:
1. WebInterface (element operations)
2. BrowserInterface (navigation, waits)
3. PageObjects (page-specific logic)
4. Tests (pure assertions, no setup)
5. Runner (pytest + fixtures)

Every layer has strict boundaries. The AI can't put element selectors in test files. It can't put assertions in PageObjects. The hooks enforce this at write-time.

**Why this matters:**

If you're using AI for test automation, you're probably hitting the same wall we did: the AI is fast, but the output drifts. This gives you a way to lock in quality without constant human review.

Repo: github.com/isagawa-qa/platform
MIT license, Python + Selenium + pytest

We're offering free setup demos—open an issue if you want help adapting the kernel to your stack.

---

### r/selenium

**Title:** 5-layer Selenium architecture with AI-powered test generation

---

I've been building Selenium frameworks for years, and the same problem always comes up: tests get brittle, PageObjects get bloated, and maintenance becomes a full-time job.

Then we started using AI (Claude Code) to generate tests. The speed was incredible, but it introduced a new problem: **consistency**. The AI would write tests differently every session. Some put waits in PageObjects. Some put selectors in test files. After three months, the codebase was chaos.

So we built an enforcement layer—and today we open-sourced it.

**The architecture (5 layers):**

```
Runner (pytest + fixtures)
  ↓
Tests (pure assertions, no imports except PageObjects)
  ↓
PageObjects (page-specific flows, delegates to BrowserInterface)
  ↓
BrowserInterface (navigate, wait, execute_script)
  ↓
WebInterface (find, click, send_keys, get_text)
```

**Key pattern:**
Tests **never** import WebInterface or BrowserInterface directly. They only call PageObject methods. PageObjects **never** call `driver.find_element`—they delegate to BrowserInterface or WebInterface.

**Example:**

```python
# tests/test_login.py
def test_successful_login(login_page):
    result = login_page.login("user@example.com", "password123")
    assert result.is_logged_in()

# pages/login_page.py
class LoginPage:
    def login(self, email, password):
        self.browser.navigate("/login")
        self.web.send_keys(self.email_input, email)
        self.web.send_keys(self.password_input, password)
        self.web.click(self.submit_button)
        return DashboardPage(self.browser, self.web)
```

**AI enforcement:**

The repo includes a **kernel** that hooks into Claude Code. Before the agent writes a file, hooks check:
- Is the layer boundary respected?
- Are selectors in PageObjects (not tests)?
- Are assertions in tests (not PageObjects)?

If the check fails, the write is blocked. The agent physically can't create violations.

**Repo:** github.com/isagawa-qa/platform (MIT license)

If you're interested in the pattern but not the AI part, the architecture still applies—it's just standard POM with strict boundaries.

---

### r/softwaretesting

**Title:** Built a self-improving QA agent. It learns from every test failure.

---

We've been using AI (Claude Code) to write Selenium tests for six months. The productivity was unreal—what used to take a day now takes 20 minutes.

But we hit a problem: **the AI doesn't remember**. Every session, it would make the same mistakes. Put selectors in test files. Skip waits. Forget naming conventions.

So we built a learning loop. Today we open-sourced the whole thing.

**How it works:**

1. **Agent writes test** → hooks enforce architecture (5-layer Selenium pattern)
2. **Test runs** → if it fails, hook sets `needs_learn: true`
3. **Agent invokes `/kernel/learn`** → records what went wrong in two places:
   - **Protocol** (markdown file the agent re-reads every session)
   - **Hooks** (Python scripts that block violations at write-time)
4. **Next session** → agent re-reads protocol, hooks enforce new rules

**Example:**

We had a bug where tests would fail intermittently because the agent wasn't waiting for elements to be visible. After the fix, we ran `/kernel/learn`. It added:

- **To protocol:** "Always use `wait_for_visible()` before interacting with dynamic elements"
- **To hook:** Check that PageObject methods call `browser.wait_for_visible()` before `web.click()`

Now the agent **can't** write code that skips visibility waits. The hook blocks it.

**Why this matters:**

Most QA frameworks are static. They encode what you knew on Day 1. This framework evolves—every failure makes it permanently smarter.

**Human-in-the-loop:**

The learning isn't automatic. After a test failure, the agent proposes a protocol update. You review and approve. Then it's locked in via hooks.

**Repo:** github.com/isagawa-qa/platform
Stack: Python, Selenium, pytest, Claude Code
License: MIT

We're offering free setup demos if you want to adapt the kernel to your stack (Playwright, Cypress, whatever). Just open an issue.

---

### r/ClaudeAI

**Title:** Using Claude Code hooks to enforce how AI writes test code

---

I've been using Claude Code for test automation, and it's been incredible—until the codebase hit about 200 files. Then I noticed:

- Every session, Claude would "forget" our architecture patterns
- Some tests put selectors in test files, some in PageObjects
- Some used waits, some didn't
- Naming conventions drifted constantly

I tried adding detailed instructions to CLAUDE.md. It helped for one session, then drifted again.

So I built **enforcement at the hook level**—and today I open-sourced it.

**How it works:**

Claude Code has PreToolUse and PostToolUse hooks. They run before/after every Write, Edit, and Bash operation.

**PreToolUse hook:**
- Intercepts file writes
- Checks content against a protocol (architecture rules, naming conventions, anti-patterns)
- If violation found → **blocks the write** (returns exit code 2)
- Tells Claude exactly how to fix it

**PostToolUse hook:**
- Runs after test commands (pytest, npm test, etc.)
- If exit code ≠ 0 → sets `needs_learn: true` in state
- Blocks next write until Claude invokes `/kernel/learn`

**Example block message:**

```
BLOCKED: Test in wrong layer

tests/test_checkout.py calls driver.find_element() directly.

FIX:
1. Move element selector to PageObject
2. Call PageObject method from test
3. Tests should only import PageObjects, never WebInterface

Protocol: .claude/protocols/qa-protocol.md (Line 47)
```

**The learning loop:**

When a test fails:
1. Claude fixes it
2. Invokes `/kernel/learn`
3. Updates **protocol** (markdown) + **hooks** (Python)
4. Mistake can never happen again—hook prevents it

**Smart gates:**

The hook doesn't just say "blocked." It tells Claude:
- What's wrong
- How to fix it
- Where the rule is documented

This creates a feedback loop: Claude learns, protocol updates, hooks enforce.

**Repo:** github.com/isagawa-qa/platform

The kernel is domain-agnostic. We use it for QA, but the pattern applies to any AI-generated codebase (APIs, frontends, data pipelines, whatever).

**Key files:**
- `.claude/hooks/` — PreToolUse/PostToolUse scripts
- `.claude/protocols/` — Markdown rules Claude re-reads every session
- `.claude/commands/kernel/` — `/anchor`, `/learn`, `/complete`

It's MIT licensed. If you're building anything non-trivial with Claude Code, this pattern will save you.

---

## 3. Twitter/X Thread (8 tweets)

**Thread:**

---

**Tweet 1 (Hook):**

The $5.8B AI governance market is building the wrong thing.

They're building monitors. We need managers.

Here's why—and what we're building instead. 🧵

---

**Tweet 2:**

AI governance tools monitor, document, and alert.

They watch the AI work, log what happened, and tell you when something goes wrong.

That's useful. But it doesn't stop the AI from doing the wrong thing in the first place.

---

**Tweet 3:**

The real problem: AI doesn't remember.

Every session, it forgets your patterns. Docs drift. Code quality degrades. After 3 months, your codebase is unmaintainable.

Monitoring tells you it happened. It doesn't prevent it.

---

**Tweet 4:**

What if the AI couldn't make mistakes?

Not "we'll review it later."
Not "we'll train it better."
But: the system physically blocks bad code at write-time.

That's AI Execution Management.

---

**Tweet 5:**

How it works:

- Hooks intercept Write/Edit operations
- Check against protocol (architecture, naming, anti-patterns)
- If violation → block + tell AI how to fix
- When test fails → AI learns → updates protocol + hooks

The system gets smarter with every failure.

---

**Tweet 6:**

MCP vs AI-Native:

MCP = tools AI can call (databases, APIs, search)
AI-Native = enforcement layer that controls how AI works

MCP gives AI capabilities. AI-Native gives it guardrails.

You need both.

---

**Tweet 7:**

We built this for QA automation (5-layer Selenium architecture, self-improving test framework).

Open-sourced today. MIT license.

Repo: github.com/isagawa-qa/platform

But the pattern applies to any AI-generated codebase.

---

**Tweet 8:**

If you're using AI to write code—any code—you'll hit this wall.

The AI is fast. The output drifts. Maintenance becomes impossible.

We're offering free demos: we'll set up the kernel for your stack.

DM or open an issue. Let's build AI that manages AI.

---

## 4. Product Hunt Listing

### Title:
Isagawa QA — AI Execution Management for Test Automation

### Tagline:
AI that can only do QA right—enforced at runtime, not monitored after the fact

### Description:

**The Problem**

AI is incredible at writing tests—until you hit three months and realize your codebase is unmaintainable. Every test is structured differently. The AI forgets your patterns between sessions. Code quality degrades. You're stuck choosing between velocity and maintainability.

Documentation doesn't help. The AI reads it once, then drifts. Code review catches mistakes too late. Traditional governance tools monitor what happened—they don't prevent it.

**The Category: AI Execution Management**

We're not building AI governance (monitoring, documentation, alerts). We're building **AI Execution Management**—enforcement at the point of execution.

The system doesn't watch the AI work. It controls how the AI works. Hooks intercept file writes. Protocols define architecture rules. If the AI tries to violate a pattern, the write is blocked—the agent physically can't create bad code.

When a test fails, the AI doesn't just fix it. It invokes `/kernel/learn`, which updates both the protocol (soft enforcement) and the hooks (hard enforcement). The mistake becomes permanently impossible.

**How It Works: 5-Layer Architecture**

We built this for Selenium test automation:

1. **WebInterface** — element operations (click, send_keys, get_text)
2. **BrowserInterface** — navigation, waits, script execution
3. **PageObjects** — page-specific flows, no raw selectors
4. **Tests** — pure assertions, no setup logic
5. **Runner** — pytest + fixtures

Every layer has strict boundaries. The AI can't put selectors in tests. It can't put assertions in PageObjects. The hooks enforce this at write-time.

**Self-Building Governance**

The agent creates its own enforcement. You run `/kernel/domain-setup`, and the AI:
- Analyzes your existing codebase
- Extracts patterns (naming, structure, quality gates)
- Builds a protocol (markdown) and hooks (Python)
- Enforces those patterns in every future session

Every failure makes the system smarter. Every lesson updates the protocol and the hooks.

**Open Source + Services**

- **Platform:** MIT license, production-ready, Python + Selenium + pytest
- **Repo:** github.com/isagawa-qa/platform
- **Services:** We'll set up the kernel for your stack (Playwright, Cypress, API testing, whatever). Free demo, then hourly consulting.

This pattern applies beyond QA. If you're using AI to generate any code, you need execution management.

**Category distinction:**
Governance = watching. Execution Management = controlling.

We're building the latter. And we're open-sourcing it so you can too.

---

### First Comment (Maker):

Hey Product Hunt! I'm the maker of Isagawa QA.

**The "aha" moment:**

Six months ago, we started using Claude Code to automate our Selenium tests. The first month was magic—what used to take a day took 20 minutes. By month three, the codebase was chaos. Every test looked different. The AI would "forget" our architecture between sessions.

We tried documentation. We tried detailed prompts. Nothing stuck.

Then I realized: we were managing AI like we manage humans. With docs, reviews, and hope.

But AI doesn't work like humans. It doesn't remember. It doesn't learn implicitly. It needs **enforcement at the execution layer**.

So we built hooks that intercept file writes. Protocols that define architecture rules. A learning loop that updates enforcement after every failure.

The AI can't skip steps. It can't drift from patterns. It can only do QA right.

**What's next:**

This is QA-first, but the pattern applies to any AI-generated code. We're working with early users to adapt the kernel for:
- API test automation (Postman/REST Assured)
- Frontend testing (Playwright/Cypress)
- Data pipelines (dbt/Airflow)

The category we're creating—**AI Execution Management**—is bigger than QA. It's the missing layer between your AI and your code.

If you're using AI to build anything non-trivial, you'll hit this problem. We're here to help.

Free demo: Open an issue on the repo (github.com/isagawa-qa/platform) or DM me.

Let's build AI that manages AI.
