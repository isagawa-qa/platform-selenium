"""
TestNavigationSmoke

End-to-end smoke test: Product Manager navigates to each major section
of PM Hub via the sidebar and verifies the URL changes correctly.

Validates:
1. PM Hub loads with sidebar navigation visible
2. Each sidebar link navigates to the correct route
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
from pages.navigation.nav_page import NavPage


class TestNavigationSmoke:

    @pytest.fixture(autouse=True)
    def setup(self, browser, config):
        """Pytest fixture wires browser and config into the test class."""
        self.browser = browser
        self.config = config
        self.nav_page = NavPage(self.browser)

    @pytest.mark.navigation
    @pytest.mark.smoke
    @pytest.mark.parametrize("section,expected_path", [
        ("calendar",       "/calendar"),
        ("jira",           "/jira"),
        ("jira_approvals", "/jira/approvals"),
        ("assistant",      "/assistant"),
        ("settings",       "/settings"),
    ])
    @autologger.automation_logger("Test")
    def test_sidebar_navigates_to_section(self, section, expected_path):
        """
        As a Product Manager, I want to click each sidebar link,
        so that I can navigate to the correct section of PM Hub.
        """

        # ── Arrange ───────────────────────────────────────────────────────────
        base_url = self.config["url"]

        product_manager = ProductManagerRole(
            browser_interface=self.browser,
            base_url=base_url
        )

        # ── Act ───────────────────────────────────────────────────────────────
        product_manager.navigate_to_section(section)

        # ── Assert ────────────────────────────────────────────────────────────
        assert self.nav_page.is_at_url(expected_path), (
            f"Expected URL to contain '{expected_path}' after clicking "
            f"'{section}' sidebar link, but got: '{self.browser.get_current_url()}'"
        )
