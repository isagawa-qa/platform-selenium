# Architecture

## 5-Layer Architecture

Every test in the Isagawa QA Platform follows a strict separation of concerns. Each layer has one job:

| Layer | Responsibility | Example |
|-------|---------------|---------|
| **Test** | Says what should happen, asserts the result | `test_submit_inquiry()` |
| **Role** | Coordinates tasks into business workflows | `CustomerRole.submit_new_inquiry()` |
| **Task** | Performs one domain operation across pages | `search_and_create_customer()` |
| **Page Object (POM)** | Knows where elements are on one page | `InquiryFormPage.select_type("Service")` |
| **WebInterface** | Wraps browser automation (Selenium) | `BrowserInterface.click()`, `.type()` |

```
Test (Arrange / Act / Assert)
  └─→ Role (multi-task workflow, user persona)
       └─→ Task (single domain operation)
            └─→ Page Object (one page, atomic actions, fluent API)
                 └─→ BrowserInterface (Selenium wrapper, waits, logging)
```

---

## Layer Details

### Layer 1: WebInterface (BrowserInterface)

The foundation layer. Wraps Selenium WebDriver with:

- Explicit waits (no `time.sleep`)
- Automatic retry on stale elements
- Consistent logging via `autologger`
- Screenshot capture on failure

All browser interaction flows through this single interface. Page Objects never call Selenium directly.

### Layer 2: Page Object (POM)

Each page in the application gets one Page Object class.

```python
class LoginPage:
    # Locators as class constants — ONLY place locators live
    EMAIL_INPUT = (By.CSS_SELECTOR, "#email")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "#password")
    SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit']")

    def enter_email(self, email):
        self.browser.type(*self.EMAIL_INPUT, email)
        return self  # Fluent API — return self for chaining

    def enter_password(self, password):
        self.browser.type(*self.PASSWORD_INPUT, password)
        return self

    def click_submit(self):
        self.browser.click(*self.SUBMIT_BTN)
        return self

    # State-check method — used by Tests for assertions
    def is_logged_in(self):
        return self.browser.is_element_present(*self.DASHBOARD_HEADER)
```

**Key conventions:**
- Locators are class-level constants (tuples)
- Atomic methods — one UI action per method
- Return `self` for method chaining (fluent API)
- State-check methods for assertions (`is_*`, `get_*`, `has_*`)
- No `@autologger` decorator on POM methods

### Layer 3: Task

Tasks perform one domain operation, composing multiple Page Object calls.

```python
class LoginTasks:
    def __init__(self, browser):
        self.login_page = LoginPage(browser)

    @autologger.automation_logger("Task")
    def login(self, email, password):
        self.login_page.enter_email(email) \
                       .enter_password(password) \
                       .click_submit()
```

**Key conventions:**
- `@autologger("Task")` on every method (not constructor)
- Composes Page Objects
- One domain operation per method
- Never return values — Tests assert through POM state-check methods

### Layer 4: Role

Roles represent user personas and orchestrate Tasks into business workflows.

```python
class UserRole:
    @autologger.automation_logger("Role Constructor")
    def __init__(self, browser):
        self.login_tasks = LoginTasks(browser)
        self.dashboard_tasks = DashboardTasks(browser)

    @autologger.automation_logger("Role")
    def login_and_navigate_to_settings(self, email, password):
        self.login_tasks.login(email, password)
        self.dashboard_tasks.open_settings()
```

**Key conventions:**
- `@autologger("Role")` on workflow methods
- `@autologger("Role Constructor")` on `__init__`
- Composes Task modules
- Workflow methods call multiple Tasks
- Never return values

### Layer 5: Test

Tests are thin — they orchestrate Roles and assert results.

```python
class TestUserLogin:
    @autologger.automation_logger("Test")
    def test_user_can_login(self):
        # Arrange
        email = self.test_data["email"]
        password = self.test_data["password"]

        # Act
        self.user_role.login_and_navigate_to_settings(email, password)

        # Assert — via POM state-check method
        assert self.login_page.is_logged_in()
```

**Key conventions:**
- `@autologger("Test")` decorator
- AAA pattern: Arrange / Act / Assert
- Orchestrate Roles to execute business workflows — multi-role workflows are supported
- Assert through Page Object state-check methods
- No direct Page Object calls — Roles handle orchestration

---

## Decorator Strategy

The `@autologger.automation_logger` decorator provides automatic logging for every method call:

| Layer | Decorator | On Constructor? |
|-------|-----------|-----------------|
| **POM** | None | No |
| **Task** | `@autologger("Task")` | No |
| **Role** | `@autologger("Role")` | Yes — `@autologger("Role Constructor")` |
| **Test** | `@autologger("Test")` | No |

---

## Data Flow

```
Test Data (JSON)
  ↓
Test (reads data, calls Role)
  ↓
Role (orchestrates Tasks)
  ↓
Task (calls POM methods)
  ↓
Page Object (calls BrowserInterface)
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

---

## Reference Implementations

Browse `framework/_reference/` for canonical code patterns:

| Layer | File |
|-------|------|
| **POM** | `pages/inquiry_form_page.py` |
| **Task** | `tasks/reference_tasks.py` |
| **Role** | `roles/reference_role.py` |
| **Test** | `tests/test_reference_workflow.py` |

These are the authoritative source. When in doubt, read the reference implementations.
