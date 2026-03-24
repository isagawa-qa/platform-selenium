"""
JiraPage - Page Object Model

Page Object for the PM Hub Jira Issues page (http://localhost:3000/jira).
Handles project filter, time filter, stat cards, and project expand/collapse.
"""

from selenium.webdriver.common.by import By
from interfaces.browser_interface import BrowserInterface


class JiraPage:
    """
    Page Object for PM Hub Jira Issues Page.

    - NO decorators
    - Locators as class constants
    - Atomic methods returning self
    - State-check methods for assertions
    """

    def __init__(self, browser: BrowserInterface):
        """Compose BrowserInterface — NO inheritance."""
        self.browser = browser

    # ==================== LOCATORS (Class Constants) ====================

    PAGE_HEADING     = (By.XPATH, "//h1[normalize-space(text())='Jira Issues'] | //h2[normalize-space(text())='Jira Issues']")
    PROJECT_FILTER   = (By.XPATH, "//select[@aria-label='Filter by project']")
    TIME_FILTER_ALL  = (By.XPATH, "//button[normalize-space(text())='All']")
    TIME_FILTER_7D   = (By.XPATH, "//button[normalize-space(text())='7d']")
    TIME_FILTER_30D  = (By.XPATH, "//button[normalize-space(text())='30d']")
    TIME_FILTER_90D  = (By.XPATH, "//button[normalize-space(text())='90d']")
    EXPAND_BUTTON    = (By.XPATH, "//button[contains(@aria-label,'Expand')]")
    COLLAPSE_BUTTON  = (By.XPATH, "//button[contains(@aria-label,'Collapse')]")

    # Stat card labels
    STAT_MY_ASSIGNED  = (By.XPATH, "//*[normalize-space(text())='My Assigned']")
    STAT_NEEDS_INPUT  = (By.XPATH, "//*[normalize-space(text())='Needs Input']")
    STAT_HIGH_PRIORITY = (By.XPATH, "//*[normalize-space(text())='High Priority']")
    STAT_STALE        = (By.XPATH, "//*[contains(normalize-space(text()),'Stale')]")

    # ==================== NAVIGATION ====================

    def wait_for_jira_page(self, timeout: int = 15) -> "JiraPage":
        """Wait for the Jira Issues page heading to be visible."""
        self.browser.wait_for_element_visible(*self.PAGE_HEADING, timeout=timeout)
        return self

    # ==================== ATOMIC METHODS (One UI Action) ====================

    def select_project_filter(self, project_name: str) -> "JiraPage":
        """
        Select a project from the Filter by project dropdown.

        Args:
            project_name: Visible text of the option, e.g. 'PRODUCT', 'All Projects'
        """
        self.browser.select_by_text(*self.PROJECT_FILTER, project_name)
        return self

    def click_time_filter(self, period: str) -> "JiraPage":
        """
        Click a time filter button.

        Args:
            period: One of 'All', '7d', '30d', '90d'
        """
        locator_map = {
            "All": self.TIME_FILTER_ALL,
            "7d":  self.TIME_FILTER_7D,
            "30d": self.TIME_FILTER_30D,
            "90d": self.TIME_FILTER_90D,
        }
        if period not in locator_map:
            raise ValueError(f"Unknown period '{period}'. Valid: {list(locator_map.keys())}")
        self.browser.click(*locator_map[period])
        return self

    def click_first_expand_button(self) -> "JiraPage":
        """Click the first available project expand button."""
        self.browser.click(*self.EXPAND_BUTTON)
        return self

    # ==================== STATE-CHECK METHODS (For Assertions) ====================

    def is_at_jira_page(self) -> bool:
        """Check if currently on the Jira Issues page."""
        return "/jira" in self.browser.get_current_url()

    def is_page_heading_visible(self) -> bool:
        """Check if the Jira Issues heading is visible."""
        return self.browser.is_element_displayed(*self.PAGE_HEADING, timeout=5)

    def is_project_filter_visible(self) -> bool:
        """Check if the project filter dropdown is visible."""
        return self.browser.is_element_displayed(*self.PROJECT_FILTER, timeout=5)

    def are_stat_cards_visible(self) -> bool:
        """Check if at least the 'My Assigned' stat card is visible."""
        return self.browser.is_element_displayed(*self.STAT_MY_ASSIGNED, timeout=5)

    def is_expand_button_visible(self) -> bool:
        """Check if at least one project expand button is present."""
        return self.browser.is_element_displayed(*self.EXPAND_BUTTON, timeout=5)

    def is_collapse_button_visible(self) -> bool:
        """Check if at least one project collapse button is visible (expanded state)."""
        return self.browser.is_element_displayed(*self.COLLAPSE_BUTTON, timeout=5)
