"""
TaskManagementTasks - Task module

Orchestrates page objects to accomplish task management workflows.
Handles task creation and assignment as domain operations.
"""

from interfaces.browser_interface import BrowserInterface
from _reference.pages.login_page import LoginPage
from _reference.pages.tasks_page import TasksPage
from resources.utilities import autologger


class TaskManagementTasks:
    """
    Task module for Task Management workflow.

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
        self.tasks_page = TasksPage(browser)

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
    def create_task_assigned_to(self, title: str, description: str, assignee_name: str) -> None:
        """
        Navigate to tasks page and create a task assigned to a specific employee.

        Args:
            title: Task title
            description: Task description
            assignee_name: Name of the employee to assign (partial match)
        """
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
