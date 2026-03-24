"""
JiraTasks - Task module

Orchestrates JiraPage to navigate to the Jira Issues page and interact
with project filters, time filters, and project expand/collapse.
"""

from interfaces.browser_interface import BrowserInterface
from pages.navigation.nav_page import NavPage
from pages.jira.jira_page import JiraPage
from resources.utilities import autologger


class JiraTasks:
    """
    Task module for Jira Issues workflow.

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
        self.nav_page = NavPage(browser)
        self.jira_page = JiraPage(browser)

    # ==================== TASK METHODS ====================

    @autologger.automation_logger("Task")
    def navigate_to_jira(self, base_url: str) -> None:
        """
        Navigate to PM Hub, click the Jira sidebar link, and wait for the page.

        Args:
            base_url: Base URL of the PM Hub application
        """
        (self.nav_page
            .navigate(base_url)
            .wait_for_sidebar()
            .click_jira()
            .wait_for_url("/jira"))
        (self.jira_page
            .wait_for_jira_page())

    @autologger.automation_logger("Task")
    def filter_by_project(self, project_name: str) -> None:
        """
        Select a project from the project filter dropdown.

        Args:
            project_name: Visible option text, e.g. 'PRODUCT', 'All Projects'
        """
        (self.jira_page
            .select_project_filter(project_name))

    @autologger.automation_logger("Task")
    def filter_by_time(self, period: str) -> None:
        """
        Click a time filter button to scope issues by recency.

        Args:
            period: One of 'All', '7d', '30d', '90d'
        """
        (self.jira_page
            .click_time_filter(period))

    @autologger.automation_logger("Task")
    def expand_first_project(self) -> None:
        """Click the first available project expand button to reveal its issues."""
        (self.jira_page
            .click_first_expand_button())
