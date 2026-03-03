# Architecture

## 5-Layer Architecture

Every test in the Isagawa QA Platform follows a strict separation of concerns. Each layer has one job:

| Layer | Responsibility | Example |
|-------|---------------|---------|
| **Test** | Says what should happen, asserts the result | `test_e2e_create_employee_and_assign_task()` |
| **Role** | Coordinates tasks into business workflows | `TaskManager.assign_task_to_employee()` |
| **Task** | Performs one domain operation across pages | `create_task_assigned_to()` |
| **Page Object (POM)** | Knows where elements are on one page | `TasksPage.enter_task_title("Analyze data")` |
| **BrowserInterface** | Wraps browser automation (Selenium) | `BrowserInterface.click()`, `.enter_text()` |

```
Test (Arrange / Act / Assert)
  └─→ Role (multi-task workflow, user persona)
       └─→ Task (single domain operation)
            └─→ Page Object (one page, atomic actions, fluent API)
                 └─→ BrowserInterface (Selenium wrapper, waits, logging)
```

---

## Layer Details

### Layer 1: BrowserInterface

The foundation layer. Wraps Selenium WebDriver with:

- Explicit waits (no `time.sleep`)
- Automatic retry on stale elements
- Consistent logging via `autologger`
- Screenshot capture on failure

All browser interaction flows through this single interface. Page Objects never call Selenium directly.

### Layer 2: Page Object (POM)

Each page in the application gets one Page Object class.

```python
from selenium.webdriver.common.by import By
from interfaces.browser_interface import BrowserInterface


class EmployeesPage:

    def __init__(self, browser: BrowserInterface):
        """Compose BrowserInterface — NO inheritance."""
        self.browser = browser

    # ==================== LOCATORS (Class Constants) ====================

    EMPLOYEES_NAV_LINK = (By.CSS_SELECTOR, "[data-testid='nav-employees']")
    CREATE_EMPLOYEE_BUTTON = (By.CSS_SELECTOR, "[data-testid='button-create-employee']")
    EMPLOYEE_NAME_INPUT = (By.CSS_SELECTOR, "[data-testid='input-agent-name']")
    EMPLOYEE_ROLE_COMBOBOX = (By.CSS_SELECTOR, "[data-testid='select-agent-role']")
    ANALYST_ROLE_OPTION = (By.XPATH, "//*[@role='option'][contains(., 'Analyst')]")
    EMPLOYEE_DESCRIPTION_INPUT = (By.CSS_SELECTOR, "[data-testid='input-agent-description']")
    EMPLOYEE_CAPABILITIES_INPUT = (By.CSS_SELECTOR, "[data-testid='input-agent-capabilities']")
    SUBMIT_CREATE_BUTTON = (By.CSS_SELECTOR, "[data-testid='button-submit-create']")
    EMPLOYEE_CREATED_TOAST = (By.XPATH, "//*[@role='status']//*[contains(., 'Employee created')]")

    # ==================== ATOMIC METHODS (One UI Action) ====================

    def navigate_to_employees(self) -> "EmployeesPage":
        self.browser.click(*self.EMPLOYEES_NAV_LINK)
        return self

    def wait_for_employees_page(self, timeout: int = 10) -> "EmployeesPage":
        self.browser.wait_for_element_visible(*self.CREATE_EMPLOYEE_BUTTON, timeout=timeout)
        return self

    def click_create_employee(self) -> "EmployeesPage":
        self.browser.click(*self.CREATE_EMPLOYEE_BUTTON)
        return self

    def enter_employee_name(self, name: str) -> "EmployeesPage":
        self.browser.enter_text(*self.EMPLOYEE_NAME_INPUT, name)
        return self

    def click_role_dropdown(self) -> "EmployeesPage":
        self.browser.click(*self.EMPLOYEE_ROLE_COMBOBOX)
        return self

    def select_analyst_role(self) -> "EmployeesPage":
        self.browser.click(*self.ANALYST_ROLE_OPTION)
        return self

    def click_submit_create(self) -> "EmployeesPage":
        self.browser.click(*self.SUBMIT_CREATE_BUTTON)
        return self

    # ==================== STATE-CHECK METHODS (For Assertions) ====================

    def is_employee_created_toast_displayed(self) -> bool:
        return self.browser.is_element_displayed(*self.EMPLOYEE_CREATED_TOAST, timeout=5)

    def is_employee_displayed_in_list(self, name: str) -> bool:
        locator = (By.XPATH, f"//*[contains(., '{name}')]")
        return self.browser.is_element_displayed(*locator, timeout=5)

    def is_employee_idle(self, name: str) -> bool:
        locator = (By.XPATH, f"//*[contains(., '{name}')]/../..//*[contains(., 'Idle')]")
        return self.browser.is_element_displayed(*locator, timeout=5)
```

