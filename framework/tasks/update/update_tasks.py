"""
UpdateTasks - Task module

Orchestrates Page Objects to accomplish the PM Hub priority update workflow.
Handles navigation to the dashboard and waiting for priority items to load.
"""

from interfaces.browser_interface import BrowserInterface
from pages.update.hub_dashboard_page import HubDashboardPage
from resources.utilities import autologger


class UpdateTasks:
    """
    Task module for the priority update workflow.

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
        self.hub_dashboard_page = HubDashboardPage(browser)

    # ==================== TASK METHODS ====================

    @autologger.automation_logger("Task")
    def navigate_to_dashboard(self, base_url: str) -> None:
        """
        Navigate to the PM Hub dashboard and wait for it to load.

        Args:
            base_url: Base URL of the PM Hub application
        """
        (self.hub_dashboard_page
            .navigate(base_url)
            .wait_for_dashboard_loaded())

    @autologger.automation_logger("Task")
    def wait_for_priority_items(self) -> None:
        """
        Wait for the Morning Brief card (priority items) to be visible.
        """
        self.hub_dashboard_page.wait_for_morning_brief()
