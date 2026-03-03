"""
TasksPage - Page Object Model

Page Object for the Tasks page. Handles navigation, opening Create Task modal,
filling the form, assigning to an employee, and verifying task creation.
"""

from selenium.webdriver.common.by import By
from interfaces.browser_interface import BrowserInterface


class TasksPage:
    """
    Page Object for Tasks Page.

    - NO decorators
    - Locators as class constants
    - Atomic methods (one UI action)
    - Return self for chaining
    - State-check methods for assertions
    """

    def __init__(self, browser: BrowserInterface):
        """Compose BrowserInterface — NO inheritance."""
        self.browser = browser

    # ==================== LOCATORS (Class Constants) ====================

    TASKS_NAV_LINK = (By.CSS_SELECTOR, "[data-testid='nav-tasks']")
    CREATE_TASK_BUTTON = (By.CSS_SELECTOR, "[data-testid='button-create-task']")
    TASK_TITLE_INPUT = (By.CSS_SELECTOR, "[data-testid='input-task-title']")
    TASK_DESCRIPTION_INPUT = (By.CSS_SELECTOR, "[data-testid='input-task-description']")
    TASK_ASSIGNEE_COMBOBOX = (By.CSS_SELECTOR, "[data-testid='select-task-assignee']")
    TASK_PRIORITY_COMBOBOX = (By.CSS_SELECTOR, "[data-testid='select-task-priority']")
    AUTO_RUN_CHECKBOX = (By.CSS_SELECTOR, "[data-testid='checkbox-auto-execute']")
    SUBMIT_TASK_BUTTON = (By.CSS_SELECTOR, "[data-testid='button-submit-task']")
    TASK_CREATED_TOAST = (By.XPATH, "//*[@role='status']//*[contains(., 'Task created')]")

    # ==================== NAVIGATION ====================

    def navigate_to_tasks(self) -> "TasksPage":
        """Click Tasks in the sidebar to navigate to tasks page."""
        self.browser.click(*self.TASKS_NAV_LINK)
        return self

    def wait_for_tasks_page(self, timeout: int = 10) -> "TasksPage":
        """Wait for tasks page to load."""
        self.browser.wait_for_element_visible(*self.CREATE_TASK_BUTTON, timeout=timeout)
        return self

    # ==================== ATOMIC METHODS (One UI Action) ====================

    def click_create_task(self) -> "TasksPage":
        """Click the Create Task button to open the modal."""
        self.browser.click(*self.CREATE_TASK_BUTTON)
        return self

    def wait_for_modal_visible(self, timeout: int = 10) -> "TasksPage":
        """Wait for Create Task modal to be visible."""
        self.browser.wait_for_element_visible(*self.TASK_TITLE_INPUT, timeout=timeout)
        return self

    def enter_task_title(self, title: str) -> "TasksPage":
        """Enter the task title."""
        self.browser.enter_text(*self.TASK_TITLE_INPUT, title)
        return self

    def enter_task_description(self, description: str) -> "TasksPage":
        """Enter the task description."""
        self.browser.enter_text(*self.TASK_DESCRIPTION_INPUT, description)
        return self

    def click_assignee_dropdown(self) -> "TasksPage":
        """Click the Assign to dropdown to open options."""
        self.browser.click(*self.TASK_ASSIGNEE_COMBOBOX)
        return self

    def select_assignee_by_name(self, name: str) -> "TasksPage":
        """Select an assignee from the dropdown by partial name match."""
        locator = (By.XPATH, f"//*[@role='option'][contains(., '{name}')]")
        self.browser.click(*locator)
        return self

    def click_priority_dropdown(self) -> "TasksPage":
        """Click the Priority dropdown to open options."""
        self.browser.click(*self.TASK_PRIORITY_COMBOBOX)
        return self

    def select_priority_by_name(self, priority: str) -> "TasksPage":
        """Select a priority from the dropdown by name (Low, Medium, High, Urgent)."""
        locator = (By.XPATH, f"//*[@role='option'][contains(., '{priority}')]")
        self.browser.click(*locator)
        return self

    def uncheck_auto_run(self) -> "TasksPage":
        """Uncheck the Auto-run checkbox (click to toggle off)."""
        self.browser.click(*self.AUTO_RUN_CHECKBOX)
        return self

    def click_submit_task(self) -> "TasksPage":
        """Click the Create Task submit button."""
        self.browser.click(*self.SUBMIT_TASK_BUTTON)
        return self

    def wait_for_task_created_toast(self, timeout: int = 10) -> "TasksPage":
        """Wait for the 'Task created' toast notification to appear."""
        self.browser.wait_for_element_visible(*self.TASK_CREATED_TOAST, timeout=timeout)
        return self

    # ==================== STATE-CHECK METHODS (For Assertions) ====================

    def is_task_created_toast_displayed(self) -> bool:
        """Check if the 'Task created' toast notification is displayed."""
        return self.browser.is_element_displayed(*self.TASK_CREATED_TOAST, timeout=5)

    def is_task_displayed_in_list(self, title: str) -> bool:
        """Check if a task with the given title is displayed in the list."""
        locator = (By.XPATH, f"//*[contains(., '{title}')]")
        return self.browser.is_element_displayed(*locator, timeout=5)

    def is_task_assigned_to(self, assignee_name: str) -> bool:
        """Check if a task is assigned to the given employee name."""
        locator = (By.XPATH, f"//*[contains(., '{assignee_name}')]")
        return self.browser.is_element_displayed(*locator, timeout=5)
