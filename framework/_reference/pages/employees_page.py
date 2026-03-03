"""
EmployeesPage - Page Object Model

Page Object for the Employees page. Handles navigation, opening
Create Employee modal, filling the form, and verifying employee creation.
"""

from selenium.webdriver.common.by import By
from interfaces.browser_interface import BrowserInterface


class EmployeesPage:
    """
    Page Object for Employees Page.

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

    EMPLOYEES_NAV_LINK = (By.CSS_SELECTOR, "[data-testid='nav-employees']")
    CREATE_EMPLOYEE_BUTTON = (By.CSS_SELECTOR, "[data-testid='button-create-employee']")
    EMPLOYEE_NAME_INPUT = (By.CSS_SELECTOR, "[data-testid='input-agent-name']")
    EMPLOYEE_ROLE_COMBOBOX = (By.CSS_SELECTOR, "[data-testid='select-agent-role']")
    ANALYST_ROLE_OPTION = (By.XPATH, "//*[@role='option'][contains(., 'Analyst')]")
    EMPLOYEE_DESCRIPTION_INPUT = (By.CSS_SELECTOR, "[data-testid='input-agent-description']")
    EMPLOYEE_CAPABILITIES_INPUT = (By.CSS_SELECTOR, "[data-testid='input-agent-capabilities']")
    SUBMIT_CREATE_BUTTON = (By.CSS_SELECTOR, "[data-testid='button-submit-create']")
    EMPLOYEE_CREATED_TOAST = (By.XPATH, "//*[@role='status']//*[contains(., 'Employee created')]")

    # ==================== NAVIGATION ====================

    def navigate_to_employees(self) -> "EmployeesPage":
        """Click Employees in the sidebar to navigate to employees page."""
        self.browser.click(*self.EMPLOYEES_NAV_LINK)
        return self

    def wait_for_employees_page(self, timeout: int = 10) -> "EmployeesPage":
        """Wait for employees page to load."""
        self.browser.wait_for_element_visible(*self.CREATE_EMPLOYEE_BUTTON, timeout=timeout)
        return self

    # ==================== ATOMIC METHODS (One UI Action) ====================

    def click_create_employee(self) -> "EmployeesPage":
        """Click the Create Employee button to open the modal."""
        self.browser.click(*self.CREATE_EMPLOYEE_BUTTON)
        return self

    def wait_for_modal_visible(self, timeout: int = 10) -> "EmployeesPage":
        """Wait for Create Employee modal to be visible."""
        self.browser.wait_for_element_visible(*self.EMPLOYEE_NAME_INPUT, timeout=timeout)
        return self

    def enter_employee_name(self, name: str) -> "EmployeesPage":
        """Enter the employee name."""
        self.browser.enter_text(*self.EMPLOYEE_NAME_INPUT, name)
        return self

    def click_role_dropdown(self) -> "EmployeesPage":
        """Click the Role dropdown to open options."""
        self.browser.click(*self.EMPLOYEE_ROLE_COMBOBOX)
        return self

    def select_analyst_role(self) -> "EmployeesPage":
        """Select Analyst from the Role dropdown."""
        self.browser.click(*self.ANALYST_ROLE_OPTION)
        return self

    def enter_employee_description(self, description: str) -> "EmployeesPage":
        """Enter the employee description."""
        self.browser.enter_text(*self.EMPLOYEE_DESCRIPTION_INPUT, description)
        return self

    def enter_employee_capabilities(self, capabilities: str) -> "EmployeesPage":
        """Enter the employee capabilities (comma-separated)."""
        self.browser.enter_text(*self.EMPLOYEE_CAPABILITIES_INPUT, capabilities)
        return self

    def click_submit_create(self) -> "EmployeesPage":
        """Click the Create Employee submit button."""
        self.browser.click(*self.SUBMIT_CREATE_BUTTON)
        return self

    def wait_for_employee_created_toast(self, timeout: int = 10) -> "EmployeesPage":
        """Wait for the 'Employee created' toast notification to appear."""
        self.browser.wait_for_element_visible(*self.EMPLOYEE_CREATED_TOAST, timeout=timeout)
        return self

    # ==================== STATE-CHECK METHODS (For Assertions) ====================

    def is_employee_created_toast_displayed(self) -> bool:
        """Check if the 'Employee created' toast notification is displayed."""
        return self.browser.is_element_displayed(*self.EMPLOYEE_CREATED_TOAST, timeout=5)

    def is_employee_displayed_in_list(self, name: str) -> bool:
        """Check if an employee with the given name is displayed in the list."""
        locator = (By.XPATH, f"//*[contains(., '{name}')]")
        return self.browser.is_element_displayed(*locator, timeout=5)

    def is_employee_idle(self, name: str) -> bool:
        """Check if an employee with the given name has 'Idle' status."""
        locator = (By.XPATH, f"//*[contains(., '{name}')]/../..//*[contains(., 'Idle')]")
        return self.browser.is_element_displayed(*locator, timeout=5)
