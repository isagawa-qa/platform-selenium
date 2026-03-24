"""
SovAI ChatTasks - Task Layer

Single-domain operations for chat interactions: send message, wait for response.

- @autologger on methods
- Composes Page Objects
- One domain operation per method
- NO return values
"""

from resources.utilities import autologger
from pages.sovai.chat_page import ChatPage


class ChatTasks:
    """
    Chat interaction tasks for SovAI LibreChat.

    Composes ChatPage POM to perform chat operations.
    """

    def __init__(self, browser):
        """
        Initialize with browser.

        NO @autologger on constructor.
        """
        self.browser = browser
        self.chat_page = ChatPage(browser)

    # ==================== TASK METHODS ====================

    @autologger.automation_logger("Task")
    def start_new_conversation(self):
        """Start a new chat conversation. NO return value."""
        self.chat_page.start_new_chat()
        self.chat_page.wait_for_chat_ready()

    @autologger.automation_logger("Task")
    def send_message_and_wait(self, message: str, timeout: int = 120):
        """
        Send a chat message and wait for the AI response to complete.

        NO return value.
        """
        self.chat_page.wait_for_chat_ready()
        self.chat_page.send_message(message)
        self.chat_page.wait_for_response(timeout=timeout)

    @autologger.automation_logger("Task")
    def send_quick_message(self, message: str):
        """
        Send a brief message expecting a fast response (health checks, simple queries).

        NO return value.
        """
        self.chat_page.wait_for_chat_ready()
        self.chat_page.send_message(message)
        self.chat_page.wait_for_response(timeout=60)

    @autologger.automation_logger("Task")
    def select_agent(self, agent_name: str):
        """
        Select a specific agent from the model selector dropdown.

        NO return value.
        """
        self.chat_page.open_model_selector()
        self.chat_page.click_agents_menu()
        self.chat_page.select_agent_by_name(agent_name)

    @autologger.automation_logger("Task")
    def start_new_conversation_with_agent(self, agent_name: str):
        """
        Start a new chat and select a specific agent.

        Flow: navigate to /c/new → select agent → wait for chat ready.
        Agent must be selected before waiting for textarea since the
        dropdown may overlay the input area.

        NO return value.
        """
        self.chat_page.start_new_chat()
        self.select_agent(agent_name)
        self.chat_page.wait_for_chat_ready()

    @autologger.automation_logger("Task")
    def send_facets_request(self, prompt: str, timeout: int = 180):
        """
        Send a FACETS opt-in prompt and wait for the vessel to mount.

        NO return value.
        """
        self.chat_page.wait_for_chat_ready()
        self.chat_page.send_message(prompt)
        self.chat_page.wait_for_response(timeout=timeout)

    @autologger.automation_logger("Task")
    def send_message_with_file_and_wait(self, message: str, file_path: str, timeout: int = 120):
        """
        Attach a file and send a message, then wait for the AI response.

        Used for document upload + analysis testing.
        NO return value.
        """
        self.chat_page.wait_for_chat_ready()
        self.chat_page.send_message_with_file(message, file_path)
        self.chat_page.wait_for_response(timeout=timeout)
