# Architecture

## 5-Layer Pattern

The Isagawa QA Platform enforces a strict 5-layer test architecture. Each layer has exactly one responsibility, and layers communicate only with their immediate neighbors.

### Layer 1: WebInterface (BrowserInterface)

The foundation. This is the **only** layer that touches Selenium directly.

`framework/interfaces/browser_interface.py` wraps `WebDriver` with:
- Automatic `WebDriverWait` on every element lookup (configurable timeout, default 20s)
- Automatic screenshot capture on failure
- Structured logging at every operation
- Methods organized by concern: Navigation, Element Finding, Interactions, Waits, Screenshots, JavaScript, Window/Frame

No other layer imports Selenium locator strategies or WebDriver classes.

### Layer 2: Page Object Model (POM)

Each page class represents one page or component. It composes a `BrowserInterface` instance.

**Conventions:**
- **No decorators** on any method
- Locators as **class-level tuples**: `SUBMIT_BTN = (By.CSS_SELECTOR, "#submit")`
- Methods are **atomic** — one UI interaction each
- Methods **return `self`** for fluent chaining: `.fill_name("John").fill_email("j@test.com").click_submit()`
- **State-check methods** return `bool` for assertions: `is_form_submitted()`

Locator tuples are unpacked with splat: `self.browser.click(*self.SUBMIT_BTN)`

### Layer 3: Tasks

Tasks compose multiple Page Objects to accomplish one domain operation.

**Conventions:**
- `@autologger.automation_logger("Task")` on every method except `__init__`
- Constructor instantiates all needed Page Objects
- One domain operation per method (e.g., "create customer", "submit inquiry")
- **No return values** — tests assert via POM state-check methods
- Uses fluent POM API internally

### Layer 4: Roles

Roles represent user personas (Admin, Customer, Guest) and orchestrate multiple Tasks into business workflows.

**Conventions:**
- `@autologger.automation_logger("Role Constructor")` on `__init__`
- `@autologger.automation_logger("Role")` on all workflow methods
- Composes Task modules (never Page Objects directly)
- No locators, no direct browser calls
- No return values

### Layer 5: Tests

Tests use the AAA pattern (Arrange, Act, Assert) and are intentionally thin.

**Conventions:**
- `@autologger.automation_logger("Test")` decorator
- **Arrange:** Create Role, generate test data with Faker
- **Act:** Call Role workflow methods to execute business workflows — multi-role tests are supported for workflows that span multiple personas
- **Assert:** Use POM state-check methods

Tests delegate workflow orchestration to Roles. They only use POMs directly for assertions.

### Decorator Strategy

| Layer | Method Decorator | `__init__` Decorator |
|-------|-----------------|---------------------|
| POM | None | None |
| Task | `@automation_logger("Task")` | None |
| Role | `@automation_logger("Role")` | `@automation_logger("Role Constructor")` |
| Test | `@automation_logger("Test")` | N/A (pytest fixtures) |

### Data Flow

```
Test (Arrange / Act / Assert)
  └─→ Role (multi-task workflow, user persona)
       └─→ Task (single domain operation)
            └─→ Page Object (one page, atomic actions, fluent API)
                 └─→ BrowserInterface (Selenium wrapper)
                      └─→ WebDriver (Chrome/Brave)
```

Assertions flow in the opposite direction: Tests assert by calling POM state-check methods directly, bypassing Task and Role layers. This is why Tasks and Roles never return values — the assertion path is separate from the action path.

---

## 28 Design Decisions

The architecture is built on a set of design decisions documented across the reference implementations in `framework/_reference/`. Key decisions include:

1. **Composition over inheritance** — no class extends another
2. **Locators only in POMs** — Tasks, Roles, Tests never reference elements
3. **No return values from Tasks/Roles** — forces assertion through POMs
4. **Fluent POM API** — `return self` enables method chaining
5. **Autologger on all non-POM layers** — structured, layer-aware logging
6. **State-check methods for assertions** — `is_*()` methods return `bool`
7. **One Role call per test** — no orchestration in test files
8. **AAA pattern** — every test is Arrange, Act, Assert
9. **Faker for test data** — unique data per run, no shared state
10. **Splat operator for locators** — `self.browser.click(*self.LOCATOR)`
11. **Explicit waits everywhere** — no implicit waits, no `time.sleep()`
12. **Screenshots on failure** — automatic via BrowserInterface
13. **Environment config as JSON** — external, not hardcoded
14. **Credential strategy pattern** — flexible auth handling
15. **Read-before-write enforcement** — AI reads reference files before generating
16. **Single responsibility per file** — one class, one concern
17. **No circular dependencies** — strict layer hierarchy
18. **No business logic in tests** — delegation to Roles
19. **Atomic POM methods** — one UI action per method
20. **Multi-page Task methods** — Tasks can span pages, POMs cannot
21. **Session-scoped fixtures** — config and test data loaded once
22. **Function-scoped driver** — clean browser per test
23. **Custom CLI options** — `--env`, `--headless` for flexibility
24. **Dynamic marker registration** — AST-scanned from test files
25. **HTML report customization** — built into conftest
26. **Cross-platform driver management** — WebDriver Manager handles installs
27. **Anti-detection flags** — Chrome configured for automation compatibility
28. **Structured logging** — layer-prefixed log entries with timing

See `framework/_reference/README.md` for the canonical code patterns.
