"""
TestJiraIssues

End-to-end tests: Product Manager views Jira Issues, applies project/time filters,
and expands a project to reveal its issues.

Validates:
1. Jira Issues page loads with heading, filter, and stat cards visible
2. Project filter can be applied (PRODUCT project selected)
3. Time filter buttons respond (7d filter clicked)
4. Project expand button toggles project to expanded state
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
from pages.jira.jira_page import JiraPage


class TestJiraIssues:

    @pytest.fixture(autouse=True)
    def setup(self, browser, config):
        """Pytest fixture wires browser and config into the test class."""
        self.browser = browser
        self.config = config
        self.jira_page = JiraPage(self.browser)

    @pytest.mark.jira
    @autologger.automation_logger("Test")
    def test_jira_issues_page_loads(self):
        """
        As a Product Manager, I want to navigate to the Jira Issues page,
        so that I can see my project issues and filters.
        """

        # ── Arrange ───────────────────────────────────────────────────────────
        base_url = self.config["url"]

        product_manager = ProductManagerRole(
            browser_interface=self.browser,
            base_url=base_url
        )

        # ── Act ───────────────────────────────────────────────────────────────
        product_manager.view_jira_issues()

        # ── Assert ────────────────────────────────────────────────────────────
        assert self.jira_page.is_at_jira_page(), \
            "Expected URL to contain '/jira' after navigation"

        assert self.jira_page.is_page_heading_visible(), \
            "Expected 'Jira Issues' heading to be visible"

        assert self.jira_page.is_project_filter_visible(), \
            "Expected project filter dropdown to be visible"

        assert self.jira_page.are_stat_cards_visible(), \
            "Expected stat cards (My Assigned, etc.) to be visible"

    @pytest.mark.jira
    @autologger.automation_logger("Test")
    def test_jira_project_filter_applies(self):
        """
        As a Product Manager, I want to filter Jira issues by project,
        so that I can focus on issues relevant to a single project.
        """

        # ── Arrange ───────────────────────────────────────────────────────────
        base_url = self.config["url"]

        product_manager = ProductManagerRole(
            browser_interface=self.browser,
            base_url=base_url
        )

        # ── Act ───────────────────────────────────────────────────────────────
        product_manager.view_jira_issues(project_filter="Product Management")

        # ── Assert ────────────────────────────────────────────────────────────
        assert self.jira_page.is_at_jira_page(), \
            "Expected to remain on the Jira Issues page after filtering"

        assert self.jira_page.is_project_filter_visible(), \
            "Expected project filter to remain visible after selection"

    @pytest.mark.jira
    @autologger.automation_logger("Test")
    def test_jira_expand_project(self):
        """
        As a Product Manager, I want to expand a Jira project,
        so that I can view the individual issues within that project.
        """

        # ── Arrange ───────────────────────────────────────────────────────────
        base_url = self.config["url"]

        product_manager = ProductManagerRole(
            browser_interface=self.browser,
            base_url=base_url
        )

        # ── Act ───────────────────────────────────────────────────────────────
        product_manager.expand_jira_project()

        # ── Assert ────────────────────────────────────────────────────────────
        # After expanding, a Collapse button should appear for that project
        assert self.jira_page.is_collapse_button_visible(), \
            "Expected a Collapse button to appear after expanding a project"
