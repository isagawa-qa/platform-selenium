# Isagawa QA Platform — Developer Guide

The Isagawa QA Platform is a family of AI-powered test automation frameworks. Each framework targets a different testing domain. This guide helps you find the right one for your project and get started.

---

## Which Framework Do You Need?

| What are you testing? | Framework | Repo |
|----------------------|-----------|------|
| Web UI / browser flows (Python) | Selenium | [platform-selenium](https://github.com/isagawa-qa/platform-selenium) |
| Web UI / browser flows (TypeScript) | Playwright | [platform-playwright](https://github.com/isagawa-qa/platform-playwright) |
| Docker container images | Docker validation | [platform-docker](https://github.com/isagawa-qa/platform-docker) |
| SSH-accessible Linux images | SSH validation | [platform-ssh](https://github.com/isagawa-qa/platform-ssh) |
| LLM pipelines / AI output quality | DeepEval | [test-platform-deepeval](https://github.com/isagawa-qa/test-platform-deepeval) |

If your project involves browser-based UI, start with platform-selenium (Python) or platform-playwright (TypeScript). If you need both, they can run side by side — they do not share state.

---

## How Each Framework Works

All frameworks follow the same core pattern:

1. **You describe** what to test in plain English (a user story or validation requirement)
2. **AI generates** a complete, structured test suite following the framework's architecture
3. **Tests run** against your application or infrastructure
4. **Results report** with full HTML output and failure analysis

Tests are centralized in the framework repo. Your application repo stays clean — it only holds a `QA_COVERAGE.md` that maps features to test locations here.

---

## Common Prerequisites

| Tool | Purpose |
|------|---------|
| Git | Clone repos |
| VS Code + Claude Code extension | AI-assisted test generation |
| GitHub account | Fork repos to contribute |

Framework-specific prerequisites (Python, Node, Docker, etc.) are listed in each repo's `SETUP.md`.

---

## Getting Started

### 1. Pick your framework from the table above

### 2. Clone and set up

Each repo has a `SETUP.md` with exact steps:

- [platform-selenium/SETUP.md](https://github.com/isagawa-qa/platform-selenium/blob/main/SETUP.md)
- platform-playwright/SETUP.md *(coming soon)*
- platform-docker/SETUP.md *(coming soon)*
- platform-ssh/SETUP.md *(coming soon)*

### 3. Connect your application

Register your app's URL in the framework's environment config. See each repo's `SETUP.md` for the exact file and format.

### 4. Work from your own project

Each framework ships with an `INTEGRATION.md` — a file you import into your project's `CLAUDE.md` that lets Claude run tests and generate coverage without leaving your workspace.

Add one line to your project's `CLAUDE.md`:
```
@/path/to/platform-selenium/INTEGRATION.md
```

Then use this prompt to activate it:
```
I'm working on [your app]. The Isagawa platform-selenium framework is checked
out at /path/to/platform-selenium. Please read
/path/to/platform-selenium/INTEGRATION.md so you understand how to generate
and run tests for this project.
```

---

## The Kernel

All frameworks are governed by the **Isagawa Kernel** — an enforcement layer built into each repo's Claude Code configuration. It:

- Tracks actions and forces periodic re-anchoring to protocol
- Blocks writes when a test failure hasn't been learned from
- Enforces Human-in-the-Loop (HITL) approval before any fix is applied
- Maintains a lessons log that persists across sessions

You will see `BLOCKED:` messages when the kernel enforces a gate. Follow the instruction shown — it always tells you the exact command to run. See [KERNEL_AGENT_GUIDE.md](https://github.com/isagawa-qa/platform-selenium/blob/main/KERNEL_AGENT_GUIDE.md) for the full agent-facing spec.

---

## Framework Architecture

All repos use a variant of the same layered pattern:

```
Infrastructure / Interface layer   ← never modify
        ↑
   Page / Module layer             ← locators, atomic actions
        ↑
   Task layer                      ← domain operations
        ↑
   Role layer                      ← workflow orchestration
        ↑
   Test layer                      ← assertions, AAA pattern
```

Each layer composes the layer below it. No layer skips. AI generates code into this structure — it never writes outside it.

---

## Dependencies & Constraints

### Framework repos must be checked out locally

Tests live in the framework repo, not in your application repo. Every developer who runs tests needs the framework repo checked out. Document this dependency in your application's `README.md`.

### CI/CD

If your pipeline needs to run these tests, the framework repo must be available in that environment:

| Option | How |
|--------|-----|
| Git submodule | Add the framework repo as a submodule — pins the tested version, clean CI checkout |
| Pipeline checkout step | Add a step that clones the framework repo before running tests |
| Shared runner | A machine with all repos permanently checked out |

Git submodule is recommended — it records exactly which framework version your app was tested against.

---

## Contributing

All repos accept PRs via fork:

```bash
gh repo fork isagawa-qa/REPO_NAME --fork-name REPO_NAME-fk --clone=false
git remote add fork https://github.com/YOURUSER/REPO_NAME-fk.git
```

Always create a clean branch from `main` before opening a PR. Never open a PR from a long-running feature branch — scope it to the change only.

---

## Support

Open an issue in the relevant repo. Include:
- Which framework and version
- The exact error or `BLOCKED:` message
- The test file path and `--env` flag used
