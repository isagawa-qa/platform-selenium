# Getting Started

## Prerequisites

- **Python 3.10+**
- **Chrome** or **Brave** browser
- **Node.js 18+** (for Playwright MCP server)
- **Claude Code** — [install instructions](https://claude.ai/claude-code)

## 1. Clone and install

```bash
git clone https://github.com/isagawa-qa/platform.git
cd platform
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` to set your preferences:

```
BROWSER=chrome        # or 'brave'
HEADLESS=false        # or 'true' for headless mode
TEST_ENV=DEFAULT      # matches key in environment_config.json
```

## 3. Add your test target

Edit `framework/resources/config/environment_config.json` to add your application URL:

```json
{
  "DEFAULT": {
    "url": "http://www.automationpractice.pl/index.php"
  },
  "myapp": {
    "url": "https://staging.your-app.com"
  }
}
```

Add credentials to `tests/data/test_users.json` if your workflow requires login:

```json
{
  "myapp_user": {
    "email": "test@example.com",
    "password": "your-test-password"
  }
}
```

## 4. Set up the AI agent

The platform includes a QA domain pack — pre-loaded architecture patterns, conventions, and quality gates. On first run, the AI agent uses this pack to configure itself.

Open a terminal in the `platform/` directory and start Claude Code:

```bash
claude
```

Once inside, type `start` or describe any task — this triggers the agent to initialize. On first run, the agent will:
- Detect a fresh setup (no existing domain)
- Analyze the codebase and reference implementations
- Learn the 5-layer architecture patterns
- Configure itself to enforce those patterns

When domain setup completes, the agent will ask you to restart Claude Code to activate enforcement:

```bash
claude
```

After restarting, type `continue`. The agent picks up where it left off and is now ready to generate tests. This setup only happens once — future sessions pick up automatically.

## 5. Generate your first test

Inside Claude Code, invoke the QA workflow command:

```
/qa-workflow
```

The agent will prompt you for your test requirement in this format:

```
As a [persona], I want to [action] on [URL]
```

For example:

```
As a customer, I want to login and view my account on https://staging.your-app.com
```

You'll also provide a **workflow identifier** — this creates organized folders at `framework/pages/{workflow}/` and `tests/{workflow}/`.

The agent then executes a 5-step workflow:

1. **User Input** — Validates your requirement and checks for duplicate coverage
2. **Pre-flight** — Configures environment and verifies connectivity
3. **Discovery** — Uses Playwright MCP to discover page elements and interactions
4. **Construction** — Reads reference implementations, then generates code following the 5-layer architecture:
   - `framework/pages/{workflow}/` — Page Objects (locators + atomic methods)
   - `framework/tasks/{workflow}/` — Tasks (domain operations)
   - `framework/roles/{workflow}/` — Roles (workflow orchestration)
   - `tests/{workflow}/` — Tests (assertions)
5. **Execution** — Runs the generated test with human-in-the-loop triage on failure

## 6. Review generated code

After tests are generated and passing, run the PR review command inside Claude Code:

```
/pr
```

The agent scans all generated files and validates them against the architecture rules:

- **Page Objects** — locators as class constants, atomic methods returning `self`, state-check methods
- **Tasks** — `@autologger` decorator, no locator imports, no return values
- **Roles** — `@autologger` decorator, imports from tasks only, no direct navigation
- **Tests** — `@autologger` decorator, assertions via POM state-check methods, no locators

If violations are found, the agent reports them with file and line references and asks how you'd like to proceed (fix all, fix specific, explain, or approve with exceptions).

If everything passes:

```
PR REVIEW: APPROVED

Summary: 4 files checked, 0 violations

Ready to merge.
```

## 7. Run tests manually

Once you have generated tests, you can run them directly with pytest:

```bash
# Run all tests
pytest tests/

# Run a specific workflow
pytest tests/myapp/

# Run with a specific environment
pytest tests/ --env=myapp

# Run in headless mode
pytest tests/ --headless

# Generate HTML report
pytest tests/ --html=report.html
```

## Understanding the output

Each generated file follows the 5-layer architecture:

**Page Object** — element locators and atomic interactions:
```python
class LoginPage:
    EMAIL_INPUT = (By.CSS_SELECTOR, "#email")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "#password")
    SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit']")

    def enter_email(self, email):
        self.browser.type(*self.EMAIL_INPUT, email)
        return self

    def is_logged_in(self):
        return self.browser.is_element_present(*self.DASHBOARD_HEADER)
```

**Task** — domain operations:
```python
class LoginTasks:
    @autologger.automation_logger("Task")
    def login(self, email, password):
        self.login_page.enter_email(email).enter_password(password).click_submit()
```

**Role** — workflow orchestration:
```python
class UserRole:
    @autologger.automation_logger("Role")
    def login_and_verify(self, email, password):
        self.login_tasks.login(email, password)
```

**Test** — thin, focused assertion:
```python
@autologger.automation_logger("Test")
def test_user_login(self):
    self.user_role.login_and_verify(email, password)
    assert self.login_page.is_logged_in()
```

## Windows Users

The `.mcp.json` is configured for cross-platform use with `npx`. If you encounter issues with the Playwright MCP server on Windows, create a `.mcp.json` override:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "cmd",
      "args": ["/c", "npx", "@playwright/mcp@latest"]
    }
  }
}
```

## Next Steps

- Read [Architecture](architecture.md) for the full 5-layer explanation
- Browse `framework/_reference/` for canonical code patterns
- Check [CONTRIBUTING.md](../CONTRIBUTING.md) if you want to contribute
