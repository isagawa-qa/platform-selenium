# Isagawa QA Platform

### AI Execution Management for Test Automation

> AI can generate tests. But can you trust it to execute correctly?

Most AI tools watch what happened and report after the fact. Isagawa **enforces how AI works** gating every action at runtime so the AI can only do it right.

This isn't AI governance. It's **AI execution management**.

https://github.com/user-attachments/assets/b9fc88b5-5fd4-4308-b248-17fbcc47b637

---

## Get Started (Step by Step)

Follow each step in order. Do not skip any step. Everything is done inside VS Code.

### Step 1: Install VS Code

VS Code is the code editor where you will do all your work.

1. Go to https://code.visualstudio.com/
2. Click the big **Download** button
3. Open the file you downloaded
4. Follow the installer — click **Next** on each screen, then click **Install**
5. When it finishes, open VS Code

### Step 2: Install Git

Git is a tool that downloads and tracks code. You need it to download this project.

1. Go to https://git-scm.com/downloads
2. Click the download for your operating system (Windows, Mac, or Linux)
3. Open the file you downloaded
4. Follow the installer — use the default options on every screen, click **Next**, then **Install**
5. When it finishes, restart VS Code if it is already open

**Check that Git is installed:**
1. In VS Code, open the terminal: press ``Ctrl + ` `` (the backtick key, above the Tab key on your keyboard)
2. Type this and press **Enter**:
   ```bash
   git --version
   ```
3. You should see something like: `git version 2.44.0`. If you see this, Git is installed.

### Step 3: Install Python

Python runs the test framework. You need version 3.10 or higher.

1. Go to https://www.python.org/downloads/
2. Click the big **Download Python** button
3. Open the file you downloaded
4. **Important:** Check the box that says **"Add Python to PATH"** at the bottom of the installer
5. Click **Install Now**
6. When it finishes, restart VS Code

**Check that Python is installed:**
1. In the VS Code terminal (``Ctrl + ` ``), type:
   ```bash
   python --version
   ```
2. You should see something like: `Python 3.12.2`. The number must be 3.10 or higher.

### Step 4: Install Node.js

Node.js is needed for the Playwright MCP browser tool that discovers page elements.

1. Go to https://nodejs.org/
2. Click the **LTS** download button (the one that says "Recommended")
3. Open the file you downloaded
4. Follow the installer — use the default options, click **Next**, then **Install**
5. Restart VS Code after installing

