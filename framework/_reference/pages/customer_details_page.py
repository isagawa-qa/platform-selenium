"""
CustomerDetailsPage - Page Object Model

Page Object representing customer details step in the inquiry wizard.
Provides atomic UI interactions via BrowserInterface composition.
"""

from selenium.webdriver.common.by import By
from interfaces.browser_interface import BrowserInterface


class CustomerDetailsPage:
    """
    Page Object for Customer Details Page (wizard step 2).

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
    NEXT_BUTTON = (By.CSS_SELECTOR, "[aria-label='customer_add_button_submit']")
    PREVIOUS_BUTTON = (By.CSS_SELECTOR, "[aria-label='customer_add button_previous']")
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, "[aria-label='customer_add_input_firstname']")
    LAST_NAME_INPUT = (By.CSS_SELECTOR, "[aria-label='customer_add_input_lastname']")

    # ==================== ATOMIC METHODS (One UI Action) ====================

    def click_next(self) -> "CustomerDetailsPage":
        """Click next button."""
        self.browser.click(*self.NEXT_BUTTON)
        return self

    def click_previous(self) -> "CustomerDetailsPage":
        """Click previous button."""
        self.browser.click(*self.PREVIOUS_BUTTON)
        return self

    # ==================== STATE-CHECK METHODS (For Assertions) ====================

    def is_next_button_enabled(self) -> bool:
        """Check if next button is enabled."""
        return self.browser.is_element_clickable(*self.NEXT_BUTTON, timeout=2)

    def is_form_visible(self) -> bool:
        """Check if customer details form is visible."""
        return self.browser.is_element_displayed(*self.FIRST_NAME_INPUT, timeout=2)