**Key conventions:**
- `__init__` receives `BrowserInterface` via composition (no inheritance)
- Locators are class-level constants (tuples of `By` strategy + selector)
- Atomic methods — one UI action per method
- Return `self` for method chaining (fluent API)
- State-check methods for assertions (`is_*`, `get_*`, `has_*`)
- No `@autologger` decorator on POM methods

### Layer 3: Task

Tasks perform one domain operation, composing multiple Page Object calls into a fluent chain.

```python
from interfaces.browser_interface import BrowserInterface
from pages.common.login_page import LoginPage
from pages.task_management.tasks_page import TasksPage
from resources.utilities import autologger


class TaskManagementTasks:

    def __init__(self, browser: BrowserInterface):
        self.browser = browser
        self.login_page = LoginPage(browser)
        self.tasks_page = TasksPage(browser)

    @autologger.automation_logger("Task")
    def login(self, login_url: str, email: str, password: str) -> None:
        (self.login_page
            .navigate(login_url)
            .wait_for_login_button_visible()
            .click_log_in()
            .wait_for_email_visible()
            .enter_email(email)
            .enter_password(password)
            .click_sign_in())

    @autologger.automation_logger("Task")
    def create_task_assigned_to(self, title: str, description: str, assignee_name: str) -> None:
        (self.tasks_page
            .navigate_to_tasks()
            .wait_for_tasks_page()
            .click_create_task()
            .wait_for_modal_visible()
            .enter_task_title(title)
            .enter_task_description(description)
            .click_assignee_dropdown()
            .select_assignee_by_name(assignee_name)
            .uncheck_auto_run()
            .click_submit_task()
            .wait_for_task_created_toast())
```

**Key conventions:**
- `@autologger("Task")` on every method (not constructor)
- Composes Page Objects via `__init__`
- One domain operation per method
- Fluent API chaining for readable sequences
- Never return values — Tests assert through POM state-check methods

### Layer 4: Role

Roles represent user personas and orchestrate Tasks into complete business workflows.

```python
from interfaces.browser_interface import BrowserInterface
from resources.utilities import autologger
from tasks.task_management.task_management_tasks import TaskManagementTasks


class TaskManager:

    @autologger.automation_logger("Role Constructor")
    def __init__(self, browser_interface: BrowserInterface, login_url: str, email: str, password: str):
        self.browser = browser_interface
        self.login_url = login_url
        self.email = email
        self.password = password
        self.task_management_tasks = TaskManagementTasks(browser_interface)

    @autologger.automation_logger("Role")
    def assign_task_to_employee(self, title: str, description: str, assignee_name: str) -> None:
        """Login and create a task assigned to an employee."""
        self.task_management_tasks.login(self.login_url, self.email, self.password)
        self.task_management_tasks.create_task_assigned_to(title, description, assignee_name)

    @autologger.automation_logger("Role")
    def assign_task_to_employee_continue(self, title: str, description: str, assignee_name: str) -> None:
        """Create a task (already logged in from a prior Role call)."""
        self.task_management_tasks.create_task_assigned_to(title, description, assignee_name)
```

**Key conventions:**
- `@autologger("Role")` on workflow methods
- `@autologger("Role Constructor")` on `__init__`
- Composes Task modules
- Workflow methods call multiple Tasks
- `_continue` variant skips login for integration tests (shared browser session)
- Never return values

### Layer 5: Test

Tests are thin — they call one Role workflow method per phase and assert via POM state-check methods.

```python
import pytest
from resources.utilities import autologger
from roles.employee_management.employee_manager import EmployeeManager
from roles.task_management.task_manager import TaskManager
from pages.employee_management.employees_page import EmployeesPage
from pages.task_management.tasks_page import TasksPage


class TestE2ECreateEmployeeAndAssignTask:

    @pytest.fixture(autouse=True)
    def setup(self, browser, config, test_users):
        """Pytest fixture wires browser, config, and test data into the test class."""
        self.browser = browser
        self.config = config
        self.test_users = test_users
        self.employees_page = EmployeesPage(self.browser)
        self.tasks_page = TasksPage(self.browser)

    @pytest.mark.task_management
    @pytest.mark.employee_management
    @autologger.automation_logger("Test")
    def test_e2e_create_employee_and_assign_task(self):
        # Arrange
        credentials = self.test_users["admin"]
        login_url = self.config["url"] + "/auth/login"

        employee_name = "Research Assistant"
        employee_description = "Analyzes market trends and competitor data"
        employee_capabilities = "data analysis, reporting, research"

        task_title = "Research competitor pricing"
        task_description = "Analyze competitor pricing strategies and create a summary report"

        employee_manager = EmployeeManager(
            self.browser, login_url=login_url,
            email=credentials["email"], password=credentials["password"]
        )
        task_manager = TaskManager(
            self.browser, login_url=login_url,
            email=credentials["email"], password=credentials["password"]
        )

        # Act — Phase 1: Create the employee
        employee_manager.create_employee(
            name=employee_name,
            description=employee_description,
            capabilities=employee_capabilities
        )

        # Assert — Phase 1: Employee created
        assert self.employees_page.is_employee_created_toast_displayed()
        assert self.employees_page.is_employee_displayed_in_list(employee_name)

        # Act — Phase 2: Assign task to the employee (already logged in)
        task_manager.assign_task_to_employee_continue(
            title=task_title,
            description=task_description,
            assignee_name=employee_name
        )

        # Assert — Phase 2: Task created and assigned
        assert self.tasks_page.is_task_created_toast_displayed()
        assert self.tasks_page.is_task_displayed_in_list(task_title)
        assert self.tasks_page.is_task_assigned_to(employee_name)
```

