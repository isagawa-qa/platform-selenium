# Contributing to Isagawa QA Platform

Thank you for your interest in contributing.

## Architecture

This project uses a **5-layer architecture**: Test > Role > Task > Page Object > WebInterface (BrowserInterface).

Before writing any code, read the reference implementations in `framework/_reference/`:

| Layer | Reference File | Pattern |
|-------|---------------|---------|
| Page Object | `pages/inquiry_form_page.py` | Locators as class constants, atomic methods, return `self` |
| Task | `tasks/reference_tasks.py` | `@autologger`, POM composition, no return values |
| Role | `roles/reference_role.py` | `@autologger`, Task composition, workflow orchestration |
| Test | `tests/test_reference_workflow.py` | AAA pattern, fixtures, one Role call per test |

See `docs/architecture.md` for the full explanation of the 5-layer pattern and the 28 Design Decisions.

## Key Rules

- **No locators** in Tasks or Roles — only in Page Objects
- **No return values** from Tasks or Roles
- **Return `self`** from POM atomic methods (fluent chaining)
- **Assert via POM state-check methods** in Tests
- **One Role workflow call** per test
- **`@autologger`** decorator on all Task, Role, and Test methods

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
