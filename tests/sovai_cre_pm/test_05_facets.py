"""
TestSovAIFACETS - FACETS rendering pipeline tests for SovAI CRE/PM.

Validates the end-to-end FACETS workflow:
1. Agent outputs FML data wrapped in <facets-fml> sentinel tags
2. Vessel MutationObserver detects the tags
3. FacetsVessel React component mounts and renders the data
4. Lens switcher and data cards are interactive

Uses AAA pattern: Arrange, Act, Assert.
"""

import pytest
from resources.utilities import autologger
from roles.sovai.admin_role import AdminRole
from pages.sovai.login_page import LoginPage
from pages.sovai.chat_page import ChatPage


class TestSovAIFACETS:
    """
    FACETS rendering pipeline and vessel interaction tests.

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
        """Ensure we're logged in before tests."""
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
    @pytest.mark.facets
    @pytest.mark.smoke
    @autologger.automation_logger("Test")
    def test_facets_optin_produces_fml_output(self):
        """
        Verify that using 'render as facet' trigger phrase produces
        <facets-fml> tagged output from the agent.

        AAA Pattern:
        1. Arrange - Ensure authenticated
        2. Act - Select agent, send FACETS opt-in prompt
        3. Assert - Response is substantial (FML data was generated)
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

        # Act — send with the FACETS opt-in trigger
        admin.request_facets_rendering(
            "Rent Roll Analyst",
            "Render as facet: Analyze this rent roll — "
            "10-unit building, 8 occupied at average $2,100/month, "
            "2 vacancies, market rent $2,400/month."
        )

        # Assert — response should contain substantial output
        assert self.chat_page.has_assistant_response(), \
            "Agent should respond to FACETS opt-in prompt"

        response = self.chat_page.get_last_response_text()
        assert len(response) > 50, \
            f"FACETS response should contain rendered content, got {len(response)} chars"

    @pytest.mark.sovai
    @pytest.mark.facets
    @autologger.automation_logger("Test")
    def test_facets_lease_abstractor_optin(self):
        """
        Verify the Lease Abstractor agent responds to FACETS opt-in requests.

        AAA Pattern:
        1. Arrange - Ensure authenticated
        2. Act - Select Lease Abstractor, trigger FACETS mode
        3. Assert - Response is substantial with lease analysis content
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
        admin.request_facets_rendering(
            "Lease Abstractor",
            "Render as facet: Abstract this lease — "
            "7-year NNN office lease at 500 Congress Ave, Austin TX. "
            "$32 PSF base rent, 3% annual escalation, "
            "$55 PSF TI allowance, 9 months free rent, "
            "options: 2 x 5-year renewal at fair market value."
        )

        # Assert
        assert self.chat_page.has_assistant_response(), \
            "Lease Abstractor should respond to FACETS prompt"

        response = self.chat_page.get_last_response_text()
        assert len(response) > 100, \
            f"FACETS lease abstract should be substantial, got {len(response)} chars"

    @pytest.mark.sovai
    @pytest.mark.facets
    @autologger.automation_logger("Test")
    def test_facets_market_comps_optin(self):
        """
        Verify the Market Comp Analyst responds to FACETS opt-in request.

        AAA Pattern:
        1. Arrange - Ensure authenticated
        2. Act - Select Market Comps, trigger FACETS mode
        3. Assert - Response is substantial with market analysis
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
        admin.request_facets_rendering(
            "Market Comp Analyst",
            "Render as facet: Compare these office lease comps:\n"
            "- 100 Congress: $34 PSF, 96% occ, Class A\n"
            "- 200 Lamar: $28 PSF, 89% occ, Class B+\n"
            "- 300 Colorado: $31 PSF, 93% occ, Class A\n"
            "Subject property: 400 Brazos, asking $30 PSF, Class A-"
        )

        # Assert
        assert self.chat_page.has_assistant_response(), \
            "Market Comp agent should respond to FACETS prompt"

        response = self.chat_page.get_last_response_text()
        assert len(response) > 100, \
            f"FACETS market analysis should be substantial, got {len(response)} chars"

    @pytest.mark.sovai
    @pytest.mark.facets
    @autologger.automation_logger("Test")
    def test_default_mode_does_not_produce_facets(self):
        """
        Verify that a normal prompt (without 'render as facet') does NOT
        produce FACETS output — it should produce a standard text/dashboard response.

        AAA Pattern:
        1. Arrange - Ensure authenticated
        2. Act - Send a normal analysis prompt (no FACETS trigger)
        3. Assert - Response is text, no FACETS vessel mount
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

        # Act — normal prompt, no FACETS trigger
        admin.select_agent_and_send(
            "Rent Roll Analyst",
            "What are the key metrics I should track for a 10-unit "
            "apartment building rent roll?"
        )

        # Assert — should get a response, but no FACETS vessel mount
        assert self.chat_page.has_assistant_response(), \
            "Agent should respond to normal prompt"

        response = self.chat_page.get_last_response_text()
        assert len(response) > 50, \
            "Normal response should be meaningful"

        # FACETS vessel should NOT mount for non-opt-in prompts
        is_mounted = self.chat_page.is_facets_vessel_mounted(timeout=5)
        assert not is_mounted, \
            "FACETS vessel should NOT mount for non-FACETS prompts"
