"""
NavPage - Page Object Model

Page Object for PM Hub sidebar navigation (accessible from all pages).
Handles navigation between major sections via sidebar links and URL verification.
"""

from selenium.webdriver.common.by import By
from interfaces.browser_interface import BrowserInterface


class NavPage:
    """
    Page Object for PM Hub sidebar navigation.

    - NO decorators
    - Locators as class constants
    - Atomic methods returning self
    - State-check methods for assertions
    """

    def __init__(self, browser: BrowserInterface):
        """Compose BrowserInterface — NO inheritance."""
        self.browser = browser

    # ==================== LOCATORS (Class Constants) ====================

    NAV_CALENDAR       = (By.CSS_SELECTOR, "a[href='/calendar']")
    NAV_JIRA           = (By.CSS_SELECTOR, "a[href='/jira']")
    NAV_JIRA_APPROVALS = (By.CSS_SELECTOR, "a[href='/jira/approvals']")
    NAV_ASSISTANT      = (By.CSS_SELECTOR, "a[href='/assistant']")
    NAV_SETTINGS       = (By.CSS_SELECTOR, "a[href='/settings']")

    # Used to confirm sidebar is loaded before navigating
    SIDEBAR_ANY_LINK   = (By.CSS_SELECTOR, "a[href='/assistant']")

    # ==================== NAVIGATION ====================

    def navigate(self, url: str) -> "NavPage":
        """Navigate to the given URL."""
        self.browser.navigate_to(url)
        return self

    def wait_for_sidebar(self, timeout: int = 15) -> "NavPage":
        """Wait for the sidebar to be visible (confirms page loaded)."""
        self.browser.wait_for_element_visible(*self.SIDEBAR_ANY_LINK, timeout=timeout)
        return self

    # ==================== ATOMIC METHODS (One UI Action) ====================

    def click_calendar(self) -> "NavPage":
        """Click the Calendar link in the sidebar."""
        self.browser.click(*self.NAV_CALENDAR)
        return self

    def click_jira(self) -> "NavPage":
        """Click the Jira link in the sidebar."""
        self.browser.click(*self.NAV_JIRA)
        return self

    def click_jira_approvals(self) -> "NavPage":
        """Click the Jira Approvals link in the sidebar."""
        self.browser.click(*self.NAV_JIRA_APPROVALS)
        return self

    def click_assistant(self) -> "NavPage":
        """Click the PM Assistant link in the sidebar."""
        self.browser.click(*self.NAV_ASSISTANT)
        return self

    def click_settings(self) -> "NavPage":
        """Click the Settings link in the sidebar."""
        self.browser.click(*self.NAV_SETTINGS)
        return self

    def wait_for_url(self, path: str, timeout: int = 10) -> "NavPage":
        """Wait for the URL to contain the given path fragment."""
        self.browser.wait_for_url_contains(path, timeout=timeout)
        return self

    # ==================== STATE-CHECK METHODS (For Assertions) ====================

    def is_at_url(self, path: str) -> bool:
        """Check if the current URL contains the given path fragment."""
        return path in self.browser.get_current_url()

    def is_sidebar_nav_visible(self) -> bool:
        """Check if sidebar navigation links are visible."""
        return self.browser.is_element_displayed(*self.SIDEBAR_ANY_LINK, timeout=5)
