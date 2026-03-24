"""
PmAssistantTasks - Task module

Orchestrates Page Objects to accomplish PM Assistant workflows.
Handles navigation to Tiffany and querying for priorities.
"""

from interfaces.browser_interface import BrowserInterface
from pages.pm_assistant.hub_page import HubPage
from pages.pm_assistant.assistant_page import AssistantPage
from resources.utilities import autologger


class PmAssistantTasks:
    """
    Task module for PM Assistant (Tiffany) workflow.

    - @autologger("Task") on all methods
    - NO decorator on constructor
    - Composes Page Objects
    - One domain operation per method
    - NO return values
    """

    def __init__(self, browser: BrowserInterface):
        """
        Compose Page Objects — NO decorator on constructor.

        Args:
            browser: BrowserInterface instance
        """
        self.browser = browser
        self.hub_page = HubPage(browser)
        self.assistant_page = AssistantPage(browser)

    # ==================== TASK METHODS ====================

    @autologger.automation_logger("Task")
    def navigate_to_pm_hub(self, base_url: str) -> None:
        """
        Navigate to PM Hub and wait for the dashboard to load.

        Args:
            base_url: Base URL of the PM Hub application
        """
        (self.hub_page
            .navigate(base_url)
            .wait_for_hub_loaded())

    @autologger.automation_logger("Task")
    def open_tiffany_assistant(self) -> None:
        """
        Click the PM Assistant link in the sidebar and wait for Tiffany to load.
        """
        (self.hub_page
            .click_pm_assistant())
        (self.assistant_page
            .wait_for_assistant_page())

    @autologger.automation_logger("Task")
    def ask_tiffany_about_priorities(self, question: str) -> None:
        """
        Type the priorities question into the chat input and send it.
        Waits for Tiffany to finish responding.

        Args:
            question: The question to ask Tiffany about priorities
        """
        (self.assistant_page
            .enter_message(question)
            .click_send()
            .wait_for_response_message())

    @autologger.automation_logger("Task")
    def click_quick_action(self, action_name: str) -> None:
        """
        Click a quick-action button on the assistant page and wait for Tiffany to respond.

        Args:
            action_name: One of 'My blockers', 'Pipeline', "Today's schedule",
                         'Slack activity', 'Search Jira'
        """
        (self.assistant_page
            .click_quick_action(action_name)
            .wait_for_response_message())

    @autologger.automation_logger("Task")
    def start_new_conversation(self) -> None:
        """
        Click the New button to clear the current conversation and start fresh.
        Waits for the chat input to be ready again.
        """
        (self.assistant_page
            .click_new_chat()
            .wait_for_assistant_page())
