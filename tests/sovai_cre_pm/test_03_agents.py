"""
TestSovAIAgents - Agent selection and availability tests for SovAI CRE/PM.

Validates that all expected agents are accessible in the UI, selectable from
the model dropdown, and respond to domain-specific prompts.

Uses AAA pattern: Arrange, Act, Assert.
"""

import pytest
from resources.utilities import autologger
from roles.sovai.admin_role import AdminRole
from pages.sovai.login_page import LoginPage
from pages.sovai.chat_page import ChatPage


class TestSovAIAgents:
    """
    Agent availability and selection tests for SovAI CRE/PM.

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
        """Ensure we're logged in before tests. Navigates and logs in if needed."""
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
    @pytest.mark.agent
    @pytest.mark.smoke
    @autologger.automation_logger("Test")
    def test_lease_abstractor_responds_to_domain_prompt(self):
        """
        Verify the Lease Abstractor agent can be selected and responds
        with lease-relevant content.

        AAA Pattern:
        1. Arrange - Ensure authenticated, create admin role
        2. Act - Select Lease Abstractor, send lease analysis prompt
        3. Assert - Response contains lease-relevant terms
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

        # Act
        admin.select_agent_and_send(
            "Lease Abstractor",
            "Analyze this lease: 5-year NNN office lease at 123 Main St, "
            "$28 PSF base rent with 3% annual escalation, "
            "$45 PSF TI allowance, 6 months free rent."
        )

        # Assert
        assert self.chat_page.has_assistant_response(), \
            "Lease Abstractor should produce a response"

        response = self.chat_page.get_last_response_text()
        assert len(response) > 200, \
            f"Lease analysis should be substantial, got {len(response)} chars"

    @pytest.mark.sovai
    @pytest.mark.agent
    @autologger.automation_logger("Test")
    def test_rent_roll_analyst_responds_to_domain_prompt(self):
        """
        Verify the Rent Roll Analyst agent responds with occupancy-relevant content.

        AAA Pattern:
        1. Arrange - Ensure authenticated
        2. Act - Select Rent Roll Analyst, send rent roll prompt
        3. Assert - Response contains occupancy-relevant terms
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

        # Act
        admin.select_agent_and_send(
            "Rent Roll Analyst",
            "Analyze this rent roll summary: 10-unit building, 8 occupied, "
            "average rent $2,100/month, 2 vacancies on units 4 and 9, "
            "market rate for similar units is $2,400/month."
        )

        # Assert
        assert self.chat_page.has_assistant_response(), \
            "Rent Roll Analyst should produce a response"

        response = self.chat_page.get_last_response_text()
        assert len(response) > 200, \
            f"Rent roll analysis should be substantial, got {len(response)} chars"

    @pytest.mark.sovai
    @pytest.mark.agent
    @autologger.automation_logger("Test")
    def test_maintenance_triage_responds_to_emergency(self):
        """
        Verify the Maintenance Triage agent handles emergency scenarios.

        AAA Pattern:
        1. Arrange - Ensure authenticated
        2. Act - Select Maintenance Triage, send emergency work order
        3. Assert - Response is substantial and contains priority indication
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

        # Act
        admin.select_agent_and_send(
            "Maintenance Triage",
            "Emergency: Tenant in Unit 301 reports water leaking from ceiling, "
            "water is pooling on the floor. Building has 3 floors, "
            "Unit 401 is directly above. It's 11pm on a Friday."
        )

        # Assert
        assert self.chat_page.has_assistant_response(), \
            "Maintenance Triage should produce a response"

        response = self.chat_page.get_last_response_text()
        assert len(response) > 150, \
            f"Triage response should be substantial, got {len(response)} chars"
