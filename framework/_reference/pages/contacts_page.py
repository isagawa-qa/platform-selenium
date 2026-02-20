"""
ContactsPage - Page Object Model

Page Object representing contacts step in the inquiry wizard.
Provides atomic UI interactions via BrowserInterface composition.
"""

from selenium.webdriver.common.by import By
from interfaces.browser_interface import BrowserInterface


class ContactsPage:
    """
    Page Object for Contacts Page (wizard step 3).

    - NO decorators
    - Locators as class constants
    - Atomic methods (one UI action)
    - Return self for chaining
    - State-check methods for assertions
    """

    def __init__(self, browser: BrowserInterface):
        """Compose BrowserInterface - NO inheritance."""
        self.browser = browser

    # ==================== LOCATORS (Class Constants) ====================
    NEXT_BUTTON = (By.CSS_SELECTOR, "[aria-label='contact_add_button_submit']")
    PREVIOUS_BUTTON = (By.CSS_SELECTOR, "[aria-label='contact_add button_previous']")
    CONTACT_TABLE = (By.CSS_SELECTOR, "[aria-label='contact_edit_title_contacts']")

    # ==================== ATOMIC METHODS (One UI Action) ====================

    def click_next(self) -> "ContactsPage":
        """Click next button."""
        self.browser.click(*self.NEXT_BUTTON)
        return self

    def click_previous(self) -> "ContactsPage":
        """Click previous button."""
        self.browser.click(*self.PREVIOUS_BUTTON)
        return self

    # ==================== STATE-CHECK METHODS (For Assertions) ====================

    def is_next_button_enabled(self) -> bool:
        """Check if next button is enabled."""
        return self.browser.is_element_clickable(*self.NEXT_BUTTON, timeout=2)

    def is_contacts_visible(self) -> bool:
        """Check if contacts table is visible."""
        return self.browser.is_element_displayed(*self.CONTACT_TABLE, timeout=2)
