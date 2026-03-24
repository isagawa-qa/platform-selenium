"""
HubDashboardPage - Page Object Model

Page Object for the PM Hub dashboard (http://localhost:3000/).
Provides state-check methods for verifying priority update content.
"""

from selenium.webdriver.common.by import By
from interfaces.browser_interface import BrowserInterface


class HubDashboardPage:
    """
    Page Object for PM Hub Dashboard — priority update view.

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

    GREETING_HEADING    = (By.TAG_NAME, "h1")
    MORNING_BRIEF_CARD  = (By.CSS_SELECTOR, ".briefing-strip")
    BRIEF_SUMMARY_STATS = (By.CSS_SELECTOR, ".briefing-strip .briefing-strip-summary")

    # ==================== NAVIGATION ====================

    def navigate(self, url: str) -> "HubDashboardPage":
        """Navigate to the PM Hub dashboard URL."""
        self.browser.navigate_to(url)
        return self

    # ==================== ATOMIC METHODS ====================

    def wait_for_dashboard_loaded(self, timeout: int = 15) -> "HubDashboardPage":
        """Wait for the dashboard greeting heading to be visible."""
        self.browser.wait_for_element_visible(*self.GREETING_HEADING, timeout=timeout)
        return self

    def wait_for_morning_brief(self, timeout: int = 15) -> "HubDashboardPage":
        """Wait for the Morning Brief card to be visible."""
        self.browser.wait_for_element_visible(*self.MORNING_BRIEF_CARD, timeout=timeout)
        return self

    # ==================== STATE-CHECK METHODS (For Assertions) ====================

    def has_priority_items_visible(self) -> bool:
        """Check if the Morning Brief card (priority items) is displayed."""
        return self.browser.is_element_displayed(*self.MORNING_BRIEF_CARD, timeout=10)

    def has_morning_brief_visible(self) -> bool:
        """Check if the Morning Brief card is visible on the dashboard."""
        return self.browser.is_element_displayed(*self.MORNING_BRIEF_CARD, timeout=10)

    def has_item_title_and_status(self) -> bool:
        """Check if the brief summary stats (items/overdue/meetings) are visible."""
        return self.browser.is_element_displayed(*self.BRIEF_SUMMARY_STATS, timeout=10)

    def is_on_dashboard(self) -> bool:
        """Check if currently on the PM Hub dashboard (URL is root)."""
        url = self.browser.get_current_url()
        return url.rstrip("/").endswith(":3000") or url.endswith("/")

    def get_brief_summary_text(self) -> str:
        """Return the Morning Brief summary stats text (e.g. '35 items · 10 overdue')."""
        return self.browser.get_text(*self.BRIEF_SUMMARY_STATS)
