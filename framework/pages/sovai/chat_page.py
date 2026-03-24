"""
SovAI ChatPage - Page Object Model

Page Object for the LibreChat chat interface. Handles sending messages,
reading responses, and detecting agent output types (dashboard, FACETS).

- NO decorators
- Locators as class constants
- Atomic methods (one UI action)
- Return self for chaining
- State-check methods for assertions
"""

import os
import time
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from interfaces.browser_interface import BrowserInterface


class ChatPage:
    """
    Page Object for LibreChat Chat Interface.

    Handles the main chat UI: agent selection, message sending,
    response detection, and artifact rendering verification.
    """

    def __init__(self, browser: BrowserInterface):
        """Compose BrowserInterface — NO inheritance."""
        self.browser = browser

    # ==================== LOCATORS (Class Constants) ====================

    # Chat input
    TEXTAREA = (By.CSS_SELECTOR, "#prompt-textarea")
    SEND_BUTTON = (By.CSS_SELECTOR, "#send-button")

    # Agent/Model selector (top bar) — LibreChat v0.8.3
    MODEL_SELECTOR = (By.XPATH, "//button[@aria-label='Select a model']")
    AGENTS_MENU = (By.CSS_SELECTOR, "#endpoint-agents-menu")
    AGENT_SEARCH = (By.CSS_SELECTOR, "input[placeholder*='Search']")
    AGENT_ITEM = (By.CSS_SELECTOR, "div[role='option']")

    # Messages — target only the main conversation area
    ASSISTANT_MESSAGE = (By.CSS_SELECTOR, "main .agent-turn")
    LAST_RESPONSE = (By.CSS_SELECTOR, "main .agent-turn:last-child")
    LOADING_INDICATOR = (By.CSS_SELECTOR, "[class*='result-streaming'], .animate-spin")
    MESSAGE_PROSE = (By.CSS_SELECTOR, ".prose.message-content")

    # Artifacts / Output
    ARTIFACT_FRAME = (By.CSS_SELECTOR, "iframe[class*='artifact'], iframe[sandbox]")
    ARTIFACT_BUTTON = (By.CSS_SELECTOR, "[class*='artifact'], button[class*='artifact']")
    CODE_BLOCK = (By.CSS_SELECTOR, "pre code, .code-block")

    # File upload — LibreChat has a hidden file input triggered by the paperclip button
    FILE_ATTACH_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Attach files'], button[id*='upload'], [class*='attach']")
    FILE_INPUT = (By.CSS_SELECTOR, "input[type='file']")
    ATTACHED_FILE_TAG = (By.CSS_SELECTOR, "[class*='file-tag'], [class*='attachment'], [class*='uploaded-file']")

    # New chat
    NEW_CHAT_BUTTON = (By.CSS_SELECTOR, "a[aria-label='New chat']")

    # Sidebar
    SIDEBAR = (By.CSS_SELECTOR, "nav, [class*='sidebar']")
    SIDEBAR_CHAT_ITEMS = (By.CSS_SELECTOR, "a[class*='conversation'], nav a[href*='/c/']")

    # FACETS Vessel (injected by Nginx MutationObserver)
    FACETS_VESSEL_MOUNT = (By.CSS_SELECTOR, ".facets-vessel-mount")
    FACETS_VESSEL_MOUNTED = (By.CSS_SELECTOR, "[data-vessel-mounted]")
    FACETS_CONTAINER = (By.CSS_SELECTOR, "#facets-vessel-root, [class*='facets-vessel']")
    FACETS_SETTINGS = (By.CSS_SELECTOR, "[class*='facets-settings'], [class*='vessel-settings']")
    FACETS_LENS_BUTTON = (By.CSS_SELECTOR, ".facets-vessel-mount button")
    FACETS_DATA_CARD = (By.CSS_SELECTOR, ".facets-vessel-mount [class*='card'], .facets-vessel-mount [class*='metric']")

    # ==================== NAVIGATION ====================

    def start_new_chat(self) -> "ChatPage":
        """Start a fresh conversation by navigating to /c/new."""
        current_url = self.browser.get_current_url()
        parsed = urlparse(current_url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        self.browser.navigate_to(f"{base}/c/new")
        time.sleep(2)
        return self

    def open_model_selector(self) -> "ChatPage":
        """Click the model/agent selector button in the top bar."""
        self.browser.wait_for_element_visible(*self.MODEL_SELECTOR, timeout=20)
        self.browser.click(*self.MODEL_SELECTOR)
        time.sleep(1)
        return self

    def click_agents_menu(self) -> "ChatPage":
        """Click the 'My Agents' menu item in the model selector dropdown."""
        self.browser.click(*self.AGENTS_MENU)
        time.sleep(1)
        return self

    def select_agent_by_name(self, agent_name: str) -> "ChatPage":
        """Select an agent by matching its name in the agent list."""
        # Use role='option' divs and match by text content
        agent_locator = (By.XPATH, f"//div[@role='option'][.//span[contains(text(), '{agent_name}')]]")
        self.browser.click(*agent_locator)
        time.sleep(2)
        return self

    # ==================== ATOMIC METHODS (One UI Action) ====================

    def wait_for_chat_ready(self, timeout: int = 15) -> "ChatPage":
        """Wait for the chat textarea to be ready for input."""
        self.browser.wait_for_element_visible(*self.TEXTAREA, timeout=timeout)
        return self

    def type_message(self, message: str) -> "ChatPage":
        """Type a message into the chat textarea."""
        self.browser.type(*self.TEXTAREA, message, clear_first=True)
        time.sleep(0.5)
        return self

    def click_send(self) -> "ChatPage":
        """Click the send button."""
        self.browser.click(*self.SEND_BUTTON)
        return self

    def send_message(self, message: str) -> "ChatPage":
        """Type and send a message (convenience method).

        Includes a stabilization wait after typing to let LibreChat
        process the input and enable the send button.
        """
        self.type_message(message)
        time.sleep(1)  # Let LibreChat enable the send button
        self.click_send()
        return self

    def attach_file(self, file_path: str) -> "ChatPage":
        """Attach a file to the chat message using the hidden file input.

        Selenium best practice: send_keys() on input[type=file] bypasses
        the OS file dialog. Works headless.

        Args:
            file_path: Absolute path to the file to attach.
        """
        abs_path = os.path.abspath(file_path)
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Cannot attach file — not found: {abs_path}")

        # Make the hidden file input visible via JS so send_keys works
        file_inputs = self.browser.find_elements(*self.FILE_INPUT, timeout=5)
        if file_inputs:
            self.browser.execute_script(
                "arguments[0].style.display = 'block'; "
                "arguments[0].style.visibility = 'visible'; "
                "arguments[0].style.height = '1px'; "
                "arguments[0].style.width = '1px';",
                file_inputs[0]
            )
            file_inputs[0].send_keys(abs_path)
        else:
            # Fallback: inject a file input if none exists
            self.browser.execute_script(
                "const input = document.createElement('input');"
                "input.type = 'file';"
                "input.id = 'selenium-file-upload';"
                "input.style.display = 'block';"
                "document.body.appendChild(input);"
            )
            injected = self.browser.find_element(By.ID, 'selenium-file-upload')
            injected.send_keys(abs_path)
        time.sleep(2)  # Wait for file processing
        return self

    def send_message_with_file(self, message: str, file_path: str) -> "ChatPage":
        """Attach a file and send a message in one operation."""
        self.attach_file(file_path)
        self.type_message(message)
        time.sleep(1)
        self.click_send()
        return self

    # Stop/generating indicators — present while agent turn is in progress
    STOP_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Stop generating'], button[aria-label='Cancel']")
    REGENERATE_BUTTON = (By.CSS_SELECTOR, "button[aria-label='Regenerate']")

    def wait_for_response(self, timeout: int = 120) -> "ChatPage":
        """
        Wait for the AI response to FULLY complete, including MCP tool cycles.

        Strategy:
        1. Wait for initial assistant message to appear
        2. Wait for the stop/generating button to disappear (full turn done)
        3. Confirm response text has stabilized (not still streaming)

        This handles multi-step agent turns: text → tool_call → tool_result → final text.
        """
        import time as t
        from selenium.common.exceptions import StaleElementReferenceException
        start = t.time()
        prev_text = ""
        stable_count = 0

        # Phase 1: Wait for any assistant message to appear
        while t.time() - start < timeout:
            try:
                messages = self.browser.find_elements(*self.ASSISTANT_MESSAGE, timeout=3)
                if messages and messages[-1].text.strip():
                    break
            except StaleElementReferenceException:
                pass
            t.sleep(2)

        # Phase 2: Wait for full turn completion (stop button disappears + text stabilizes)
        while t.time() - start < timeout:
            try:
                # Check if still generating
                stop_btns = self.browser.find_elements(*self.STOP_BUTTON, timeout=1)
                is_generating = len(stop_btns) > 0

                messages = self.browser.find_elements(*self.ASSISTANT_MESSAGE, timeout=1)
                current_text = messages[-1].text.strip() if messages else ""

                if not is_generating and len(current_text) > 50:
                    # Text must be stable for 2 consecutive polls
                    if current_text == prev_text:
                        stable_count += 1
                        if stable_count >= 2:
                            t.sleep(1)  # Final settle
                            return self
                    else:
                        stable_count = 0
                    prev_text = current_text

            except StaleElementReferenceException:
                stable_count = 0
            t.sleep(3)

        # Timeout — return anyway, test will assert on content
        return self

    # ==================== STATE-CHECK METHODS (For Assertions) ====================

    def get_last_response_text(self) -> str:
        """Get the text content of the last assistant message."""
        messages = self.browser.find_elements(*self.ASSISTANT_MESSAGE)
        if messages:
            return messages[-1].text
        return ""

    def has_assistant_response(self, timeout: int = 10) -> bool:
        """Check if at least one assistant message is present."""
        return self.browser.is_element_present(*self.ASSISTANT_MESSAGE, timeout=timeout)

    def response_contains(self, text: str) -> bool:
        """Check if the last response contains specific text."""
        return text.lower() in self.get_last_response_text().lower()

    def has_artifact_iframe(self, timeout: int = 10) -> bool:
        """Check if the response contains an artifact iframe (HTML dashboard)."""
        return self.browser.is_element_present(*self.ARTIFACT_FRAME, timeout=timeout)

    def has_artifact_button(self, timeout: int = 10) -> bool:
        """Check if the response has an artifact preview button."""
        return self.browser.is_element_present(*self.ARTIFACT_BUTTON, timeout=timeout)

    def has_code_block(self, timeout: int = 10) -> bool:
        """Check if the response contains a code block."""
        return self.browser.is_element_present(*self.CODE_BLOCK, timeout=timeout)

    def is_facets_vessel_present(self, timeout: int = 10) -> bool:
        """Check if the FACETS Vessel container is injected in the page."""
        return self.browser.is_element_present(*self.FACETS_CONTAINER, timeout=timeout)

    def is_facets_vessel_mounted(self, timeout: int = 30) -> bool:
        """Check if the FACETS Vessel actually mounted (React rendered into DOM)."""
        return self.browser.is_element_present(*self.FACETS_VESSEL_MOUNT, timeout=timeout)

    def is_prose_hidden_by_vessel(self, timeout: int = 10) -> bool:
        """Check if the raw FML prose has been hidden by the vessel scanner."""
        return self.browser.is_element_present(*self.FACETS_VESSEL_MOUNTED, timeout=timeout)

    def get_facets_vessel_text(self) -> str:
        """Get the text content rendered inside the FACETS vessel mount."""
        mounts = self.browser.find_elements(*self.FACETS_VESSEL_MOUNT, timeout=10)
        if mounts:
            return mounts[0].text
        return ""

    def get_facets_lens_buttons(self) -> list:
        """Get the text labels of all lens buttons in the vessel."""
        buttons = self.browser.find_elements(*self.FACETS_LENS_BUTTON, timeout=5)
        return [b.text.strip() for b in buttons if b.text.strip()]

    def get_facets_data_cards_count(self) -> int:
        """Count the number of data/metric cards rendered in the vessel."""
        cards = self.browser.find_elements(*self.FACETS_DATA_CARD, timeout=5)
        return len(cards)

    def get_response_count(self) -> int:
        """Get the number of assistant messages in the chat."""
        messages = self.browser.find_elements(*self.ASSISTANT_MESSAGE, timeout=5)
        return len(messages)

    def is_chat_input_ready(self) -> bool:
        """Check if the chat input textarea is visible and ready."""
        return self.browser.is_element_displayed(*self.TEXTAREA, timeout=5)

    def get_sidebar_chat_count(self) -> int:
        """Count the number of conversation items in the sidebar."""
        items = self.browser.find_elements(*self.SIDEBAR_CHAT_ITEMS, timeout=5)
        return len(items)

    def get_page_title(self) -> str:
        """Get the current page title."""
        return self.browser.get_page_title()

    def get_selected_model_text(self) -> str:
        """Get the text displayed in the model/agent selector button."""
        elements = self.browser.find_elements(*self.MODEL_SELECTOR, timeout=5)
        if elements:
            return elements[0].text.strip()
        return ""

    def has_file_attached(self, timeout: int = 5) -> bool:
        """Check if a file attachment indicator is visible in the chat input."""
        return self.browser.is_element_present(*self.ATTACHED_FILE_TAG, timeout=timeout)

    def is_response_empty(self) -> bool:
        """Check if the last assistant response is effectively empty.

        An 'empty' response = agent name/label visible but no substantial
        content (< 50 chars). This is the P0 blocker symptom.
        """
        messages = self.browser.find_elements(*self.ASSISTANT_MESSAGE, timeout=5)
        if not messages:
            return True
        last_text = messages[-1].text.strip()
        # Agent responses typically start with the agent name (short),
        # but should have substantial content beyond that
        return len(last_text) < 50

    def get_response_length(self) -> int:
        """Get the character count of the last assistant response."""
        return len(self.get_last_response_text())

    # ==================== CSS VERIFICATION (#58 Send Button Fix) ====================

    def get_send_button_dimensions(self) -> dict:
        """Get the computed width, height, and border-radius of the send button.

        Uses JavaScript to read computed styles, which reflect the actual
        rendered values after CSS injection via Nginx.

        Returns:
            dict with keys: width, height, border_radius (as floats in px)
        """
        script = """
        const btn = document.querySelector('#send-button')
            || document.querySelector('button[data-testid="send-button"]')
            || document.querySelector('button[aria-label="Send message"]');
        if (!btn) return null;
        const cs = window.getComputedStyle(btn);
        const rect = btn.getBoundingClientRect();
        return {
            width: rect.width,
            height: rect.height,
            border_radius: cs.borderRadius,
            padding: cs.padding,
            display: cs.display
        };
        """
        return self.browser.execute_script(script)

    def get_element_css_property(self, css_selector: str, property_name: str) -> str:
        """Get a computed CSS property value for any element.

        Args:
            css_selector: CSS selector for the target element
            property_name: CSS property name (e.g. 'color', 'background-color')

        Returns:
            Computed CSS value as a string, or empty string if element not found
        """
        script = f"""
        const el = document.querySelector('{css_selector}');
        if (!el) return '';
        return window.getComputedStyle(el).getPropertyValue('{property_name}');
        """
        return self.browser.execute_script(script) or ""

    def is_send_button_circular(self, tolerance: float = 4.0) -> bool:
        """Check if the send button is circular (width ≈ height, border-radius: 50%).

        Args:
            tolerance: Maximum allowed difference between width and height in px

        Returns:
            True if the send button is a compact circle (not an oversized pill)
        """
        dims = self.get_send_button_dimensions()
        if not dims:
            return False
        width = dims.get("width", 0)
        height = dims.get("height", 0)
        border_radius = dims.get("border_radius", "")
        # Must be roughly square (circular) and border-radius must be 50%
        is_square = abs(width - height) <= tolerance
        is_rounded = "50%" in border_radius or "9999" in border_radius
        is_compact = width <= 50 and height <= 50  # Not an oversized pill
        return is_square and is_rounded and is_compact
