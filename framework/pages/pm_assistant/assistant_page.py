"""
AssistantPage - Page Object Model

Page Object for the Tiffany PM Assistant page (http://localhost:3000/assistant).
Handles the chat interface: input, send, wait for response, and read response text.
"""

from selenium.webdriver.common.by import By
from interfaces.browser_interface import BrowserInterface


class AssistantPage:
    """
    Page Object for Tiffany PM Assistant Page.

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

    CHAT_INPUT            = (By.CSS_SELECTOR, "input[placeholder*='Ask Tiffany']")
    SEND_BUTTON           = (By.XPATH, "//button[contains(@class,'btn-primary') and normalize-space(text())='Send']")
    NEW_CHAT_BUTTON       = (By.XPATH, "//button[normalize-space(text())='New']")
    CHAT_CONTAINER        = (By.CSS_SELECTOR, "div[scrollable='true']")
    THINKING_INDICATOR    = (By.XPATH, "//*[contains(text(), 'Thinking')]")
    # Quick-action buttons (visible on fresh assistant page before any conversation)
    QUICK_ACTION_MY_BLOCKERS    = (By.XPATH, "//button[normalize-space(text())='My blockers']")
    QUICK_ACTION_PIPELINE       = (By.XPATH, "//button[normalize-space(text())='Pipeline']")
    QUICK_ACTION_SCHEDULE       = (By.XPATH, "//button[normalize-space(text())=\"Today's schedule\"]")
    QUICK_ACTION_SLACK          = (By.XPATH, "//button[normalize-space(text())='Slack activity']")
    QUICK_ACTION_SEARCH_JIRA    = (By.XPATH, "//button[normalize-space(text())='Search Jira']")

    # Assistant message rows align flex-start; the inner bubble div carries the text.
    # DOM inspection confirmed: no class names on chat elements — layout is inline-style only.
    LAST_ASSISTANT_ROW    = (By.XPATH, "(//div[contains(@style,'flex-start')])[last()]")
    LAST_ASSISTANT_BUBBLE = (By.XPATH, "(//div[contains(@style,'flex-start')]//div[contains(@style,'background')])[last()]")
    ANY_ASSISTANT_BUBBLE  = (By.XPATH, "//div[contains(@style,'flex-start')]//div[contains(@style,'background')]")
    

    # ==================== NAVIGATION ====================

    def wait_for_assistant_page(self, timeout: int = 15) -> "AssistantPage":
        """Wait for the Tiffany chat input to be visible."""
        self.browser.wait_for_element_visible(*self.CHAT_INPUT, timeout=timeout)
        return self

    # ==================== ATOMIC METHODS (One UI Action) ====================

    def click_new_chat(self) -> "AssistantPage":
        """Click the New button to start a fresh conversation session."""
        self.browser.click(*self.NEW_CHAT_BUTTON)
        return self

    def click_quick_action(self, action_name: str) -> "AssistantPage":
        """
        Click a quick-action button by its visible label.

        Args:
            action_name: One of 'My blockers', 'Pipeline', "Today's schedule",
                         'Slack activity', 'Search Jira'
        """
        action_map = {
            "My blockers":      self.QUICK_ACTION_MY_BLOCKERS,
            "Pipeline":         self.QUICK_ACTION_PIPELINE,
            "Today's schedule": self.QUICK_ACTION_SCHEDULE,
            "Slack activity":   self.QUICK_ACTION_SLACK,
            "Search Jira":      self.QUICK_ACTION_SEARCH_JIRA,
        }
        if action_name not in action_map:
            raise ValueError(
                f"Unknown quick-action '{action_name}'. Valid: {list(action_map.keys())}"
            )
        self.browser.click(*action_map[action_name])
        return self

    def enter_message(self, message: str) -> "AssistantPage":
        """Type a message into the chat input field."""
        self.browser.type(*self.CHAT_INPUT, message)
        return self

    def click_send(self) -> "AssistantPage":
        """Click the Send button to submit the message."""
        self.browser.click(*self.SEND_BUTTON)
        return self

    def wait_for_thinking(self, timeout: int = 5) -> "AssistantPage":
        """Wait for Tiffany's 'Thinking' indicator to appear (confirms message sent)."""
        self.browser.wait_for_element_visible(*self.THINKING_INDICATOR, timeout=timeout)
        return self

    def wait_for_response(self, timeout: int = 60) -> "AssistantPage":
        """Wait for Tiffany's 'Thinking' indicator to disappear (response complete)."""
        self.browser.wait_for_element_invisible(*self.THINKING_INDICATOR, timeout=timeout)
        return self

    def wait_for_response_message(self, timeout: int = 90) -> "AssistantPage":
        """Wait for an assistant response bubble to appear in the chat container."""
        self.browser.wait_for_element_visible(*self.ANY_ASSISTANT_BUBBLE, timeout=timeout)
        return self

    # ==================== STATE-CHECK METHODS (For Assertions) ====================

    def is_quick_action_visible(self, action_name: str) -> bool:
        """
        Check if a quick-action button with the given label is visible.

        Uses pre-defined locators — never constructs XPath dynamically to avoid
        apostrophe injection issues (LESSON 007).

        Args:
            action_name: One of 'My blockers', 'Pipeline', "Today's schedule",
                         'Slack activity', 'Search Jira'
        """
        action_map = {
            "My blockers":      self.QUICK_ACTION_MY_BLOCKERS,
            "Pipeline":         self.QUICK_ACTION_PIPELINE,
            "Today's schedule": self.QUICK_ACTION_SCHEDULE,
            "Slack activity":   self.QUICK_ACTION_SLACK,
            "Search Jira":      self.QUICK_ACTION_SEARCH_JIRA,
        }
        if action_name not in action_map:
            return False
        return self.browser.is_element_displayed(*action_map[action_name], timeout=5)

    def is_at_assistant_page(self) -> bool:
        """Check if currently on the Tiffany assistant page (via URL)."""
        return "/assistant" in self.browser.get_current_url()

    def is_thinking(self) -> bool:
        """Check if Tiffany is currently thinking/processing a response."""
        return self.browser.is_element_displayed(*self.THINKING_INDICATOR, timeout=3)

    def has_response_appeared(self) -> bool:
        """Check if at least one assistant response bubble is visible."""
        return self.browser.is_element_displayed(*self.ANY_ASSISTANT_BUBBLE, timeout=10)

    def get_last_response_text(self) -> str:
        """Get the text content of the last assistant response bubble."""
        return self.browser.get_text(*self.LAST_ASSISTANT_BUBBLE)
