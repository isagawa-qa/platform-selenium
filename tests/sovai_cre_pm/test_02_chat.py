"""
TestSovAIChat - Core chat functionality tests for SovAI CRE/PM.

Validates that the admin user can send messages to agents and receive
responses through the LibreChat interface.

Uses AAA pattern: Arrange, Act, Assert.
"""

import pytest
from resources.utilities import autologger
from roles.sovai.admin_role import AdminRole
from pages.sovai.login_page import LoginPage
from pages.sovai.chat_page import ChatPage


class TestSovAIChat:
    """
    Chat functionality tests for SovAI CRE/PM.

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

    def _ensure_authenticated(self):
        """Ensure we're logged in before chat tests. Navigates and logs in if needed."""
        base_url = self.config["url"]
        current_url = self.browser.get_current_url()

        # If already on the chat page, no need to login
        if base_url.rstrip("/") in current_url and "/login" not in current_url:
            return

        # Not logged in — perform login
        credentials = self.test_users["sovai_admin"]
        admin = AdminRole(
            self.browser,
            base_url=base_url,
            email=credentials["email"],
            password=credentials["password"]
        )
        admin.login_and_verify()

    # ==================== TEST METHODS ====================

    @pytest.mark.sovai
    @pytest.mark.chat
    @pytest.mark.smoke
    @autologger.automation_logger("Test")
    def test_send_message_and_get_response(self):
        """
        Verify a basic message gets a response from the default agent.

        AAA Pattern:
        1. Arrange - Ensure authenticated, prepare admin role
        2. Act - Send a simple greeting
        3. Assert - Response received, chat input ready for next message
        """
        # Arrange
        self._ensure_authenticated()

        credentials = self.test_users["sovai_admin"]
        admin = AdminRole(
            self.browser,
            base_url=self.config["url"],
            email=credentials["email"],
            password=credentials["password"]
        )

        # Act — send message (already authenticated)
        admin.send_message_continue("Hello, what can you help me with?")

        # Assert
        assert self.chat_page.has_assistant_response(), \
            "At least one assistant response should be present"

        assert self.chat_page.is_chat_input_ready(), \
            "Chat input should be ready for the next message"

    @pytest.mark.sovai
    @pytest.mark.chat
    @autologger.automation_logger("Test")
    def test_agent_produces_substantial_response(self):
        """
        Verify that an agent can produce a substantial analytical response.

        AAA Pattern:
        1. Arrange - Ensure authenticated
        2. Act - Send a request that should trigger detailed output
        3. Assert - Response contains substantial content
        """
        # Arrange
        self._ensure_authenticated()

        credentials = self.test_users["sovai_admin"]
        admin = AdminRole(
            self.browser,
            base_url=self.config["url"],
            email=credentials["email"],
            password=credentials["password"]
        )

        # Act — Start new chat for clean state, then send analysis request
        self.chat_page.start_new_chat()
        admin.send_message_continue(
            "Create a sample portfolio summary showing 3 properties: "
            "Sunset Office (95% occupancy, $2.1M NOI), "
            "Harbor Retail (87% occupancy, $890K NOI), "
            "Industrial Park (100% occupancy, $1.5M NOI)"
        )

        # Assert
        assert self.chat_page.has_assistant_response(), \
            "Agent should respond with portfolio analysis"

        response_text = self.chat_page.get_last_response_text()
        assert len(response_text) > 100, \
            f"Response should contain substantial content, got {len(response_text)} chars"
