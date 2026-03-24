"""
HubPage - Page Object Model

Page Object for the PM Hub dashboard (http://localhost:3000/).
Handles navigation to the PM Assistant (Tiffany) from the sidebar.
"""

from selenium.webdriver.common.by import By
from interfaces.browser_interface import BrowserInterface


class HubPage:
    """
    Page Object for PM Hub Dashboard.

    - NO decorators
    - Locators as class constants
    - Atomic methods (one UI action)
    - Return self for chaining
    - State-check methods for assertions
    """

    def __init__(self, browser: BrowserInterface):
        """Compose BrowserInterface — NO inheritance."""
        self.browser = browser

    # ==================== LOCATORS (Class Constants) ====================

    SIDEBAR_ASSISTANT_LINK = (By.CSS_SELECTOR, "a[href='/assistant']")

    # ==================== NAVIGATION ====================

    def navigate(self, url: str) -> "HubPage":
        """Navigate to the PM Hub base URL."""
        self.browser.navigate_to(url)
        return self

    def wait_for_hub_loaded(self, timeout: int = 15) -> "HubPage":
        """Wait for the PM Hub sidebar to be visible."""
        self.browser.wait_for_element_visible(*self.SIDEBAR_ASSISTANT_LINK, timeout=timeout)
        return self

    # ==================== ATOMIC METHODS (One UI Action) ====================

    def click_pm_assistant(self) -> "HubPage":
        """Click the PM Assistant link in the sidebar to navigate to Tiffany."""
        self.browser.click(*self.SIDEBAR_ASSISTANT_LINK)
        return self

    # ==================== STATE-CHECK METHODS (For Assertions) ====================

    def is_hub_loaded(self) -> bool:
        """Check if PM Hub dashboard has loaded (sidebar assistant link visible)."""
        return self.browser.is_element_displayed(*self.SIDEBAR_ASSISTANT_LINK, timeout=10)
