"""
ProductManagerRole - Role module (common)

Represents a Product Manager persona on PM Hub.
Orchestrates complete business workflows using Task modules.

Workflows:
  - query_tiffany_for_priorities  (pm_assistant workflow)
  - get_priority_update            (update workflow)
"""

from interfaces.browser_interface import BrowserInterface
from resources.utilities import autologger
from tasks.pm_assistant.pm_assistant_tasks import PmAssistantTasks
from tasks.update.update_tasks import UpdateTasks
from tasks.navigation.navigation_tasks import NavigationTasks
from tasks.jira.jira_tasks import JiraTasks


class ProductManagerRole:
    """
    ProductManagerRole - orchestrates all PM Hub workflows.

    - @autologger("Role") on workflow methods
    - @autologger("Role Constructor") on __init__
    - Composes Task modules
    - Workflow methods call MULTIPLE tasks
    - NO return values
    """

    @autologger.automation_logger("Role Constructor")
    def __init__(self, browser_interface: BrowserInterface, base_url: str):
        """
        Initialize and compose Task modules.

        Args:
            browser_interface: BrowserInterface instance
            base_url: Base URL of the PM Hub application
        """
        self.browser = browser_interface
        self.base_url = base_url
        self.pm_assistant_tasks = PmAssistantTasks(browser_interface)
        self.update_tasks = UpdateTasks(browser_interface)
        self.navigation_tasks = NavigationTasks(browser_interface)
        self.jira_tasks = JiraTasks(browser_interface)

    # ==================== WORKFLOW METHODS ====================

    @autologger.automation_logger("Role")
    def query_tiffany_for_priorities(self, question: str) -> None:
        """
        Complete workflow: Navigate to PM Hub, open Tiffany, and ask about priorities.

        Orchestrates MULTIPLE task operations:
        1. Navigate to PM Hub dashboard
        2. Open the Tiffany PM Assistant
        3. Ask Tiffany the priorities question and wait for response

        Args:
            question: The question to ask Tiffany about current priorities
        """
        self.pm_assistant_tasks.navigate_to_pm_hub(self.base_url)
        self.pm_assistant_tasks.open_tiffany_assistant()
        self.pm_assistant_tasks.ask_tiffany_about_priorities(question)

    @autologger.automation_logger("Role")
    def get_priority_update(self) -> None:
        """
        Complete workflow: Navigate to the PM Hub dashboard and read priority update.

        Orchestrates task operations:
        1. Navigate to PM Hub dashboard
        2. Wait for priority items to load
        """
        self.update_tasks.navigate_to_dashboard(self.base_url)
        self.update_tasks.wait_for_priority_items()

    @autologger.automation_logger("Role")
    def navigate_to_section(self, section: str) -> None:
        """
        Complete workflow: Navigate to PM Hub and click the given sidebar section.

        Orchestrates task operations:
        1. Navigate to PM Hub and wait for sidebar
        2. Click the section link and wait for URL change

        Args:
            section: One of 'calendar', 'jira', 'jira_approvals', 'assistant', 'settings'
        """
        self.navigation_tasks.navigate_to_hub(self.base_url)
        self.navigation_tasks.navigate_to_section(section)

    @autologger.automation_logger("Role")
    def view_jira_issues(self, project_filter: str = None, time_filter: str = None) -> None:
        """
        Complete workflow: Navigate to the Jira Issues page and optionally apply filters.

        Orchestrates task operations:
        1. Navigate to Jira Issues page
        2. Apply project filter if provided
        3. Apply time filter if provided

        Args:
            project_filter: Optional project name to filter by, e.g. 'PRODUCT'
            time_filter: Optional time period, e.g. '7d', '30d', '90d', 'All'
        """
        self.jira_tasks.navigate_to_jira(self.base_url)
        if project_filter:
            self.jira_tasks.filter_by_project(project_filter)
        if time_filter:
            self.jira_tasks.filter_by_time(time_filter)

    @autologger.automation_logger("Role")
    def expand_jira_project(self) -> None:
        """
        Complete workflow: Navigate to Jira Issues and expand the first project.

        Orchestrates task operations:
        1. Navigate to Jira Issues page
        2. Click the first available project expand button
        """
        self.jira_tasks.navigate_to_jira(self.base_url)
        self.jira_tasks.expand_first_project()

    @autologger.automation_logger("Role")
    def click_pm_assistant_quick_action(self, action_name: str) -> None:
        """
        Complete workflow: Navigate to PM Assistant and click a quick-action button.

        Orchestrates task operations:
        1. Navigate to PM Hub
        2. Open the PM Assistant (Tiffany)
        3. Click the quick-action button and wait for response

        Args:
            action_name: One of 'My blockers', 'Pipeline', "Today's schedule",
                         'Slack activity', 'Search Jira'
        """
        self.pm_assistant_tasks.navigate_to_pm_hub(self.base_url)
        self.pm_assistant_tasks.open_tiffany_assistant()
        self.pm_assistant_tasks.click_quick_action(action_name)
