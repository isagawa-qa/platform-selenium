# Isagawa QA Platform

### AI Execution Management for Test Automation

> AI can generate tests. But can you trust it to execute correctly?

Most AI tools watch what happened and report after the fact. Isagawa **enforces how AI works** gating every action at runtime so the AI can only do it right.

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

The Isagawa QA Platform combines a **5-layer test architecture** with the **Isagawa Kernel** a self-building, self-improving enforcement system that runs *inside* the AI agent.

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
- Locators live *only* in Page Objects, never in Tasks, Roles, or Tests
- Tasks and Roles never return values, Tests assert through POM state-check methods
- Tests orchestrate Roles to execute business workflows, multi-role workflows are supported
- `@autologger` decorator on every Task, Role, and Test method

---

## How It Works

1. Describe the persona, URL, and workflow you want to test
2. The AI discovers page elements and generates code following the 5-layer architecture
3. Tests are executed with human-in-the-loop triage on failure
4. Every fix makes the system permanently smarter, the same mistake cannot happen again

---

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+ (for Playwright MCP)
- Chrome or Brave browser
- [Claude Code](https://claude.ai/claude-code)

### 1. Install

```bash
git clone https://github.com/isagawa-qa/platform.git
cd platform
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

### 2. Configure your test target

Edit `framework/resources/config/environment_config.json` to add your application URL:

```json
{
  "myapp": {
    "url": "https://staging.your-app.com"
  }
}
```

### 3. Set up the AI agent

The platform includes a QA domain pack. On first run, the agent analyzes your codebase and configures itself to enforce the 5-layer architecture.

```bash
claude                    # Start Claude Code in the platform/ directory
```

Once inside, type `start` or describe any task. The agent will detect a fresh setup and run domain initialization automatically. When it finishes, it will ask you to restart Claude Code to activate enforcement.

```bash
claude                    # Start again
> continue                # Agent picks up where it left off — now ready
```

### 4. Generate your first test

```bash
# Inside Claude Code, invoke the workflow command:
/qa-workflow
```

The agent will ask for your test requirement:

```
As a [persona], I want to [action] on [URL]

Example: "As a customer, I want to login on https://staging.your-app.com"
```

It then discovers page elements via Playwright MCP and generates all 5 layers — Page Object, Task, Role, and Test — following every convention automatically.

### 5. Review generated code

```bash
# Inside Claude Code:
/pr
```

The agent reviews all generated files against the architecture rules — layer separation, naming conventions, decorator usage, locator placement — and reports violations with file and line references. Like a senior SDET code review, done in seconds.

For detailed setup instructions, see [Getting Started](docs/getting-started.md).

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
│       └── utilities/      # Autologger
├── tests/
│   ├── data/               # Test data (credentials, fixtures)
│   └── conftest.py         # Pytest fixtures and configuration
├── docs/                   # Architecture, getting started
├── .mcp.json               # Playwright MCP server config
├── CLAUDE.md               # Kernel instructions
├── CONTRIBUTING.md          # Architecture rules and PR process
├── LICENSE                  # MIT
└── requirements.txt
```

---

## The Bigger Picture

QA is one domain. The Isagawa Kernel supports **any** domain.

The kernel is domain-agnostic, it enforces how AI executes, not just what it generates. What you see here in QA can be applied to:

- Code generation and review
- Content creation workflows
- Data pipeline management
- Any process where AI needs to execute correctly, not just generate output

The kernel will be open-sourced separately. Domain packs pre-loaded with patterns, anti-patterns, and quality gates for specific verticals will be available for teams that want to skip the learning curve. The first pack targets vibe coders: ship code like a senior engineer.

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

We deliver a highly scalable, maintainable, enterprise-grade test automation framework powered by an AI agent managed by our own enforcement kernel. We build the entire test solution: login credentials, data management, environment configuration, and page object architecture. Your team owns the entire tech stack: a true AI-native test automation framework built on Claude Code. We also train your team to create and maintain test scripts on their own.

### What We Deliver

Depending on your needs, the full solution can include:

- Login/auth credential management
- Test data management
- Environment configuration
- Page object architecture

### Demo

We'll build working tests on **YOUR** site in 60 minutes. No discovery phase. No proposal. No waiting.

**[alain@isagawa.co](mailto:alain@isagawa.co)** · **[DM on LinkedIn](https://www.linkedin.com/in/alain-ignacio-54b9823)**

### Pricing

| Offering | What's Included | Price |
|----------|----------------|-------|
| **Demo** | Live 60-min session on your site | Contact us |
| **Implementation** | Full QA infrastructure: framework setup, credential management, environment config, team training | $15,000 - $50,000 |
| **Retainer** | Ongoing test development, maintenance, new workflow coverage, priority support | $1,000 - $3,000/month |
| **Enterprise** | Full implementation, compliance docs, dedicated support | Custom ($50K+) |

---

## Contributing

See [Getting Started](docs/getting-started.md) for detailed setup, [Architecture](docs/architecture.md) for the full 5-layer explanation, and [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and PR process.

## License

[MIT](LICENSE) — Copyright (c) 2025 Isagawa

---

<sub>Built with the [Isagawa Kernel](https://github.com/isagawa-qa) self-building, self-improving, safety-first.</sub>