**Check that Node.js is installed:**
1. In the VS Code terminal (``Ctrl + ` ``), type:
   ```bash
   node --version
   ```
2. You should see something like: `v20.11.0`. The number must be 18 or higher.

### Step 5: Install Claude Code Extension

Claude Code is the AI agent that builds tests for you inside VS Code.

1. In VS Code, click the **Extensions** icon on the left sidebar (it looks like 4 small squares)
2. In the search box, type: `Claude Code`
3. Find **"Claude Code"** by Anthropic — click **Install**
4. Wait for the install to finish
5. You will see a **sparkle icon (✱)** appear in the top-right area of VS Code

> **You need an Anthropic account.** If you do not have one, go to https://claude.ai and create an account first.

### Step 6: Download This Project

Do this inside VS Code. Do not use a separate terminal.

1. In VS Code, open the terminal: press ``Ctrl + ` ``
2. Go to your Desktop (so the project saves there):
   ```bash
   cd Desktop
   ```
3. Download the project:
   ```bash
   git clone https://github.com/isagawa-qa/platform-selenium.git
   ```
4. Wait for the download to finish

### Step 7: Open the Project in VS Code

This step is important. Claude Code needs to be inside the project folder to work correctly.

1. In VS Code, click **File** → **Open Folder**
2. Find and select the `platform-selenium` folder on your Desktop
3. Click **Select Folder** (Windows) or **Open** (Mac)
4. VS Code will reload with the project open
5. You should see the project files on the left sidebar (folders like `framework/`, `tests/`, `.claude/`)

### Step 8: Install Dependencies

1. In VS Code, open the terminal: press ``Ctrl + ` ``
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Mac / Linux:**
     ```bash
     source venv/bin/activate
     ```
4. You should see `(venv)` at the beginning of your terminal line. This means the virtual environment is active.
5. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Wait for it to finish
7. Copy the environment config file:
   ```bash
   cp .env.example .env
   ```

### Step 9: Verify Playwright MCP

The AI agent uses Playwright MCP to open a browser and discover page elements.

1. Click the **sparkle icon (✱)** in VS Code to open Claude Code
2. Type:
   ```
   /mcp
   ```
3. You should see **playwright** in the list of MCP servers
4. If you do NOT see it, close VS Code and open it again, then check `/mcp` again

### Step 10: Verify the Install

In the VS Code terminal, make sure `(venv)` is showing, then type:
```bash
pytest --co
```

You should see a list of test files. This means pytest can find the tests and the framework is installed correctly.

If you see errors, go to the [Troubleshooting](#troubleshooting) section below.

### Step 11: Create Your First Test

1. In Claude Code (click the **sparkle icon ✱** if it is not open), type:
   ```
   /qa-workflow
   ```
2. Claude will ask what you want to test. Use this format for best results:

   ```
   Requirement: As a [role], I want to [action] so I can [goal]
   URL: https://your-app.com/page1, https://your-app.com/page2
   Workflows: workflow-name

   ---
   Steps:

   Phase 1: [Description]
   1. [Action] → [Expected result]
   2. [Action] → [Expected result]
   3. [Action] → [Expected result]

   Phase 2: [Description]
   4. [Action] → [Expected result]
   5. [Action] → [Expected result]

   Expected:
   - [What should happen after Phase 1]
   - [What should happen after Phase 2]

   Credentials:
   - Email: your-test-email@example.com
   - Password: your-test-password
   ```

   **Example (real test):**

   ```
   Requirement: As an employee manager, I want to create an employee
     and assign them a task so I can validate the workforce management flow
   URL: https://myapp.com/employees, https://myapp.com/tasks
   Workflows: employee-management and task-management

   ---
   Steps:

   Phase 1: Create employee
   1. Login with credentials → redirects to /dashboard
   2. Click "Employees" in sidebar → opens /employees
   3. Click "Add Employee" button → modal opens
   4. Enter name: "Research Assistant"
   5. Configure employee settings (role, capabilities)
   6. Click "Create Employee" → modal closes

   Phase 2: Assign task to employee
   7. Click "Tasks" in sidebar → opens /tasks
   8. Click "Add Task" button → modal opens
   9. Enter title: "Research competitor pricing"
   10. Enter description: "Analyze top 5 competitors"
   11. Select assignee: "Research Assistant" from dropdown
   12. Click "Create Task" → modal closes

   Expected:
   - Toast: "Employee created" after step 6
   - "Research Assistant" appears in employees list
   - Toast: "Task created" after step 12
   - Task shows "Research Assistant" as assignee

   Credentials:
   - Email: testuser@example.com
   - Password: testpassword123
   ```

3. Press **Enter** and wait. Claude will:
   - Open a browser and navigate to your URL
   - Find all the buttons, fields, and links on each page
   - Write the test code automatically
   - Save the files in the correct folders
   - Run the test

4. When it finishes, you will see the test result: **passed** or **failed**

### Step 12: Review the Code Quality

After Claude creates the test, run a code review to fix any pattern issues:

1. In Claude Code, type:
   ```
   /pr
   ```
2. Claude will scan all generated files and check them against the framework's coding standards
3. If everything is correct, you will see: **PR REVIEW: APPROVED**
4. If there are issues, Claude will show you what is wrong and ask how you want to fix them. Choose **Option 1 (Fix all)** to let Claude fix the issues automatically.

> **Always run `/pr` after creating tests.** This ensures your test code follows the correct architecture patterns.

### Step 13: Create More Tests

Repeat Steps 11-12 with different requirements for your application.

> **Tip:** The more detail you put in your requirement (steps, expected results, URLs), the better the generated test will be. Vague requirements produce vague tests.

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
| **BrowserInterface** | Wraps browser automation (Selenium) | `BrowserInterface.click()`, `.type()` |

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
git clone https://github.com/isagawa-qa/platform-selenium.git
cd platform-selenium
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

The platform includes a QA domain pack and a pre-configured `CLAUDE.md` that drives the kernel. On first run, the agent reads these instructions, analyzes your codebase, and configures itself to enforce the 5-layer architecture.

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
│   │   └── browser_interface.py   # BrowserInterface (Selenium wrapper)
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