**Key conventions:**
- `@autologger("Test")` decorator
- AAA pattern: Arrange / Act / Assert
- `pytest.fixture(autouse=True)` wires browser, config, and test data (defined in `tests/conftest.py`)
- Multi-role workflows: two Roles share one browser session
- Causal dependency: employee name (Phase 1 output) becomes task assignee (Phase 2 input)
- Assert through POM state-check methods only

---

## Why 5 Layers?

The integration test above demonstrates why each layer earns its place:

```
Test: test_e2e_create_employee_and_assign_task()
│
├─ Phase 1: EmployeeManager.create_employee()          ← Role
│   ├─ EmployeeManagementTasks.login()                  ← Task
│   │   └─ LoginPage: navigate → click → enter → sign in    ← POM → BrowserInterface
│   └─ EmployeeManagementTasks.create_employee()        ← Task
│       └─ EmployeesPage: navigate → fill form → submit     ← POM → BrowserInterface
│
├─ Assert: employee toast, employee in list
│
├─ Phase 2: TaskManager.assign_task_to_employee_continue()  ← Role (skips login)
│   └─ TaskManagementTasks.create_task_assigned_to()    ← Task
│       └─ TasksPage: navigate → fill form → assign → submit    ← POM → BrowserInterface
│
└─ Assert: task toast, task in list, assigned to employee
```

Remove any layer and the architecture degrades:
- **Remove Roles** → Tests must orchestrate tasks directly (duplication across tests)
- **Remove Tasks** → POM calls scatter across Roles (10+ UI steps inline per workflow)
- **Remove POMs** → Locators and Selenium calls leak into Tasks (unmaintainable)
- **Remove BrowserInterface** → Exception handling and waits duplicated in every POM

---

## Decorator Strategy

The `@autologger.automation_logger` decorator provides layer-by-layer runtime tracing in the terminal. You can watch the full execution flow as it happens: which Role called which Task called which POM method.

| Layer | Decorator | On Constructor? |
|-------|-----------|-----------------|
| **POM** | None | No |
| **Task** | `@autologger("Task")` | No |
| **Role** | `@autologger("Role")` | Yes — `@autologger("Role Constructor")` |
| **Test** | `@autologger("Test")` | No |

---

## Data Flow

```
Test Data (config, test_users via pytest fixtures)
  ↓
Test (reads data, creates Roles, calls workflow methods)
  ↓
Role (orchestrates Tasks with credentials and parameters)
  ↓
Task (chains POM methods into domain operations)
  ↓
Page Object (calls BrowserInterface for each UI action)
  ↓
BrowserInterface (Selenium WebDriver)
  ↓
Browser (Chrome / Brave)
```

**Assertions flow upward:** Tests assert by calling POM state-check methods. Tasks and Roles never return values — this keeps the assertion boundary clean.

---

## Key Rules

| Rule | Layer |
|------|-------|
| Locators live ONLY in Page Objects | POM |
| No return values from Tasks or Roles | Task, Role |
| Return `self` from POM atomic methods | POM |
| Assert via POM state-check methods | Test |
| `@autologger` on Task, Role, and Test methods | All (except POM) |
| Multi-role workflows supported | Test |
| `_continue` variants skip login for shared sessions | Role |

---

## Reference Implementations

Browse `framework/_reference/` for canonical code patterns:

| Layer | File |
|-------|------|
| **POM** | `pages/login_page.py`, `pages/employees_page.py`, `pages/tasks_page.py` |
| **Task** | `tasks/employee_management_tasks.py`, `tasks/task_management_tasks.py` |
| **Role** | `roles/employee_manager.py`, `roles/task_manager.py` |
| **Test** | `tests/test_e2e_create_employee_and_assign_task.py` |

These are the authoritative source. When in doubt, read the reference implementations.
