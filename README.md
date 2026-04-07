# Isagawa QA Platform

### AI Execution Management for Test Automation

> "AI can generate tests. But can you trust it to execute correctly?"

Most AI tools watch what happened and report after the fact. Isagawa **enforces how AI works** — gating every action at runtime so the AI can only do it right.

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
5. You will see a **sparkle icon (&#10033;)** appear in the top-right area of VS Code

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

1. In VS Code, click **File** > **Open Folder**
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

1. Click the **sparkle icon (&#10033;)** in VS Code to open Claude Code
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

1. In Claude Code (click the **sparkle icon &#10033;** if it is not open), type:
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

**The cycle:** Generate > breaks something > fix > generate > breaks it differently > start over.

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
| **BrowserInterface** | Wraps browser automation (Selenium) | `BrowserInterface.click()`, `.type()` |

```
Test (Arrange / Act / Assert)
  └── Role (multi-task workflow, user persona)
       └── Task (single domain operation)
            └── Page Object (one page, atomic actions, fluent API)
                 └── BrowserInterface (Selenium wrapper, waits, logging)
```

### Key Rules

- Locators live *only* in Page Objects, never in Tasks, Roles, or Tests
- Tasks and Roles never return values — Tests assert through POM state-check methods
- Tests orchestrate Roles to execute business workflows — multi-role workflows are supported
- `@autologger` decorator on every Task, Role, and Test method

---

## Real Code Examples

The framework ships with canonical reference implementations in `framework/_reference/`. The AI agent reads these before generating any code — ensuring every test follows the exact same patterns.

### Page Object (LoginPage)

Page Objects own all locators for a single page. Methods are atomic (one UI action) and return `self` for fluent chaining:

```python
from selenium.webdriver.common.by import By
from interfaces.browser_interface import BrowserInterface


class LoginPage:
    """
    - NO decorators on methods
    - Locators as class constants
    - Atomic methods (one UI action)
    - Return self for chaining
    - State-check methods for assertions
    """

    def __init__(self, browser: BrowserInterface):
        """Compose BrowserInterface — NO inheritance."""
        self.browser = browser

    # ==================== LOCATORS (Class Constants) ====================

    LOG_IN_BUTTON = (By.CSS_SELECTOR, "[data-testid='button-goto-login']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "[data-testid='input-email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "[data-testid='input-password']")
    SIGN_IN_BUTTON = (By.CSS_SELECTOR, "[data-testid='button-sign-in']")

    # ==================== ATOMIC METHODS ====================

    def click_log_in(self) -> "LoginPage":
        """Click the Log In button to reveal the login form."""
        self.browser.click(*self.LOG_IN_BUTTON)
        return self

    def enter_email(self, email: str) -> "LoginPage":
        """Enter email address."""
        self.browser.enter_text(*self.EMAIL_INPUT, email)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        """Enter password."""
        self.browser.enter_text(*self.PASSWORD_INPUT, password)
        return self

    def click_sign_in(self) -> "LoginPage":
        """Click the Sign In button."""
        self.browser.click(*self.SIGN_IN_BUTTON)
        return self

    # ==================== STATE-CHECK METHODS ====================

    def is_on_dashboard(self) -> bool:
        """Check if redirected to dashboard after login."""
        return "/dashboard" in self.browser.get_current_url()
```

### Task (EmployeeManagementTasks)

Tasks compose Page Objects and perform one domain operation. Methods chain POM calls fluently:

```python
from interfaces.browser_interface import BrowserInterface
from _reference.pages.login_page import LoginPage
from _reference.pages.employees_page import EmployeesPage
from resources.utilities import autologger


class EmployeeManagementTasks:
    """
    - @autologger("Task") on all methods
    - Composes Page Objects
    - One domain operation per method
    - NO return values
    """

    def __init__(self, browser: BrowserInterface):
        self.browser = browser
        self.login_page = LoginPage(browser)
        self.employees_page = EmployeesPage(browser)

    @autologger.automation_logger("Task")
    def login(self, login_url: str, email: str, password: str) -> None:
        """Login with provided credentials."""
        (self.login_page
            .navigate(login_url)
            .wait_for_login_button_visible()
            .click_log_in()
            .wait_for_email_visible()
            .enter_email(email)
            .enter_password(password)
            .click_sign_in())

    @autologger.automation_logger("Task")
    def create_employee(self, name: str, description: str = "",
                        capabilities: str = "") -> None:
        """Navigate to employees page and create a new employee."""
        (self.employees_page
            .navigate_to_employees()
            .wait_for_employees_page()
            .click_create_employee()
            .wait_for_modal_visible()
            .enter_employee_name(name)
            .click_role_dropdown()
            .select_analyst_role()
            .enter_employee_description(description)
            .enter_employee_capabilities(capabilities)
            .click_submit_create()
            .wait_for_employee_created_toast())
```

### Role (EmployeeManager)

Roles represent user personas. They compose Tasks and orchestrate multi-step business workflows:

```python
from interfaces.browser_interface import BrowserInterface
from resources.utilities import autologger
from _reference.tasks.employee_management_tasks import EmployeeManagementTasks


class EmployeeManager:
    """
    - @autologger("Role") on workflow methods
    - @autologger("Role Constructor") on __init__
    - Composes Task modules
    - Workflow methods call MULTIPLE tasks
    - NO return values
    """

    @autologger.automation_logger("Role Constructor")
    def __init__(self, browser_interface: BrowserInterface, login_url: str,
                 email: str, password: str):
        self.browser = browser_interface
        self.login_url = login_url
        self.email = email
        self.password = password
        self.employee_management_tasks = EmployeeManagementTasks(browser_interface)

    @autologger.automation_logger("Role")
    def create_employee(self, name: str, description: str = "",
                        capabilities: str = "") -> None:
        """
        Complete workflow: Login and create an employee.

        Orchestrates MULTIPLE task operations:
        1. Login with credentials
        2. Create employee with specified details
        """
        self.employee_management_tasks.login(
            self.login_url, self.email, self.password)
        self.employee_management_tasks.create_employee(
            name, description, capabilities)
```

### Test (End-to-End Integration)

Tests use the AAA pattern (Arrange, Act, Assert). They orchestrate Roles and assert through Page Object state-check methods:

```python
import pytest
from resources.utilities import autologger
from _reference.roles.employee_manager import EmployeeManager
from _reference.roles.task_manager import TaskManager
from _reference.pages.employees_page import EmployeesPage
from _reference.pages.tasks_page import TasksPage


class TestE2ECreateEmployeeAndAssignTask:
    """
    - @autologger("Test") decorator
    - MULTIPLE Role workflow calls (integration test)
    - Assert via Page Object state-check methods
    """

    @pytest.fixture(autouse=True)
    def setup(self, browser, config, test_users):
        self.browser = browser
        self.config = config
        self.test_users = test_users
        self.employees_page = EmployeesPage(self.browser)
        self.tasks_page = TasksPage(self.browser)

    @pytest.mark.employee_management
    @pytest.mark.task_management
    @autologger.automation_logger("Test")
    def test_e2e_create_employee_and_assign_task(self):
        """Integration test: create employee then assign a task."""

        # ==================== ARRANGE ====================
        credentials = self.test_users["admin"]
        login_url = self.config["url"] + "/auth/login"
        employee_name = "Research Assistant"
        task_title = "Research competitor pricing"

        employee_manager = EmployeeManager(
            self.browser, login_url=login_url,
            email=credentials["email"], password=credentials["password"]
        )
        task_manager = TaskManager(
            self.browser, login_url=login_url,
            email=credentials["email"], password=credentials["password"]
        )

        # ==================== ACT — Phase 1 ====================
        employee_manager.create_employee(
            name=employee_name,
            description="Analyzes market trends",
            capabilities="data analysis, reporting"
        )

        # ==================== ASSERT — Phase 1 ====================
        assert self.employees_page.is_employee_created_toast_displayed(), \
            "Toast 'Employee created' should be displayed"
        assert self.employees_page.is_employee_displayed_in_list(employee_name), \
            f"Employee '{employee_name}' should be in the list"

        # ==================== ACT — Phase 2 ====================
        task_manager.assign_task_to_employee_continue(
            title=task_title,
            description="Analyze competitor pricing strategies",
            assignee_name=employee_name
        )

        # ==================== ASSERT — Phase 2 ====================
        assert self.tasks_page.is_task_created_toast_displayed(), \
            "Toast 'Task created' should be displayed"
        assert self.tasks_page.is_task_assigned_to(employee_name), \
            f"Task should be assigned to '{employee_name}'"
```

---

## BrowserInterface

The foundation layer. Every browser interaction flows through BrowserInterface — navigation, clicking, typing, waiting, screenshots. No test code touches Selenium directly.

```python
class BrowserInterface:
    """Selenium WebDriver wrapper with logging, screenshots, and waits."""

    DEFAULT_EXPLICIT_WAIT = 20

    def __init__(self, driver: WebDriver, config: dict, logger: logging.Logger):
        self.driver = driver
        self.config = config
        self.logger = logger

    def navigate_to(self, url: str) -> None:
        """Navigate to a URL."""
        self.driver.get(url)
        self.logger.info(f"Navigated to: {url}")

    def click(self, by: By, value: str) -> None:
        """Click an element after waiting for it to be clickable."""
        element = WebDriverWait(self.driver, self.explicit_wait).until(
            EC.element_to_be_clickable((by, value)))
        element.click()

    def enter_text(self, by: By, value: str, text: str) -> None:
        """Clear and type text into an element."""
        element = WebDriverWait(self.driver, self.explicit_wait).until(
            EC.visibility_of_element_located((by, value)))
        element.clear()
        element.send_keys(text)

    def wait_for_element_visible(self, by: By, value: str,
                                  timeout: int = None) -> WebElement:
        """Wait for element to be visible."""
        wait_time = timeout or self.explicit_wait
        return WebDriverWait(self.driver, wait_time).until(
            EC.visibility_of_element_located((by, value)))

    def get_current_url(self) -> str:
        """Get the current page URL."""
        return self.driver.current_url
```

**Critical rule:** Before writing ANY browser interaction in a Page Object, check if BrowserInterface already has the method. If it doesn't, ask before creating a workaround. Never use `time.sleep()` — always use explicit waits.

---

## Autologger

Every Task, Role, and Test method gets the `@autologger` decorator. It logs entry/exit with timing automatically:

```python
def automation_logger(category=""):
    """
    Decorator factory for logging function entry/exit.

    Usage:
        @autologger.automation_logger("Test")
        def test_login(self):
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            prefix = f"[{category}] " if category else ""
            logger.info(f"{prefix}{func.__name__} - START")
            start_time = datetime.now()
            try:
                result = func(*args, **kwargs)
                duration = (datetime.now() - start_time).total_seconds()
                logger.info(f"{prefix}{func.__name__} - END ({duration:.2f}s)")
                return result
            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds()
                logger.error(f"{prefix}{func.__name__} - FAILED ({duration:.2f}s)")
                raise
        return wrapper
    return decorator
```

**Log output example:**
```
[Role Constructor] __init__ - START
[Task] login - START
[Task] login - END (3.42s)
[Task] create_employee - START
[Task] create_employee - END (5.17s)
[Role] create_employee - END (8.59s)
[Test] test_e2e_create_employee_and_assign_task - END (12.31s)
```

---

## Test Configuration (conftest.py)

Pytest fixtures wire everything together — driver, config, credentials, and BrowserInterface:

```python
@pytest.fixture
def driver(request):
    """New browser driver per test. Supports Chrome and Brave."""
    headless = request.config.getoption("--headless")
    browser_type = request.config.getoption("--browser")
    chromedriver = create_driver(headless=headless, browser=browser_type)
    try:
        yield chromedriver
    finally:
        chromedriver.quit()


@pytest.fixture(scope="session")
def config(request):
    """Load environment config (base URL, settings)."""
    env_id = request.config.getoption("--env")
    config_path = PROJECT_ROOT / "framework" / "resources" / "config" / "environment_config.json"
    with open(config_path) as f:
        environments = json.load(f)
    yield environments[env_id]


@pytest.fixture(scope="session")
def test_users():
    """Load test user credentials."""
    users_path = PROJECT_ROOT / "tests" / "data" / "test_users.json"
    with open(users_path) as f:
        yield json.load(f)


@pytest.fixture
def browser(driver, config):
    """BrowserInterface wrapper with all dependencies."""
    yield BrowserInterface(driver, config, logger)
```

**Running tests:**
```bash
# Default (Chrome, headed)
pytest tests/

# Headless Chrome
pytest tests/ --headless

# Brave browser
pytest tests/ --browser brave

# Specific environment
pytest tests/ --env staging

# With HTML report
pytest tests/ --html=report.html --self-contained-html
```

---

## The 5-Step QA Workflow

When you invoke `/qa-workflow`, the agent follows a 5-step process with self-enforcing gates at every step:

```
/qa-workflow
    │
Step 1: USER INPUT
    Receive requirement, URL, credentials
    Gate: requirement has persona, action, URL
    │
Step 2: PRE-FLIGHT
    Verify URLs accessible, check environment config
    Gate: all URLs respond, config file valid
    │
Step 3: AI PROCESSING
    Open browser via Playwright MCP, discover page elements
    Gate: element map captured for each URL
    │
Step 4: CONSTRUCTION
    Read reference files, generate Page Objects, Tasks, Roles, Test
    Gate: all files follow 5-layer architecture, locators only in POMs
    │
Step 5: EXECUTION
    Run pytest, capture results
    Gate: test passes or failure triaged with user
    │
COMPLETE → /kernel/complete → lesson recorded
```

### Gate Contract (Self-Enforcement)

Every gate does 6 things:

| # | Action | Description |
|---|--------|-------------|
| 1 | **VALIDATE** | Check output against step criteria |
| 2 | **TEACH** | Record lesson on success or failure |
| 3 | **LEARN** | Send lesson to /kernel/learn for storage |
| 4 | **BLOCK** | Prevent next step if validation fails |
| 5 | **SAVE** | Persist state for next step |
| 6 | **LOOP** | Retry with teaching if recoverable failure |

### HITL Protocol (Human-In-The-Loop)

On ANY failure, the agent stops and asks:

```
FAILURE at Step [N]: [brief description]

Error: [exact message]
Location: [file:line or URL]

HOW SHOULD WE PROCEED?
1. I'll fix it — tell me what to change
2. You investigate — show me more context
3. Skip this — continue without it
4. Abort — stop workflow entirely
```

The agent never loops through autonomous fixes. It stops, reports, and waits for your decision.

### Forbidden Patterns

```python
# NEVER do this in Page Objects:
import time
while len(self.browser.get_window_handles()) < 2:
    time.sleep(0.5)  # NO — ask for BrowserInterface method instead

# CORRECT — use existing BrowserInterface method:
self.browser.wait_for_new_window(timeout=10)
```

---

## The Kernel (Enforcement Engine)

The Isagawa Kernel is the enforcement engine that runs inside Claude Code. It's not a linter or a post-hoc checker — it **gates every action in real-time**.

### What It Does

1. **Self-builds** — On first run, the kernel reads your codebase, extracts patterns, and builds its own protocol
2. **Self-enforces** — Every 10 actions, the hook forces the agent to re-read its protocol (`/kernel/anchor`)
3. **Self-improves** — After every failure, `/kernel/learn` updates the protocol permanently

### How It Works

```
session-start → anchor → WORK ──────────────────→ complete
                   ↑         ↓                       ↑
                   └─ every 10 actions ←─────────────┘
                             ↓
                   failure? → fix → learn (MANDATORY)
```

### Universal Gate Enforcer

The hook script (`universal-gate-enforcer.py`) intercepts every Write, Edit, and Bash command. It blocks if:

1. **Session not started** — Must invoke `/kernel/session-start` first
2. **Lesson not recorded** — Test failed but `/kernel/learn` wasn't called
3. **Protocol not anchored** — Must re-read protocol via `/kernel/anchor`
4. **Action limit reached** — 10 actions since last anchor, time to re-center

```python
# Simplified gate logic:
if not session_state.get('session_started'):
    BLOCK → "Invoke /kernel/session-start"

if session_state.get('needs_learn'):
    BLOCK → "Invoke /kernel/learn"

if not domain_state.get('anchored'):
    BLOCK → "Invoke /kernel/anchor"

if actions_since_anchor > actions_limit:
    BLOCK → "Invoke /kernel/anchor"
```

The agent cannot bypass these gates. Every failure becomes a permanent lesson. Every lesson makes the next test better.

---

## How It Works (End-to-End)

1. Describe the persona, URL, and workflow you want to test
2. The AI discovers page elements via Playwright MCP and generates code following the 5-layer architecture
3. Tests are executed with human-in-the-loop triage on failure
4. Every fix makes the system permanently smarter — the same mistake cannot happen again

```
Input:
  "As an employee manager, I want to create an employee
   and assign them a task"
  URL: https://myapp.com/employees, https://myapp.com/tasks

  │
  ├── Discover: Playwright MCP opens browser, maps all elements
  ├── Generate: LoginPage, EmployeesPage, TasksPage (POMs)
  │             EmployeeManagementTasks, TaskManagementTasks (Tasks)
  │             EmployeeManager, TaskManager (Roles)
  │             TestE2ECreateEmployeeAndAssignTask (Test)
  ├── Execute: pytest runs, 1 passed in 12.31s
  └── Learn: patterns recorded, next test is better
```

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

```bash
claude                    # Start Claude Code in the project directory
> start                   # Agent runs domain-setup automatically
                          # --> "Restart Claude Code to activate hooks"
claude                    # Restart
> continue                # Agent anchors and is ready
```

### 4. Generate your first test

```bash
# Inside Claude Code:
/qa-workflow
```

### 5. Review generated code

```bash
# Inside Claude Code:
/pr
```

For detailed setup instructions, see [Getting Started](docs/getting-started.md).

---

## Project Structure

```
platform-selenium/
├── .claude/
│   ├── commands/                    # Kernel + QA workflow commands
│   │   ├── qa-workflow.md           # /qa-workflow — 5-step test generation
│   │   ├── qa-workflow-dev.md       # /qa-workflow-dev — dev mode
│   │   └── pr.md                    # /pr — code review against architecture
│   ├── hooks/                       # Gate enforcer + test failure detector
│   │   └── universal-gate-enforcer.py
│   ├── lessons/                     # Learned anti-patterns
│   │   └── lessons.md
│   ├── skills/
│   │   ├── kernel-domain-setup/     # Self-building kernel setup
│   │   └── qa-management-layer/     # 5-step QA workflow skill
│   │       ├── SKILL.md             # Entry point, rules, reading order
│   │       ├── workflow.md          # 5-step index with data flow
│   │       ├── gate-contract.md     # Validation contract (6 responsibilities)
│   │       └── steps/               # Step-specific criteria
│   │           ├── step-01.md       # User Input
│   │           ├── step-02.md       # Pre-flight
│   │           ├── step-03.md       # AI Processing (element discovery)
│   │           ├── step-04.md       # Construction (code generation)
│   │           └── step-05.md       # Execution (pytest run)
│   └── settings.json                # Hook configuration
├── framework/
│   ├── _reference/                  # Canonical code patterns (read-before-write)
│   │   ├── pages/                   # POM reference implementations
│   │   │   ├── login_page.py
│   │   │   ├── employees_page.py
│   │   │   └── tasks_page.py
│   │   ├── tasks/                   # Task reference implementations
│   │   │   ├── employee_management_tasks.py
│   │   │   └── task_management_tasks.py
│   │   ├── roles/                   # Role reference implementations
│   │   │   ├── employee_manager.py
│   │   │   └── task_manager.py
│   │   └── tests/                   # Test reference implementations
│   │       └── test_e2e_create_employee_and_assign_task.py
│   ├── interfaces/
│   │   └── browser_interface.py     # BrowserInterface (Selenium wrapper)
│   └── resources/
│       ├── chromedriver/            # Driver factory
│       ├── config/                  # Environment configuration
│       │   └── environment_config.json
│       └── utilities/               # Autologger decorator
│           └── autologger.py
├── tests/
│   ├── data/                        # Test data (credentials, fixtures)
│   │   └── test_users.json
│   └── conftest.py                  # Pytest fixtures and configuration
├── docs/                            # Architecture, getting started
│   ├── architecture.md
│   └── getting-started.md
├── .mcp.json                        # Playwright MCP server config
├── CLAUDE.md                        # Kernel instructions
├── CONTRIBUTING.md                  # Architecture rules and PR process
├── LICENSE                          # MIT
└── requirements.txt
```

---

## The Bigger Picture

QA is one domain. The Isagawa Kernel supports **any** domain.

The kernel is domain-agnostic — it enforces how AI executes, not just what it generates. What you see here in QA can be applied to:

- Code generation and review
- Content creation workflows
- Data pipeline management
- Healthcare compliance
- Financial auditing
- Any process where AI needs to execute correctly, not just generate output

The kernel is available separately. Domain packs — pre-loaded with patterns, anti-patterns, and quality gates for specific verticals — are built by the [Domain Spec Factory](https://github.com/isagawa-co/domain-spec-factory).

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

## Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/qa-workflow` | Run 5-step test generation workflow | Creating new tests |
| `/qa-workflow-dev` | Run with dev permissions | Development/debugging |
| `/pr` | Code review against architecture rules | After generating tests |
| `/kernel/anchor` | Re-center on protocol | Automatic every 10 actions |
| `/kernel/learn` | Record lesson after failure | After fixing any issue |

---

## Services

We deliver a highly scalable, maintainable, enterprise-grade test automation framework powered by an AI agent managed by our own enforcement kernel. We build the entire test solution: login credentials, data management, environment configuration, and page object architecture. Your team owns the entire tech stack: a true AI-native test automation framework built on Claude Code. We also train your team to create and maintain test scripts on their own.

### What We Deliver

Depending on your needs, the full solution can include:

- Complete 5-layer test architecture configured for your application
- Login/auth credential management
- Test data management
- Environment configuration (dev, staging, production)
- Page Object library for your application's pages
- Team training on test creation and maintenance

### Demo

We'll build working tests on **YOUR** site in 60 minutes. No discovery phase. No proposal. No waiting.

**[alain@isagawa.co](mailto:alain@isagawa.co)** | **[DM on LinkedIn](https://www.linkedin.com/in/alain-ignacio-54b9823)**

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

Built with the [Isagawa Kernel](https://github.com/isagawa-co/isagawa-kernel) — self-building, self-improving, safety-first.
