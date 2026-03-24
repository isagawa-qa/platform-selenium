"""
TestSovAILogin - Authentication tests for SovAI CRE/PM.

Validates that the admin user can log in to LibreChat via the Nginx-proxied
endpoint and access the chat interface.

Uses AAA pattern: Arrange, Act, Assert.

NOTE: Tests run in order within a session-scoped browser. Login test runs first,
subsequent tests in other modules reuse the authenticated session.
"""

import pytest
from resources.utilities import autologger
from roles.sovai.admin_role import AdminRole
from pages.sovai.login_page import LoginPage
from pages.sovai.chat_page import ChatPage


class TestSovAILogin:
    """
    Authentication tests for SovAI CRE/PM LibreChat instance.

    - @autologger("Test") decorator
    - Role workflow calls
    - Assert via Page Object state-check methods
    """

    @pytest.fixture(autouse=True)
    def setup(self, browser, config, test_users):
        """Pytest fixture wires browser, config, and test data into the test class."""
        self.browser = browser
        self.config = config
        self.test_users = test_users
        self.login_page = LoginPage(self.browser)
        self.chat_page = ChatPage(self.browser)

    # ==================== TEST METHODS ====================

    @pytest.mark.sovai
    @pytest.mark.auth
    @pytest.mark.smoke
    @autologger.automation_logger("Test")
    def test_admin_login_success(self):
        """
        Verify admin can log in with stored credentials.

        AAA Pattern:
        1. Arrange - Create AdminRole with sovai_admin credentials
        2. Act - Execute login workflow
        3. Assert - Verify redirected to chat page, no errors
        """
        # Arrange
        credentials = self.test_users["sovai_admin"]
        base_url = self.config["url"]

        admin = AdminRole(
            self.browser,
            base_url=base_url,
            email=credentials["email"],
            password=credentials["password"]
        )

        # Act
        admin.login_and_verify()

        # Assert
        assert self.login_page.is_on_chat_page(), \
            "Should be redirected to chat page after login"

        assert not self.login_page.has_error_message(), \
            "No error message should be displayed after successful login"
