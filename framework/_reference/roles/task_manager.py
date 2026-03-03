"""
TaskManager - Role module

Represents a task manager persona who logs in and manages tasks.
Orchestrates complete business workflows using Task modules.
"""

from interfaces.browser_interface import BrowserInterface
from resources.utilities import autologger
from _reference.tasks.task_management_tasks import TaskManagementTasks


class TaskManager:
    """
    TaskManager role - orchestrates task management workflows.

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
        self.task_management_tasks = TaskManagementTasks(browser_interface)

    # ==================== WORKFLOW METHODS ====================

    @autologger.automation_logger("Role")
    def assign_task_to_employee(self, title: str, description: str, assignee_name: str) -> None:
        """
        Complete workflow: Login and create a task assigned to an employee.

        Orchestrates MULTIPLE task operations:
        1. Login with credentials
        2. Create task assigned to specified employee
        """
        self.task_management_tasks.login(self.login_url, self.email, self.password)
        self.task_management_tasks.create_task_assigned_to(title, description, assignee_name)

    @autologger.automation_logger("Role")
    def assign_task_to_employee_continue(self, title: str, description: str, assignee_name: str) -> None:
        """
        Continue workflow: Create a task assigned to an employee (already logged in).

        For integration tests where login was already performed by a prior Role.
        Skips login, goes directly to task creation.
        """
        self.task_management_tasks.create_task_assigned_to(title, description, assignee_name)
