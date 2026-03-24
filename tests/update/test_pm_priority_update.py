"""
TestPmPriorityUpdate

End-to-end test: Product Manager views priority update on PM Hub dashboard.

Validates:
1. PM Hub dashboard loads at http://localhost:3000/
2. Morning Brief card (priority items) is visible
3. Brief summary stats (items · overdue · meetings) are displayed
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
from pages.update.hub_dashboard_page import HubDashboardPage


class TestPmPriorityUpdate:

    @pytest.fixture(autouse=True)
    def setup(self, browser, config):
        """Pytest fixture wires browser and config into the test class."""
        self.browser = browser
        self.config = config
        self.hub_dashboard_page = HubDashboardPage(self.browser)

    @pytest.mark.update
    @autologger.automation_logger("Test")
    def test_product_manager_gets_priority_update(self):
        """
        As a Product Manager, I want to get an update on my priority items,
        so that I can quickly see what needs attention today.
        """

        # ── Arrange ───────────────────────────────────────────────────────────
        base_url = self.config["url"]

        product_manager = ProductManagerRole(
            browser_interface=self.browser,
            base_url=base_url
        )

        # ── Act ───────────────────────────────────────────────────────────────
        product_manager.get_priority_update()

        # ── Assert ────────────────────────────────────────────────────────────

        # 1. Verify we are on the dashboard
        assert self.hub_dashboard_page.is_on_dashboard(), \
            "Expected to be on PM Hub dashboard after navigation"

        # 2. Verify the Morning Brief (priority items) card is visible
        assert self.hub_dashboard_page.has_morning_brief_visible(), \
            "Expected Morning Brief card to be visible on the dashboard"

        # 3. Verify the brief summary stats are displayed
        assert self.hub_dashboard_page.has_item_title_and_status(), \
            "Expected Morning Brief summary stats (items · overdue · meetings) to be visible"
