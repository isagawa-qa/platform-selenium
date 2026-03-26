# Developer Guide — Isagawa QA Platform

This is a centralized Selenium test framework. You develop your application in your own workspace; this framework tests it from here.

---

## How It Works

Your app runs locally (or remotely). This framework points a browser at it, navigates it, and asserts behavior — just like a user would. Tests are organized by app, not by framework feature.

```
Your App Workspace          platform-selenium
──────────────────          ─────────────────
You write features   →      Claude runs tests against your app
Your CLAUDE.md       →      imports INTEGRATION.md from here
                            registers your app in environment_config.json
                            runs: pytest tests/yourapp/ --env=yourapp
```

---

## Step 1: Register Your App

Add your app to `framework/resources/config/environment_config.json`:

```json
{
  "yourapp": {
    "url": "http://localhost:3000",
    "explicit_wait": 10,
    "screenshots_on_failure": true,
    "screenshot_dir": "screenshots/yourapp"
  }
}
```

| Key | Required | Description |
|-----|----------|-------------|
| `url` | yes | Base URL of your running app |
| `explicit_wait` | no | Seconds to wait for elements (default: 10) |
| `screenshots_on_failure` | no | Capture screenshot on test failure |
| `screenshot_dir` | no | Where to save screenshots |

---

## Step 2: Set Up Cross-Workspace Access

In your app project's `.claude/settings.json`, add this project as an additional working directory:

```json
{
  "additionalWorkingDirectories": [
    "/path/to/platform-selenium"
  ]
}
```

Or add this line to your project's `CLAUDE.md`:

```
@/path/to/platform-selenium/INTEGRATION.md
```

---

## Step 3: Generate Tests for Your App

From inside the platform-selenium directory, invoke `/qa-workflow` and tell Claude:

```
As a [persona], I want to [action] on [URL]

Example:
As a registered user, I want to log in on http://localhost:3000/login
```

Claude will generate a 4-layer test structure:

| Layer | Location | Purpose |
|-------|----------|---------|
| Page Object | `framework/pages/yourapp/` | UI element locators + atomic actions |
| Task | `framework/tasks/yourapp/` | Domain operations (login, submit, navigate) |
| Role | `framework/roles/yourapp/` | Workflow orchestration |
| Test | `tests/yourapp/` | AAA-pattern assertions |

---

## Step 4: Run Tests

From the platform-selenium directory:

```bash
# Run all tests for your app
pytest tests/yourapp/ --env=yourapp -v

# Run a specific test file
pytest tests/yourapp/test_login.py --env=yourapp -v

# Run headless
pytest tests/yourapp/ --env=yourapp --headless -v

# Generate HTML report
pytest tests/yourapp/ --env=yourapp -v --html=tests/_reports/report.html --self-contained-html
```

---

## Available Commands (when working inside platform-selenium)

| Command | What It Does |
|---------|-------------|
| `/qa-workflow` | 5-step guided test generation — provide a user story, get a full test suite |
| `/qa-workflow-dev` | Same as above, unrestricted permissions (for framework changes) |
| `/run-test [path]` | Run a specific test file or directory with HITL failure protocol |
| `/pr` | Review changed test code against framework patterns |
| `/qa-reuse-check` | Scan for duplicate page objects before building new ones |

---

## Test Reports

HTML reports are written to `tests/_reports/report.html` after any `/run-test` invocation. Open in browser for full pass/fail detail, error tracebacks, and metadata (env, URL, browser, timestamp).

---

## Framework Architecture

```
platform-selenium/
├── framework/
│   ├── pages/          ← Page Object Models (locators + atomic UI actions)
│   ├── tasks/          ← Domain operations (compose POMs)
│   ├── roles/          ← Workflow orchestration (compose Tasks)
│   ├── interfaces/     ← BrowserInterface (core, do not modify)
│   └── resources/
│       └── config/
│           └── environment_config.json   ← Register your app here
├── tests/
│   ├── yourapp/        ← Your test files go here
│   ├── conftest.py     ← Fixtures: driver, config, browser
│   └── _reports/       ← HTML test reports
└── INTEGRATION.md      ← Import this from your project's CLAUDE.md
```

---

## Dependencies & Constraints

### platform-selenium Must Be Checked Out

Your tests live here, not in your application repo. This means:

- Every developer who wants to run tests must have platform-selenium checked out locally
- Your application repo will have no test files — only a `QA_COVERAGE.md` that maps features to test locations here
- If you delete or move your platform-selenium checkout, tests become inaccessible until it is restored

Document this dependency clearly in your application's `README.md` or `CONTRIBUTING.md`.

### CI/CD

If your application pipeline needs to run these tests automatically, platform-selenium must be available in that environment. Options:

| Approach | How |
|----------|-----|
| Git submodule | Add platform-selenium as a submodule in your app repo — tests travel with the code but stay in a separate repo |
| Pipeline checkout step | In your CI config, add a step that checks out platform-selenium alongside your app before running tests |
| Shared runner | Run tests from a machine that has both repos permanently checked out |

A submodule is the cleanest for most teams: the app repo records the exact platform-selenium commit it was tested against, and CI gets both repos in one checkout.

---

## When Tests Fail

The `/run-test` command follows a Human-in-the-Loop (HITL) protocol on failure:

1. **STOP** — does not auto-fix
2. **REPORT** — shows test name, error, and location
3. **ANALYZE** — explains expected vs actual behavior
4. **DISCUSS** — asks whether to log a defect in `docs/DEFECT_LOG.md`
5. **FIX OPTIONS** — presents 2-3 approaches with tradeoffs
6. **APPROVE** — you choose the fix approach
7. **FIX + RE-TEST** — implements and re-runs

You stay in control of every fix decision.
