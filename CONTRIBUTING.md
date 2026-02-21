# Contributing to Isagawa QA Platform

Thank you for your interest in contributing.

## Architecture

This project uses a **5-layer architecture**: Test > Role > Task > Page Object > BrowserInterface (BrowserInterface).

| Layer | Responsibility |
|-------|---------------|
| **Test** | Orchestrates Roles, asserts results via POM state-check methods |
| **Role** | Coordinates Tasks into business workflows (user persona) |
| **Task** | Performs one domain operation, composes Page Objects |
| **Page Object** | Locators + atomic UI actions for one page, fluent API (`return self`) |
| **BrowserInterface** | Selenium wrapper — waits, logging, retry |

**Key rules:**
- Locators live *only* in Page Objects
- Tasks and Roles never return values
- `@autologger` decorator on every Task, Role, and Test method
- Multi-role workflows are supported in Tests

See [docs/architecture.md](docs/architecture.md) for the full explanation.

Before writing any code, read the reference implementations in `framework/_reference/`.

---

## What We're Looking For

We welcome contributions that extend the platform's reach while preserving the 5-layer architecture. Here are the areas where help is most needed:

### Framework Ports

The current implementation uses Python + Selenium. We'd love ports to other frameworks — all using the same layered architecture:

- **Playwright** (Python) — port the BrowserInterface layer to use Playwright instead of Selenium
- **Cypress** — JavaScript implementation following the same 5-layer pattern
- **Selenide** (Java) — Java implementation for teams on the JVM

### Language Support

Bring the 5-layer architecture to other language ecosystems:

- **TypeScript/JavaScript** — Node.js implementation with the same layer separation
- **Java** — Selenium or Selenide-based, with equivalent Page Object and Task patterns
- **C#/.NET** — for teams using NUnit/xUnit + Selenium

### New Test Layers

Extend the architecture beyond browser UI testing — same layered approach, different interfaces:

- **API layer** — replace BrowserInterface with an HTTP client (requests, RestAssured, etc.), keep Task/Role/Test layers identical
- **Mobile layer** — Appium or similar, same 5-layer pattern adapted for mobile interactions

### CI/CD & Infrastructure

- **GitHub Actions** workflow for running tests on PR
- **Docker** support for containerized test execution
- **Jenkins/GitLab CI** pipeline examples

### Reporting & Observability

- **Allure** integration for richer test reports
- **HTML dashboard** improvements beyond pytest-html
- **Slack/Teams notifications** on test failure

### Example Test Suites

Complete working examples that demonstrate the architecture on public test sites:

- Authentication flows (login, registration, password reset)
- CRUD operations (create, read, update, delete)
- E-commerce workflows (search, cart, checkout)
- Multi-role scenarios (admin + user interactions)

### Documentation

- Tutorials and walkthroughs
- Video guides
- Translations

---

## Development Setup

### 1. Clone and install

```bash
git clone https://github.com/isagawa-qa/platform.git
cd platform
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

### 2. Configure MCP (required for AI-powered test generation)

The platform uses [Playwright MCP](https://github.com/microsoft/playwright-mcp) for browser element discovery. It's pre-configured in `.mcp.json`:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

**Prerequisites:**
- Node.js 18+ (`node --version` to check)
- npm (`npm --version` to check)

**Verify MCP is working:**
```bash
npx @playwright/mcp@latest --help
```

**Windows users:** If you encounter issues with `npx`, create a `.mcp.json` override:
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

### 3. Configure environment

Edit `.env` to set your preferences:
```
BROWSER=chrome        # or 'brave'
HEADLESS=false        # or 'true' for headless mode
TEST_ENV=DEFAULT      # matches key in environment_config.json
```

### 4. Run tests

```bash
pytest tests/
```

---

## PR Process

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Follow the 5-layer architecture — read `framework/_reference/` before writing code
4. Ensure all tests pass: `pytest tests/`
5. Submit a PR with a clear description of what layer(s) your change touches

For framework ports or new language support, open an issue first to discuss the approach.

## Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` — New feature
- `fix:` — Bug fix
- `refactor:` — Code restructuring
- `test:` — Test additions/changes
- `docs:` — Documentation
- `chore:` — Maintenance

## Questions?

Open an issue or reach out at **[alain@isagawa.co](mailto:alain@isagawa.co)**.
