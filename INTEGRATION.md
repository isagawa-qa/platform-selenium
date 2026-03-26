# Isagawa QA Platform — Integration Context

You are operating in a developer's application workspace. This file gives you the context to run automated Selenium tests against that application using the centralized Isagawa platform-selenium framework.

The platform-selenium directory is the directory containing this file. All test execution, file generation, and framework operations happen there — not in the developer's project.

---

## Your Role

When the developer asks you to test something, generate tests, or run QA:

1. Verify their app is registered in `environment_config.json` (see below)
2. `cd` into the platform-selenium root directory
3. Execute the appropriate command
4. Report results back in context of the developer's feature

Do NOT write test files in the developer's project. All test artifacts belong in platform-selenium.

---

## Registering a New App

If the developer's app is not yet registered, add it to:
```
framework/resources/config/environment_config.json
```

```json
"yourapp": {
  "url": "http://localhost:PORT",
  "explicit_wait": 10,
  "screenshots_on_failure": true,
  "screenshot_dir": "screenshots/yourapp"
}
```

To see currently registered apps, read that config file.

---

## Running Tests

```bash
# Run all tests for an app
pytest tests/APPNAME/ --env=APPNAME -v

# Run a specific test file
pytest tests/APPNAME/test_feature.py --env=APPNAME -v

# Run headless
pytest tests/APPNAME/ --env=APPNAME --headless -v

# With HTML report
pytest tests/APPNAME/ --env=APPNAME -v --html=tests/_reports/report.html --self-contained-html
```

---

## Generating Tests for a New Feature

When the developer asks to add tests for a feature, use the QA workflow. Read and follow these files from the platform-selenium root:

```
.claude/skills/qa-management-layer/SKILL.md
.claude/skills/qa-management-layer/steps/step-01.md
.claude/skills/qa-management-layer/steps/step-04.md
.claude/skills/qa-management-layer/checkpoints/pre-construction.md
```

The workflow requires a user story in this format:
```
As a [persona], I want to [action] on [URL]
```

Output goes to:
- `framework/pages/APPNAME/` — Page Objects
- `framework/tasks/APPNAME/` — Tasks
- `framework/roles/APPNAME/` — Roles
- `tests/APPNAME/` — Test files

---

## Documenting Test Coverage in the Developer's Project

After generating or running tests, create or update a `QA_COVERAGE.md` file in the **developer's project** (not in platform-selenium). This file is the dev project's record that tests exist externally.

```markdown
# QA Coverage

Tests for this project live in the Isagawa platform-selenium framework.
platform-selenium must be checked out and available locally to run tests.

## Coverage Map

| Feature | User Story | Test Location in platform-selenium |
|---------|-----------|-------------------------------------|
| Login | As a user, I want to log in | tests/yourapp/test_login.py |
| Dashboard | As a user, I want to view my dashboard | tests/yourapp/test_dashboard.py |

## Running Tests

See platform-selenium/DEVELOPER_GUIDE.md for setup and execution instructions.
```

Update this file each time new tests are added. It is the only test-related file that belongs in the developer's project.

---

## Dependencies & Constraints

### platform-selenium Checkout Requirement

Tests live in platform-selenium, not in the developer's project. Be aware:

- The developer must have platform-selenium checked out locally for any test operation to work
- If you cannot locate the platform-selenium directory, stop and ask the developer to confirm its path before proceeding
- Never assume the path — if the developer's CLAUDE.md imports this file via `@/path/to/INTEGRATION.md`, that path is your reference point for the root directory

### CI/CD Gap

If the developer asks about running tests in a CI/CD pipeline, flag that platform-selenium must be available in that environment. The options are:

- **Git submodule** — platform-selenium added as a submodule in the app repo (recommended: pins the tested version)
- **Pipeline checkout step** — CI config checks out platform-selenium alongside the app before running tests
- **Shared runner** — a machine with both repos permanently available

This is not something you can configure automatically. Raise it with the developer and refer them to `DEVELOPER_GUIDE.md` for the full breakdown.

---

## On Test Failure

Do NOT auto-fix. Follow this protocol:

1. **STOP** — halt immediately
2. **REPORT** — test name, error message, file location
3. **ANALYZE** — expected vs actual, likely cause
4. **DISCUSS** — ask developer: log defect in `docs/DEFECT_LOG.md`?
5. **PRESENT OPTIONS** — 2-3 fix approaches with tradeoffs
6. **WAIT FOR APPROVAL** — do not fix until approved
7. **FIX + RE-TEST**

---

## Framework Constraints

**You may generate or modify:**
- `tests/` — test files
- `framework/pages/` — page object files
- `framework/tasks/` — task files
- `framework/roles/` — role files
- `tests/data/` — test data

**Do not modify:**
- `framework/interfaces/` — BrowserInterface
- `framework/resources/` — core utilities
- `.claude/` — skills, commands, hooks
- `CLAUDE.md`

---

## Code Pattern Rules

Before generating any framework code, read:
```
framework/_reference/README.md
```

Key rules:
- POM: locators as class constants, atomic methods, `return self`
- Task: `@autologger("Task")`, composes POMs, no return values
- Role: `@autologger("Role")`, composes Tasks, no return values
- Test: `@autologger("Test")`, calls Role methods, asserts via POM state-check methods

---

## Reference Paths (relative to platform-selenium root)

| Resource | Path |
|----------|------|
| Environment config | `framework/resources/config/environment_config.json` |
| Reference patterns | `framework/_reference/README.md` |
| Test reports | `tests/_reports/report.html` |
| Defect log | `docs/DEFECT_LOG.md` |
| QA skill | `.claude/skills/qa-management-layer/` |
