# Isagawa QA Platform

### AI Execution Management for Test Automation

> AI can generate tests. But can you trust it to execute correctly?

Most AI tools watch what happened and report after the fact. Isagawa **enforces how AI works** — gating every action at runtime so the AI can only do it right.

This isn't AI governance. It's **AI execution management**.

---

## The Problem

AI can generate Selenium tests in seconds. But without enforcement:

- Tests break existing architecture patterns
- Page Objects get skipped or mixed with business logic
- The same mistakes repeat across every session
- You spend more time fixing AI output than writing tests yourself

**The cycle:** Generate → breaks something → fix → generate → breaks it differently → start over.

## The Solution

The Isagawa QA Platform combines a **5-layer test architecture** with the **Isagawa Kernel** — a self-building, self-improving enforcement system that runs *inside* the AI agent.

The kernel doesn't monitor the AI from outside. It **manages the AI from within**. The AI learns your standards, enforces them automatically, and gets permanently smarter after every failure.

---

## 5-Layer Architecture

Every test follows a strict separation of concerns. Each layer has one job:

| Layer | Responsibility | Example |
|-------|---------------|---------|
| **Test** | Says what should happen, asserts the result | `test_submit_inquiry()` |
| **Role** | Coordinates tasks into business workflows | `CustomerRole.submit_new_inquiry()` |
| **Task** | Performs one domain operation across pages | `search_and_create_customer()` |
| **Page (POM)** | Knows where elements are on one page | `InquiryFormPage.select_type("Service")` |
| **WebInterface** | Wraps browser automation (Selenium) | `BrowserInterface.click()`, `.type()` |

```
Test (Arrange / Act / Assert)
  └─→ Role (multi-task workflow, user persona)
       └─→ Task (single domain operation)
            └─→ Page Object (one page, atomic actions, fluent API)
                 └─→ BrowserInterface (Selenium wrapper, waits, logging)
```

**Key rules:**
- Locators live *only* in Page Objects — never in Tasks, Roles, or Tests
- Tasks and Roles never return values — Tests assert through POM state-check methods
- Tests orchestrate Roles to execute business workflows — multi-role workflows are supported
- `@autologger` decorator on every Task, Role, and Test method

See [docs/architecture.md](docs/architecture.md) for the full explanation and all 28 Design Decisions.

---

## How It Works

The AI follows a gated workflow to generate tests:

1. **User Input** — describe the persona, URL, and workflow to test
2. **Pre-flight** — credential strategy and browser session setup
3. **AI Processing** — BDD scenarios, expected states, intent extraction
4. **Construction** — element discovery, code generation following the 5-layer architecture
5. **Execution** — run the test, human-in-the-loop triage on failure

On **any** failure, the agent stops and asks. No autonomous looping. Every fix makes the system permanently smarter — the same mistake cannot happen again.

