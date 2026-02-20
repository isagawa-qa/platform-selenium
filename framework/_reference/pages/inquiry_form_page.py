"""
InquiryFormPage - Page Object Model

Page Object representing a single page in the application.
Provides atomic UI interactions via BrowserInterface composition.
"""

from selenium.webdriver.common.by import By
from interfaces.browser_interface import BrowserInterface


class InquiryFormPage:
    """
    Page Object for Inquiry Form Page.

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
    TYPE_DROPDOWN = (By.CSS_SELECTOR, "[aria-label='inquiry_add_value_type']")
    SOURCE_DROPDOWN = (By.CSS_SELECTOR, "[aria-label='inquiry_add_value_source']")
    VEHICLE_NOTES_INPUT = (By.CSS_SELECTOR, "[aria-label='inquiry_add_value_desiredvehicle']")
    ASSIGNED_USER_DROPDOWN = (By.CSS_SELECTOR, "[aria-label='inquiry_add_value_assigneduserid']")
    STATUS_DROPDOWN = (By.CSS_SELECTOR, "[aria-label='inquiry_add_value_status']")
    COMPLETE_BUTTON = (By.CSS_SELECTOR, "[aria-label='inquiry_add_button_submit']")
    PREVIOUS_BUTTON = (By.CSS_SELECTOR, "[aria-label='inquiry_add button_previous']")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "[aria-label='alert_message_validation']")
    CUSTOMER_NAME_DISPLAY = (By.CSS_SELECTOR, "[aria-label='inquiry_view_value_customername']")
    TYPE_DISPLAY = (By.CSS_SELECTOR, "[aria-label='inquiry_view_value_type']")
    SOURCE_DISPLAY = (By.CSS_SELECTOR, "[aria-label='inquiry_view_value_source']")
    STATUS_DISPLAY = (By.CSS_SELECTOR, "[aria-label='inquiry_view_value_status']")

    # ==================== NAVIGATION ====================

    def navigate(self) -> "InquiryFormPage":
        """Navigate to inquiries page."""
        self.browser.navigate_to(self.browser.config['url'] + '/Portal/Inquiries')
        return self

    # ==================== ATOMIC METHODS (One UI Action) ====================

    def wait_for_form_visible(self, timeout: int = 10) -> "InquiryFormPage":
        """Wait for inquiry form to be visible."""
        self.browser.wait_for_element_visible(*self.TYPE_DROPDOWN, timeout=timeout)
        return self

    def select_type(self, value: str) -> "InquiryFormPage":
        """Select inquiry type."""
        self.browser.select_by_text(*self.TYPE_DROPDOWN, value)
        return self

    def select_source(self, value: str) -> "InquiryFormPage":
        """Select inquiry source."""
        self.browser.select_by_text(*self.SOURCE_DROPDOWN, value)
        return self

    def enter_vehicle_notes(self, text: str) -> "InquiryFormPage":
        """Enter vehicle notes."""
        self.browser.type(*self.VEHICLE_NOTES_INPUT, text)
        return self

    def select_assigned_user(self, value: str) -> "InquiryFormPage":
        """Select assigned user."""
        self.browser.select_by_text(*self.ASSIGNED_USER_DROPDOWN, value)
        return self

    def select_status(self, value: str) -> "InquiryFormPage":
        """Select inquiry status."""
        self.browser.select_by_text(*self.STATUS_DROPDOWN, value)
        return self

    def click_complete(self) -> "InquiryFormPage":
        """Click complete button."""
        self.browser.click(*self.COMPLETE_BUTTON)
        return self

    def click_previous(self) -> "InquiryFormPage":
        """Click previous button."""
        self.browser.click(*self.PREVIOUS_BUTTON)
        return self

    # ==================== STATE-CHECK METHODS (For Assertions) ====================

    def is_inquiry_saved(self) -> bool:
        """Check if inquiry was saved successfully."""
        return self.browser.is_element_displayed(*self.SUCCESS_MESSAGE, timeout=5)

    def is_inquiry_in_list(self) -> bool:
        """Check if inquiry appears in customer name display."""
        return self.browser.is_element_displayed(*self.CUSTOMER_NAME_DISPLAY, timeout=5)
