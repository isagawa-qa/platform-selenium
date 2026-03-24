"""
SovAI LoginPage - Page Object Model

Page Object for the LibreChat login page. Handles email→password two-step
authentication flow used by LibreChat's default auth UI.

- NO decorators
- Locators as class constants
- Atomic methods (one UI action)
- Return self for chaining
- State-check methods for assertions
"""

from selenium.webdriver.common.by import By
from interfaces.browser_interface import BrowserInterface


class LoginPage:
    """
    Page Object for LibreChat Login Page.

    LibreChat uses a two-step login:
    1. Enter email → click Continue
    2. Enter password → click Continue
    """

    def __init__(self, browser: BrowserInterface):
        """Compose BrowserInterface — NO inheritance."""
        self.browser = browser

    # ==================== LOCATORS (Class Constants) ====================

    EMAIL_INPUT = (By.CSS_SELECTOR, "#email")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "#password")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Continue']")
    WELCOME_TEXT = (By.XPATH, "//*[contains(text(), 'Welcome back')]")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[role='alert'], .text-red-500, .error-message")
    NEW_CHAT_BUTTON = (By.CSS_SELECTOR, "a[aria-label='New chat']")
    SIDEBAR = (By.CSS_SELECTOR, "div[aria-label='Conversations']")

    # ==================== NAVIGATION ====================

    def navigate(self, url: str) -> "LoginPage":
        """Navigate to the login page."""
        login_url = url.rstrip("/") + "/login"
        self.browser.navigate_to(login_url)
        return self

    # ==================== ATOMIC METHODS (One UI Action) ====================

    def wait_for_login_form(self, timeout: int = 15) -> "LoginPage":
        """Wait for the login form to be visible."""
        self.browser.wait_for_element_visible(*self.EMAIL_INPUT, timeout=timeout)
        return self

    def enter_email(self, email: str) -> "LoginPage":
        """Enter email address."""
        self.browser.type(*self.EMAIL_INPUT, email)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        """Enter password."""
        self.browser.type(*self.PASSWORD_INPUT, password)
        return self

    def click_continue(self) -> "LoginPage":
        """Click the Continue/Submit button."""
        self.browser.click(*self.CONTINUE_BUTTON)
        return self

    # ==================== STATE-CHECK METHODS (For Assertions) ====================

    def is_on_chat_page(self, timeout: int = 15) -> bool:
        """Check if redirected to the chat page after login."""
        try:
            self.browser.wait_for_url_contains("/c/", timeout=timeout)
            return True
        except Exception:
            # Also check for the root URL (some LibreChat versions redirect to /)
            return "/login" not in self.browser.get_current_url()

    def is_sidebar_visible(self, timeout: int = 10) -> bool:
        """Check if the sidebar is visible (indicates successful login)."""
        return self.browser.is_element_displayed(*self.SIDEBAR, timeout=timeout)

    def has_error_message(self, timeout: int = 5) -> bool:
        """Check if an error message is displayed."""
        return self.browser.is_element_displayed(*self.ERROR_MESSAGE, timeout=timeout)

    def is_new_chat_button_visible(self, timeout: int = 10) -> bool:
        """Check if the new chat button is visible (confirms logged-in state)."""
        return self.browser.is_element_displayed(*self.NEW_CHAT_BUTTON, timeout=timeout)