---

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+ (for Playwright MCP)
- Chrome or Brave browser
- [Claude Code](https://claude.ai/claude-code) (for AI-powered test generation)

### Install

```bash
git clone https://github.com/isagawa-qa/platform.git
cd platform
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# Install Playwright MCP server (used for element discovery)
npx @playwright/mcp@latest
```

### Run Tests

```bash
# Run all tests
pytest tests/

# Run with HTML report
pytest tests/ --html=report.html

# Run against a specific environment
pytest tests/ --env=parabank
```

### AI-Powered Test Generation

With Claude Code installed:

```bash
claude
# Then use the /qa-workflow command:
# "Create a test for the login workflow on https://your-site.com"
```

The kernel enforces the 5-layer architecture automatically. The AI reads reference implementations, discovers elements via Playwright MCP, and generates POM → Task → Role → Test files that follow every convention.

---

## Project Structure

```
platform/
├── .claude/
│   ├── commands/          # Kernel + QA workflow commands
│   ├── hooks/             # Gate enforcer + test failure detector
│   ├── skills/
│   │   ├── kernel-domain-setup/   # Self-building kernel setup
│   │   └── qa-management-layer/   # 5-step QA workflow skill
│   └── settings.json      # Hook configuration
├── framework/
│   ├── _reference/         # Canonical code patterns (read-before-write)
│   │   ├── pages/          # POM reference implementations
│   │   ├── tasks/          # Task reference implementations
│   │   ├── roles/          # Role reference implementations
│   │   └── tests/          # Test reference implementations
│   ├── interfaces/
│   │   └── browser_interface.py   # WebInterface (Selenium wrapper)
│   └── resources/
│       ├── chromedriver/   # Driver factory
│       ├── config/         # Environment configuration
│       └── utilities/      # Autologger, data generator, logger
├── tests/
│   ├── data/               # Test data (credentials, fixtures)
│   └── conftest.py         # Pytest fixtures and configuration
├── docs/                   # Architecture, kernel, getting started
├── .mcp.json               # Playwright MCP server config
├── CLAUDE.md               # Kernel instructions
├── CONTRIBUTING.md          # Architecture rules and PR process
├── LICENSE                  # MIT
└── requirements.txt
```

---

## The Bigger Picture

QA is one domain. The Isagawa Kernel supports **any** domain.

The kernel is domain-agnostic — it provides the enforcement loop (hooks, protocols, learning) while domain-specific knowledge lives in protocol files and skills. What you see here in QA (5-layer architecture, gated workflows, self-improving quality) can be applied to:

- Code generation and review
- Content creation workflows
- Data pipeline management
- Any process where AI needs to execute correctly, not just generate output

The kernel will be open-sourced separately. Domain packs — pre-loaded with patterns, anti-patterns, and quality gates for specific verticals — will be available for teams that want to skip the learning curve. The first pack targets vibe coders: ship code like a senior engineer.

---

## AI Execution Management vs AI Governance

| AI Governance (Others) | AI Execution Management (Isagawa) |
|------------------------|-----------------------------------|
| Monitors AI behavior | Controls AI behavior |
| Documents compliance | Enforces compliance |
| Alerts on violations | Prevents violations |
| Audits after execution | Gates during execution |
| "Did the AI do it right?" | "The AI can only do it right" |

This is AI you can actually delegate QA to.

---

## Services

We deliver a highly scalable, maintainable, enterprise-grade test automation framework powered by an AI agent managed by our own enforcement kernel. We build the entire test solution — login credentials, data management, environment configuration, CI/CD integration, and reporting. Your team owns the entire tech stack: a true AI-native test automation framework built on Claude Code. We also train your team to create and maintain test scripts on their own.

### What We Deliver

Depending on your needs, the full solution can include:

- Login/auth credential management
- Test data management
- Environment configuration
- CI/CD pipeline integration
- Test reporting & dashboards
- Page object architecture
- API test coverage
- Cross-browser/cross-device setup

### Free Demo — The Proof

We'll build working tests on **YOUR** site in 60 minutes. You keep the code whether you hire us or not.

No discovery phase. No proposal. No waiting.

**[Book a free demo →](https://github.com/isagawa-qa/platform/discussions)**

### Pricing

| Offering | What's Included | Price |
|----------|----------------|-------|
| **Free Demo** | Live 60-min session on your site. Working tests you keep. | $0 |
| **Implementation** | Full QA infrastructure: framework setup, credential management, environment config, CI/CD integration, test coverage, team training | $15,000 - $50,000 |
| **Retainer** | Ongoing test development, maintenance, new workflow coverage, priority support | $1,000 - $3,000/month |
| **Enterprise** | Full implementation, compliance docs, cross-browser/device setup, dedicated support | Custom ($50K+) |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for architecture rules, development setup, and PR process.

## License

[MIT](LICENSE) — Copyright (c) 2025 Isagawa

---

<sub>Built with the [Isagawa Kernel](https://github.com/isagawa-qa) — self-building, self-improving, safety-first.</sub>
