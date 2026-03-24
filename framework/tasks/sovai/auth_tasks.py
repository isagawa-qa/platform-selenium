"""
SovAI AuthTasks - Task Layer

Single-domain operation: authenticate a user via LibreChat login.

- @autologger on methods
- Composes Page Objects
- One domain operation per method
- NO return values
"""

from resources.utilities import autologger
from pages.sovai.login_page import LoginPage


class AuthTasks:
    """
    Authentication tasks for SovAI LibreChat.

    Composes LoginPage POM to perform login operations.
    """

    def __init__(self, browser, base_url: str):
        """
        Initialize with browser and base URL.

        NO @autologger on constructor.
        """
        self.browser = browser
        self.base_url = base_url
        self.login_page = LoginPage(browser)

    # ==================== TASK METHODS ====================

    @autologger.automation_logger("Task")
    def login_with_credentials(self, email: str, password: str):
        """
        Perform full login flow: navigate → email → continue → password → continue.

        LibreChat uses a two-step form: email first, then password.

        NO return value.
        """
        self.login_page.navigate(self.base_url)
        self.login_page.wait_for_login_form()
        self.login_page.enter_email(email)
        self.login_page.enter_password(password)
        self.login_page.click_continue()

        # Wait for post-login redirect
        import time
        time.sleep(3)
