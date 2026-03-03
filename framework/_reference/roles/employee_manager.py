"""
EmployeeManager - Role module

Represents an employee manager persona who logs in and manages employees.
Orchestrates complete business workflows using Task modules.
"""

from interfaces.browser_interface import BrowserInterface
from resources.utilities import autologger
from _reference.tasks.employee_management_tasks import EmployeeManagementTasks


class EmployeeManager:
    """
    EmployeeManager role - orchestrates employee management workflows.

    - @autologger("Role") on workflow methods
    - @autologger("Role Constructor") on __init__
    - Composes Task modules
    - Workflow methods call MULTIPLE tasks
    - NO return values
    """

    @autologger.automation_logger("Role Constructor")
    def __init__(self, browser_interface: BrowserInterface, login_url: str, email: str, password: str):
        """
        Initialize and compose Task modules.

        Args:
            browser_interface: BrowserInterface instance
            login_url: URL for the login page
            email: User email for authentication
            password: User password for authentication
        """
        self.browser = browser_interface
        self.login_url = login_url
        self.email = email
        self.password = password
        self.employee_management_tasks = EmployeeManagementTasks(browser_interface)

    # ==================== WORKFLOW METHODS ====================

    @autologger.automation_logger("Role")
    def create_employee(self, name: str, description: str = "", capabilities: str = "") -> None:
        """
        Complete workflow: Login and create an employee.

        Orchestrates MULTIPLE task operations:
        1. Login with credentials
        2. Create employee with specified details
        """
        self.employee_management_tasks.login(self.login_url, self.email, self.password)
        self.employee_management_tasks.create_employee(name, description, capabilities)
