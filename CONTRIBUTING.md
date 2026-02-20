# Contributing to Isagawa QA Platform

Thank you for your interest in contributing.

## Architecture

This project uses a **5-layer architecture**: Test > Role > Task > Page Object > WebInterface (BrowserInterface).

| Layer | Responsibility |
|-------|---------------|
| **Test** | Orchestrates Roles, asserts results via POM state-check methods |
| **Role** | Coordinates Tasks into business workflows (user persona) |
| **Task** | Performs one domain operation, composes Page Objects |
| **Page Object** | Locators + atomic UI actions for one page, fluent API (`return self`) |
| **WebInterface** | Selenium wrapper — waits, logging, retry |

**Key rules:**
- Locators live *only* in Page Objects
- Tasks and Roles never return values
- `@autologger` decorator on every Task, Role, and Test method
- Multi-role workflows are supported in Tests

See [docs/architecture.md](docs/architecture.md) for the full explanation.

Before writing any code, read the reference implementations in `framework/_reference/`.

## Development Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/isagawa-qa/platform.git
   cd platform
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy environment config:
   ```bash
   cp .env.example .env
   ```

5. Run tests:
   ```bash
   pytest tests/
   ```

## PR Process

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Follow the architecture patterns above
4. Ensure all tests pass: `pytest tests/`
5. Submit a PR with a clear description

## Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` — New feature
- `fix:` — Bug fix
- `refactor:` — Code restructuring
- `test:` — Test additions/changes
- `docs:` — Documentation
- `chore:` — Maintenance

## Questions?

Open an issue or start a discussion on GitHub.
