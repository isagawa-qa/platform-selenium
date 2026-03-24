"""
SovAI AdminRole - Role Layer

Coordinates multi-task workflows for the SovAI admin persona.

- @autologger on workflow methods
- @autologger("Role Constructor") on __init__
- Composes Task modules
- Workflow methods call MULTIPLE tasks
- NO return values
"""

from resources.utilities import autologger
from tasks.sovai.auth_tasks import AuthTasks
from tasks.sovai.chat_tasks import ChatTasks


class AdminRole:
    """
    Admin user role for SovAI CRE/PM.

    Orchestrates authentication and chat tasks into business workflows.
    """

    @autologger.automation_logger("Role Constructor")
    def __init__(self, browser, base_url: str, email: str, password: str):
        """Initialize with credentials and compose tasks."""
        self.browser = browser
        self.base_url = base_url
        self.email = email
        self.password = password
        self.auth_tasks = AuthTasks(browser, base_url)
        self.chat_tasks = ChatTasks(browser)

    # ==================== WORKFLOW METHODS ====================

    @autologger.automation_logger("Role")
    def login_and_verify(self):
        """
        Complete login workflow: authenticate and confirm dashboard access.

        NO return value.
        """
        self.auth_tasks.login_with_credentials(self.email, self.password)

    @autologger.automation_logger("Role")
    def login_and_send_message(self, message: str):
        """
        Login, start new chat, and send a message.

        Multi-task workflow: auth → new chat → send message.
        NO return value.
        """
        self.auth_tasks.login_with_credentials(self.email, self.password)
        self.chat_tasks.start_new_conversation()
        self.chat_tasks.send_message_and_wait(message)

    @autologger.automation_logger("Role")
    def send_message_continue(self, message: str):
        """
        Send a message without re-authenticating (already logged in).

        _continue variant: skips login for shared sessions.
        NO return value.
        """
        self.chat_tasks.send_message_and_wait(message)

    @autologger.automation_logger("Role")
    def select_agent_and_send(self, agent_name: str, message: str):
        """
        Select a specific agent, start new chat, and send a message.

        Multi-task workflow: new chat → select agent → send message.
        NO return value.
        """
        self.chat_tasks.start_new_conversation_with_agent(agent_name)
        self.chat_tasks.send_message_and_wait(message)

    @autologger.automation_logger("Role")
    def request_facets_rendering(self, agent_name: str, prompt: str):
        """
        Select an agent, start new chat, and send a FACETS opt-in prompt.

        Multi-task workflow: new chat → select agent → send facets request.
        NO return value.
        """
        self.chat_tasks.start_new_conversation_with_agent(agent_name)
        self.chat_tasks.send_facets_request(prompt)

    @autologger.automation_logger("Role")
    def send_to_agent_continue(self, message: str):
        """
        Send a message to the currently selected agent (already logged in + agent selected).

        _continue variant for session-reuse.
        NO return value.
        """
        self.chat_tasks.send_message_and_wait(message)

    @autologger.automation_logger("Role")
    def select_agent_and_send_with_file(self, agent_name: str, message: str, file_path: str):
        """
        Select a specific agent, start new chat, attach a file, and send a message.

        Multi-task workflow: new chat → select agent → attach file → send message.
        Used for document upload regression testing (P0 blocker #29).
        NO return value.
        """
        self.chat_tasks.start_new_conversation_with_agent(agent_name)
        self.chat_tasks.send_message_with_file_and_wait(message, file_path)
