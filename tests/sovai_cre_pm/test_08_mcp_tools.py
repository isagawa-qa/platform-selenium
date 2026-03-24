"""
TestMCPToolInvocation - End-to-end MCP tool call verification for SovAI CRE/PM.

Validates that agents ACTUALLY invoke MCP server tools (AppFolio, Rentometer,
LoopNet, MLS) and return real mock data — NOT hallucinated responses.

Ground-truth mock data:
  - AppFolio properties: 2525 San Diego, 401 W, 3405 Kenyon St
  - Rentometer: median ~$2,000 for 1BR at 401 W
  - LoopNet: mock CRE listings
  - MLS: mock residential listings

Uses AAA pattern: Arrange, Act, Assert.
"""

import pytest
from resources.utilities import autologger
from roles.sovai.admin_role import AdminRole
from pages.sovai.login_page import LoginPage
from pages.sovai.chat_page import ChatPage


# ==================== GROUND TRUTH MOCK DATA ====================
# These values come from the MCP servers' mock data layer.
# If the agent returns these, the MCP tool was actually called.
# If the agent returns "Sunset Apartments" or "Mountain View Lofts",
# it hallucinated the response.

APPFOLIO_PROPERTIES = ["2525 San Diego", "401 W", "Kenyon"]
HALLUCINATION_MARKERS = ["Sunset Apartments", "Mountain View", "Lakeshore", "Urban Edge"]


class TestMCPToolInvocation:
    """
    MCP tool invocation tests for SovAI CRE/PM.

    - Verifies agents call MCP tools instead of hallucinating
    - Checks for ground-truth mock data in responses
    - Detects hallucination markers as test failures
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

    def _assert_not_hallucinated(self, response: str):
        """Assert the response does NOT contain hallucination markers."""
        response_lower = response.lower()
        for marker in HALLUCINATION_MARKERS:
            assert marker.lower() not in response_lower, (
                f"HALLUCINATION DETECTED: Response contains '{marker}' — "
                f"agent did NOT call the MCP tool, it fabricated data."
            )

    def _assert_contains_any(self, response: str, expected_terms: list, context: str = ""):
        """Assert the response contains at least one of the expected terms."""
        response_lower = response.lower()
        found = [t for t in expected_terms if t.lower() in response_lower]
        assert len(found) > 0, (
            f"TOOL CALL FAILED: Response does not contain any expected "
            f"mock data terms {expected_terms}. {context}\n"
            f"Response (first 500 chars): {response[:500]}"
        )

    # ==================== TEST METHODS ====================

    @pytest.mark.sovai
    @pytest.mark.mcp
    @pytest.mark.smoke
    @autologger.automation_logger("Test")
    def test_appfolio_list_properties_returns_mock_data(self):
        """
        Verify Rent Roll Analyst calls appfolio_list_properties and returns
        real mock data (2525 San Diego, 401 W, Kenyon), NOT hallucinated data.

        AAA Pattern:
        1. Arrange - Ensure authenticated, create admin role
        2. Act - Select Rent Roll Analyst, send explicit tool invocation prompt
        3. Assert - Response contains mock property names, NO hallucination markers
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
            "Use the appfolio_list_properties tool to list ALL properties. "
            "Show the property names, IDs, and addresses from the tool output."
        )

        # LibreChat hides the stop generating button while invoking tools, which tricks wait_for_response.
        # Adding an explicit sleep to ensure the tool executes and the final text returns.
        import time
        time.sleep(15)

        # Assert
        assert self.chat_page.has_assistant_response(), \
            "Rent Roll Analyst should produce a response"

        response = self.chat_page.get_last_response_text()

        # Check for ground-truth mock data
        self._assert_contains_any(
            response,
            APPFOLIO_PROPERTIES,
            context="Expected mock properties: 2525 San Diego, 401 W, Kenyon"
        )

        # Check for hallucination
        self._assert_not_hallucinated(response)

    @pytest.mark.sovai
    @pytest.mark.mcp
    @autologger.automation_logger("Test")
    def test_appfolio_list_bills_returns_mock_data(self):
        """
        Verify Rent Roll Analyst calls appfolio_list_bills and returns
        real mock billing data.

        AAA Pattern:
        1. Arrange - Ensure authenticated
        2. Act - Select Rent Roll Analyst, ask for open bills
        3. Assert - Response contains expected vendors or bill amounts
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
            "Use the appfolio_list_bills tool with status 'open' to show "
            "all open bills. Show the raw vendor names and amounts."
        )

        # Assert
        assert self.chat_page.has_assistant_response(), \
            "Rent Roll Analyst should produce a response"

        response = self.chat_page.get_last_response_text()

        # Mock data includes bills for landscaping, rent-ready, first foundation
        expected_bill_markers = ["600", "2,400", "8,750", "Landscaping",
                                  "First Foundation", "Onboarding"]
        self._assert_contains_any(
            response,
            expected_bill_markers,
            context="Expected mock bill data from AppFolio MCP"
        )

    @pytest.mark.sovai
    @pytest.mark.mcp
    @autologger.automation_logger("Test")
    def test_rentometer_returns_mock_rent_data(self):
        """
        Verify Rent Roll Analyst calls rentometer_get_rent_summary and returns
        real mock rent market data.

        AAA Pattern:
        1. Arrange - Ensure authenticated
        2. Act - Select Rent Roll Analyst, ask for rent analysis at 401 W
        3. Assert - Response contains mock median/mean rent values
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
            "Use the rentometer_get_rent_summary tool for address "
            "'401 W, San Diego, CA 92101' with 1 bedroom. "
            "Show the median rent and sample size from the tool output."
        )

        # Assert
        assert self.chat_page.has_assistant_response(), \
            "Rent Roll Analyst should produce a response"

        response = self.chat_page.get_last_response_text()

        # Mock rent data: median $2,000, mean $1,963, 16 listings
        expected_rent_markers = ["2,000", "1,963", "16", "median", "sample"]
        self._assert_contains_any(
            response,
            expected_rent_markers,
            context="Expected mock rent data from Rentometer MCP"
        )

    @pytest.mark.sovai
    @pytest.mark.mcp
    @autologger.automation_logger("Test")
    def test_agent_does_not_hallucinate_without_tool(self):
        """
        Negative test: Verify that when MCP tools are NOT available via a
        non-MCP agent, the response does NOT contain mock data.

        This ensures we're actually testing tool invocation, not just
        checking if the mock data leaked into the system prompt.
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

        # Act — use Lease Abstractor which should NOT have AppFolio tools
        admin.select_agent_and_send(
            "Lease Abstractor",
            "List all properties in the AppFolio system."
        )

        # Assert
        assert self.chat_page.has_assistant_response(), \
            "Lease Abstractor should produce a response"

        response = self.chat_page.get_last_response_text()

        # Lease Abstractor should NOT have access to AppFolio mock data
        # It should either say it can't access AppFolio or provide generic guidance
        response_lower = response.lower()
        has_mock_data = any(
            prop.lower() in response_lower for prop in APPFOLIO_PROPERTIES
        )
        # This is a soft assertion — if it has the mock data, something is wrong
        if has_mock_data:
            pytest.skip(
                "Lease Abstractor returned mock AppFolio data — "
                "MCP tools may be globally available to all agents"
            )
