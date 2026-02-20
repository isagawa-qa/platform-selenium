"""
CustomerSearchPage - Page Object Model

Page Object representing a single page in the application.
Provides atomic UI interactions via BrowserInterface composition.
"""

from selenium.webdriver.common.by import By
from interfaces.browser_interface import BrowserInterface


class CustomerSearchPage:
    """
    Page Object for Customer Search Page.

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
    NEW_INQUIRY_BUTTON = (By.CSS_SELECTOR, "[aria-label='inquiry_view_button_add']")
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, "[aria-label='customer_search_input_firstname']")
    LAST_NAME_INPUT = (By.CSS_SELECTOR, "[aria-label='customer_search_input_lastname']")
    CONTACT_TYPE_DROPDOWN = (By.CSS_SELECTOR, "[aria-label='contact_search_input_type']")
    CONTACT_IDENTIFIER_INPUT = (By.CSS_SELECTOR, "[aria-label='contact_search_input_identifier']")
    NEXT_BUTTON = (By.CSS_SELECTOR, "[aria-label='customer_search_button_next']")
    CANCEL_BUTTON = (By.CSS_SELECTOR, "[aria-label='customer_search button_cancel']")

    # ==================== NAVIGATION ====================

    def navigate(self) -> "CustomerSearchPage":
        """Navigate to inquiries page."""
        self.browser.navigate_to(self.browser.config['url'] + '/Portal/Inquiries')
        return self

    # ==================== ATOMIC METHODS (One UI Action) ====================

    def click_new_inquiry(self) -> "CustomerSearchPage":
        """Click new inquiry button to open wizard."""
        self.browser.click(*self.NEW_INQUIRY_BUTTON)
        return self

    def wait_for_form_visible(self, timeout: int = 10) -> "CustomerSearchPage":
        """Wait for customer search form to be visible."""
        self.browser.wait_for_element_visible(*self.FIRST_NAME_INPUT, timeout=timeout)
        return self

    def enter_first_name(self, text: str) -> "CustomerSearchPage":
        """Enter text into first name input."""
        self.browser.enter_text(*self.FIRST_NAME_INPUT, text)
        return self

    def enter_last_name(self, text: str) -> "CustomerSearchPage":
        """Enter text into last name input."""
        self.browser.enter_text(*self.LAST_NAME_INPUT, text)
        return self

    def select_contact_type(self, value: str) -> "CustomerSearchPage":
        """Select option from contact type dropdown."""
        self.browser.select_dropdown_by_visible_text(*self.CONTACT_TYPE_DROPDOWN, value)
        return self

    def enter_contact_identifier(self, text: str) -> "CustomerSearchPage":
        """Enter text into contact identifier input."""
        self.browser.enter_text(*self.CONTACT_IDENTIFIER_INPUT, text)
        return self

    def click_next(self) -> "CustomerSearchPage":
        """Click next button."""
        self.browser.click(*self.NEXT_BUTTON)
        return self

    def click_cancel(self) -> "CustomerSearchPage":
        """Click cancel button."""
        self.browser.click(*self.CANCEL_BUTTON)
        return self

    # ==================== STATE-CHECK METHODS (For Assertions) ====================

    def is_next_button_enabled(self) -> bool:
        """Check if next button is enabled."""
        return self.browser.is_element_clickable(*self.NEXT_BUTTON, timeout=2)

    def is_form_valid(self) -> bool:
        """Check if form is valid (next button clickable)."""
        return self.browser.is_element_displayed(*self.NEXT_BUTTON, timeout=2)
