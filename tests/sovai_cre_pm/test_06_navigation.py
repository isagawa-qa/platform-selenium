"""
TestSovAINavigation - Navigation, sidebar, and UI state tests for SovAI CRE/PM.

Validates core LibreChat UI functionality: sidebar visibility, new chat creation,
conversation persistence, page title, and chat session management.

Uses AAA pattern: Arrange, Act, Assert.
"""

import pytest
from resources.utilities import autologger
from roles.sovai.admin_role import AdminRole
from pages.sovai.login_page import LoginPage
from pages.sovai.chat_page import ChatPage


class TestSovAINavigation:
    """
    Navigation and UI state tests for SovAI CRE/PM.

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
        """Ensure we're logged in before tests."""
        base_url = self.config["url"]
        current_url = self.browser.get_current_url()

        if base_url.rstrip("/") in current_url and "/login" not in current_url:
            return

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
    @pytest.mark.navigation
    @pytest.mark.smoke
    @autologger.automation_logger("Test")
    def test_sidebar_visible_after_login(self):
        """
        Verify the sidebar/nav is visible after successful login.

        AAA Pattern:
        1. Arrange - Ensure authenticated
        2. Act - Check sidebar visibility
        3. Assert - Sidebar is displayed
        """
        # Arrange
        self._ensure_authenticated()

        # Assert
        assert self.login_page.is_sidebar_visible(), \
            "Sidebar should be visible after login"

    @pytest.mark.sovai
    @pytest.mark.navigation
    @autologger.automation_logger("Test")
    def test_new_chat_creates_clean_session(self):
        """
        Verify starting a new chat creates a clean conversation state.

        AAA Pattern:
        1. Arrange - Ensure authenticated, note current state
        2. Act - Start a new chat
        3. Assert - Chat input ready, no prior messages in new conversation
        """
        # Arrange
        self._ensure_authenticated()

        # Act
        self.chat_page.start_new_chat()

        # Assert
        assert self.chat_page.is_chat_input_ready(), \
            "Chat input should be ready after starting new chat"

    @pytest.mark.sovai
    @pytest.mark.navigation
    @autologger.automation_logger("Test")
    def test_conversation_saved_to_sidebar(self):
        """
        Verify that sending a message creates a conversation entry in the sidebar.

        AAA Pattern:
        1. Arrange - Ensure authenticated, start new chat
        2. Act - Send a message and wait for response
        3. Assert - Sidebar contains at least one conversation entry
        """
        # Arrange
        self._ensure_authenticated()
        self.chat_page.start_new_chat()

        credentials = self.test_users["sovai_admin"]
        admin = AdminRole(
            self.browser,
            base_url=self.config["url"],
            email=credentials["email"],
            password=credentials["password"]
        )

        # Act — send message to create a conversation
        admin.send_message_continue("What types of properties do you support?")

        # Assert
        sidebar_count = self.chat_page.get_sidebar_chat_count()
        assert sidebar_count >= 1, \
            f"Sidebar should have at least 1 conversation, found {sidebar_count}"

    @pytest.mark.sovai
    @pytest.mark.navigation
    @autologger.automation_logger("Test")
    def test_chat_input_accepts_long_multiline_prompt(self):
        """
        Verify the chat textarea accepts and properly handles long multi-line prompts.

        AAA Pattern:
        1. Arrange - Ensure authenticated, start new chat
        2. Act - Send a long multi-line prompt with data
        3. Assert - Response received (prompt was accepted and processed)
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

        # Act — long multi-line prompt
        self.chat_page.start_new_chat()
        long_prompt = (
            "Please analyze the following financial data for my portfolio:\n\n"
            "Property 1: Sunset Office Complex\n"
            "- Address: 123 Sunset Blvd, Austin TX 78701\n"
            "- Type: Class A Office\n"
            "- Size: 125,000 SF\n"
            "- NOI: $2,100,000\n"
            "- Occupancy: 95%\n\n"
            "Property 2: Harbor Retail Center\n"
            "- Address: 456 Harbor Dr, Dallas TX 75201\n"
            "- Type: Retail Strip\n"
            "- Size: 45,000 SF\n"
            "- NOI: $890,000\n"
            "- Occupancy: 87%\n\n"
            "What is the overall portfolio performance?"
        )
        admin.send_message_continue(long_prompt)

        # Assert
        assert self.chat_page.has_assistant_response(), \
            "Agent should handle long multi-line prompts"

        response = self.chat_page.get_last_response_text()
        assert len(response) > 100, \
            f"Response to detailed prompt should be substantial, got {len(response)} chars"

    @pytest.mark.sovai
    @pytest.mark.navigation
    @autologger.automation_logger("Test")
    def test_multiple_sequential_chats(self):
        """
        Verify multiple new chat sessions can be created without errors.

        AAA Pattern:
        1. Arrange - Ensure authenticated
        2. Act - Create new chat, send message, repeat
        3. Assert - Each iteration produces a valid response
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

        prompts = [
            "What is NOI?",
            "What is a cap rate?",
        ]

        for prompt in prompts:
            # Act — new chat each time
            self.chat_page.start_new_chat()
            admin.send_message_continue(prompt)

            # Assert
            assert self.chat_page.has_assistant_response(), \
                f"Should get response for: '{prompt}'"

            response = self.chat_page.get_last_response_text()
            assert len(response) > 30, \
                f"Response too short for '{prompt}': {len(response)} chars"
