"""
TestE2ECreateEmployeeAndAssignTask - Integration test for workforce management.

End-to-end test that validates the complete workflow: create an employee,
then assign a task to that employee. Uses two Roles (EmployeeManager + TaskManager)
because the output of Phase 1 (employee creation) is the input to Phase 2 (task assignment).

Uses AAA pattern: Arrange, Act, Assert.
"""

import pytest
from resources.utilities import autologger
from _reference.roles.employee_manager import EmployeeManager
from _reference.roles.task_manager import TaskManager
from _reference.pages.employees_page import EmployeesPage
from _reference.pages.tasks_page import TasksPage


class TestE2ECreateEmployeeAndAssignTask:
    """
    Integration test - workforce management end-to-end flow.

    - @autologger("Test") decorator
    - MULTIPLE Role workflow calls (integration test)
    - Assert via Page Object state-check methods from BOTH domains
    - Validates causal dependency: employee must exist before task assignment
    """

    @pytest.fixture(autouse=True)
    def setup(self, browser, config, test_users):
        """Pytest fixture wires browser, config, and test data into the test class."""
        self.browser = browser
        self.config = config
        self.test_users = test_users
        self.employees_page = EmployeesPage(self.browser)
        self.tasks_page = TasksPage(self.browser)

    # ==================== TEST METHODS ====================

    @pytest.mark.task_management
    @pytest.mark.employee_management
    @autologger.automation_logger("Test")
    def test_e2e_create_employee_and_assign_task(self):
        """
        Integration test: create employee then assign a task to them.

        AAA Pattern:
        1. Arrange - Create both roles with shared credentials, define test data
        2. Act - Call EmployeeManager.create_employee, then TaskManager.assign_task
        3. Assert - Verify employee exists AND task is assigned to that employee
        """
        # Arrange
        credentials = self.test_users["admin"]
        login_url = self.config["url"] + "/auth/login"

        employee_name = "Research Assistant"
        employee_description = "Analyzes market trends and competitor data"
        employee_capabilities = "data analysis, reporting, research"

        task_title = "Research competitor pricing"
        task_description = "Analyze competitor pricing strategies and create a summary report"

        employee_manager = EmployeeManager(
            self.browser,
            login_url=login_url,
            email=credentials["email"],
            password=credentials["password"]
        )

        task_manager = TaskManager(
            self.browser,
            login_url=login_url,
            email=credentials["email"],
            password=credentials["password"]
        )

        # Act — Phase 1: Create the employee
        employee_manager.create_employee(
            name=employee_name,
            description=employee_description,
            capabilities=employee_capabilities
        )

        # Assert — Phase 1: Employee created successfully
        assert self.employees_page.is_employee_created_toast_displayed(), \
            "Toast notification 'Employee created' should be displayed"

        assert self.employees_page.is_employee_displayed_in_list(employee_name), \
            f"Employee '{employee_name}' should be visible in the employees list"

        # Act — Phase 2: Assign task to the employee (already logged in from Phase 1)
        task_manager.assign_task_to_employee_continue(
            title=task_title,
            description=task_description,
            assignee_name=employee_name
        )

        # Assert — Phase 2: Task created and assigned
        assert self.tasks_page.is_task_created_toast_displayed(), \
            "Toast notification 'Task created' should be displayed"

        assert self.tasks_page.is_task_displayed_in_list(task_title), \
            f"Task '{task_title}' should be visible in the tasks list"

        assert self.tasks_page.is_task_assigned_to(employee_name), \
            f"Task should be assigned to '{employee_name}'"
