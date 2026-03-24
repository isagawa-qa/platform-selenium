"""
NavigationTasks - Task module

Orchestrates NavPage to navigate between PM Hub sections.
Handles loading the app and clicking sidebar navigation links.
"""

from interfaces.browser_interface import BrowserInterface
from pages.navigation.nav_page import NavPage
from resources.utilities import autologger


# Mapping of section names to sidebar locator methods and expected URL paths
SECTION_MAP = {
    "calendar":       ("click_calendar",       "/calendar"),
    "jira":           ("click_jira",           "/jira"),
    "jira_approvals": ("click_jira_approvals", "/jira/approvals"),
    "assistant":      ("click_assistant",      "/assistant"),
    "settings":       ("click_settings",       "/settings"),
}


class NavigationTasks:
    """
    Task module for sidebar navigation workflow.

    - @autologger("Task") on all methods
    - NO decorator on constructor
    - Composes NavPage
    - One domain operation per method
    - NO return values
    """

    def __init__(self, browser: BrowserInterface):
        """
        Compose NavPage — NO decorator on constructor.

        Args:
            browser: BrowserInterface instance
        """
        self.browser = browser
        self.nav_page = NavPage(browser)

    # ==================== TASK METHODS ====================

    @autologger.automation_logger("Task")
    def navigate_to_hub(self, base_url: str) -> None:
        """
        Navigate to PM Hub and wait for the sidebar to load.

        Args:
            base_url: Base URL of the PM Hub application
        """
        (self.nav_page
            .navigate(base_url)
            .wait_for_sidebar())

    @autologger.automation_logger("Task")
    def navigate_to_section(self, section: str) -> None:
        """
        Click the sidebar link for the given section and wait for URL change.

        Args:
            section: One of 'calendar', 'jira', 'jira_approvals', 'assistant', 'settings'

        Raises:
            ValueError: If section name is not recognized
        """
        if section not in SECTION_MAP:
            raise ValueError(
                f"Unknown section '{section}'. Valid sections: {list(SECTION_MAP.keys())}"
            )

        method_name, expected_path = SECTION_MAP[section]
        click_method = getattr(self.nav_page, method_name)
        (click_method()
            .wait_for_url(expected_path))
