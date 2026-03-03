"""
EmployeeManagementTasks - Task module

Orchestrates page objects to accomplish employee management workflows.
Handles login and employee creation as domain operations.
"""

from interfaces.browser_interface import BrowserInterface
from _reference.pages.login_page import LoginPage
from _reference.pages.employees_page import EmployeesPage
from resources.utilities import autologger


class EmployeeManagementTasks:
    """
    Task module for Employee Management workflow.

    - @autologger("Task") on all methods
    - NO decorator on constructor
    - Composes Page Objects
    - One domain operation per method
    - NO return values
    """

    def __init__(self, browser: BrowserInterface):
        """
        Compose Page Objects — NO decorator on constructor.

        Args:
            browser: BrowserInterface instance
        """
        self.browser = browser
        self.login_page = LoginPage(browser)
        self.employees_page = EmployeesPage(browser)

    # ==================== TASK METHODS ====================

    @autologger.automation_logger("Task")
    def login(self, login_url: str, email: str, password: str) -> None:
        """
        Login with provided credentials.

        Args:
            login_url: URL of the login page
            email: User email address
            password: User password
        """
        (self.login_page
            .navigate(login_url)
            .wait_for_login_button_visible()
            .click_log_in()
            .wait_for_email_visible()
            .enter_email(email)
            .enter_password(password)
            .click_sign_in())

    @autologger.automation_logger("Task")
    def create_employee(self, name: str, description: str = "", capabilities: str = "") -> None:
        """
        Navigate to employees page and create a new employee.

        Args:
            name: Employee name
            description: Employee description (optional)
            capabilities: Employee capabilities comma-separated (optional)
        """
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
