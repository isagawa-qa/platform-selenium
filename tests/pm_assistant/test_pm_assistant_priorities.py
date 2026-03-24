"""
TestPmAssistantPriorities

End-to-end test: Product Manager asks Tiffany (PM Assistant) about priorities.

Validates:
1. PM Hub loads and Tiffany is accessible
2. A question about priorities can be submitted via the chat interface
3. Tiffany responds with a non-empty answer
"""

import sys
from pathlib import Path
import pytest

# Ensure framework is on the path
PROJECT_ROOT = Path(__file__).parent.parent.parent
FRAMEWORK_PATH = str(PROJECT_ROOT / "framework")
if FRAMEWORK_PATH not in sys.path:
    sys.path.insert(0, FRAMEWORK_PATH)

from resources.utilities import autologger
from roles.common.product_manager_role import ProductManagerRole
from pages.pm_assistant.assistant_page import AssistantPage


class TestPmAssistantPriorities:

    @pytest.fixture(autouse=True)
    def setup(self, browser, config):
        """Pytest fixture wires browser and config into the test class."""
        self.browser = browser
        self.config = config
        self.assistant_page = AssistantPage(self.browser)

    @pytest.mark.pm_assistant
    @autologger.automation_logger("Test")
    def test_product_manager_asks_tiffany_about_priorities(self):
        """
        As a Product Manager, I want to ask Tiffany what my priorities are,
        so that I can quickly understand what to focus on today.
        """

        # ── Arrange ───────────────────────────────────────────────────────────
        base_url = self.config["url"]
        question  = "What are my current priorities?"

        product_manager = ProductManagerRole(
            browser_interface=self.browser,
            base_url=base_url
        )

        # ── Act ───────────────────────────────────────────────────────────────
        product_manager.query_tiffany_for_priorities(question=question)

        # ── Assert ────────────────────────────────────────────────────────────

        # 1. Verify we are on the assistant page
        assert self.assistant_page.is_at_assistant_page(), \
            "Expected to be on /assistant page after navigation"

        # 2. Verify Tiffany responded (a response message block is visible)
        assert self.assistant_page.has_response_appeared(), \
            "Expected Tiffany to produce a response message, but none appeared"

        # 3. Verify the response is non-empty
        response_text = self.assistant_page.get_last_response_text()
        assert response_text and len(response_text.strip()) > 0, \
            f"Expected a non-empty response from Tiffany, got: '{response_text}'"
