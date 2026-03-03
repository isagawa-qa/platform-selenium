"""
LoginPage - Page Object Model

Page Object for the login page. Handles authentication flow:
click Log In, enter credentials, sign in.
"""

from selenium.webdriver.common.by import By
from interfaces.browser_interface import BrowserInterface


class LoginPage:
    """
    Page Object for Login Page.

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

    LOG_IN_BUTTON = (By.CSS_SELECTOR, "[data-testid='button-goto-login']")
    EMAIL_INPUT = (By.CSS_SELECTOR, "[data-testid='input-email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "[data-testid='input-password']")
    SIGN_IN_BUTTON = (By.CSS_SELECTOR, "[data-testid='button-sign-in']")

    # ==================== NAVIGATION ====================

    def navigate(self, url: str) -> "LoginPage":
        """Navigate to the login page."""
        self.browser.navigate_to(url)
        return self

    # ==================== ATOMIC METHODS (One UI Action) ====================

    def wait_for_login_button_visible(self, timeout: int = 10) -> "LoginPage":
        """Wait for Log In button to be visible."""
        self.browser.wait_for_element_visible(*self.LOG_IN_BUTTON, timeout=timeout)
        return self

    def click_log_in(self) -> "LoginPage":
        """Click the Log In button to reveal the login form."""
        self.browser.click(*self.LOG_IN_BUTTON)
        return self

    def wait_for_email_visible(self, timeout: int = 10) -> "LoginPage":
        """Wait for email input to be visible."""
        self.browser.wait_for_element_visible(*self.EMAIL_INPUT, timeout=timeout)
        return self

    def enter_email(self, email: str) -> "LoginPage":
        """Enter email address."""
        self.browser.enter_text(*self.EMAIL_INPUT, email)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        """Enter password."""
        self.browser.enter_text(*self.PASSWORD_INPUT, password)
        return self

    def click_sign_in(self) -> "LoginPage":
        """Click the Sign In button."""
        self.browser.click(*self.SIGN_IN_BUTTON)
        return self

    # ==================== STATE-CHECK METHODS (For Assertions) ====================

    def is_on_dashboard(self) -> bool:
        """Check if redirected to dashboard after login."""
        return "/dashboard" in self.browser.get_current_url()
