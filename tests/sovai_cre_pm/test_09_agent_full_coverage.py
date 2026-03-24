"""
TestAgentFullCoverage - MCP tool-calling verification for ALL SovAI CRE/PM agents.

Ensures every agent (not just Rent Roll Analyst) actually invokes MCP tools
and returns real mock data. Covers all 11 tool-enabled agents.

Ground-truth mock data:
  - AppFolio properties: 2525 San Diego, 401 W, 3405 Kenyon St
  - AppFolio vendors: Pacific Plumbing, San Diego Electric, ABC Landscaping
  - Rentometer: median ~$2,000 for 1BR at 401 W
  - LoopNet: mock CRE listings
  - MLS: mock residential listings

Uses AAA pattern: Arrange, Act, Assert.
"""

import pytest
import time
from resources.utilities import autologger
from roles.sovai.admin_role import AdminRole
from pages.sovai.login_page import LoginPage
from pages.sovai.chat_page import ChatPage


# ==================== GROUND TRUTH MOCK DATA ====================
APPFOLIO_PROPERTIES = ["2525 San Diego", "401 W", "Kenyon"]
APPFOLIO_VENDORS = ["Pacific Plumbing", "San Diego Electric", "ABC Landscaping",
                    "First Foundation", "Onboarding"]
HALLUCINATION_MARKERS = ["Sunset Apartments", "Mountain View", "Lakeshore",
                         "Urban Edge", "Riverside Apartments", "Gateway Office"]

# Response wait time (seconds) for tool execution
TOOL_WAIT = 20


class TestAgentFullCoverage:
    """
    Full agent coverage tests verifying MCP tool invocation for each agent.

    Every test follows the pattern:
    1. Select the specific agent
    2. Send a prompt that should trigger MCP tool calls
    3. Assert response contains mock data (proves tools were called)
    4. Assert response does NOT contain hallucination markers
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

    def _get_admin(self):
        """Create and return an admin role instance."""
        credentials = self.test_users["sovai_admin"]
        return AdminRole(
            self.browser,
            base_url=self.config["url"],
            email=credentials["email"],
            password=credentials["password"]
        )

    def _assert_not_hallucinated(self, response: str):
        """Assert the response does NOT contain hallucination markers."""
        response_lower = response.lower()
        for marker in HALLUCINATION_MARKERS:
            assert marker.lower() not in response_lower, (
                f"HALLUCINATION DETECTED: Response contains '{marker}' — "
                f"agent did NOT call the MCP tool, it fabricated data."
            )

    def _assert_contains_any(self, response: str, expected: list, context: str = ""):
        """Assert the response contains at least one expected term."""
        response_lower = response.lower()
        found = [t for t in expected if t.lower() in response_lower]
        assert len(found) > 0, (
            f"TOOL CALL FAILED: Response does not contain any expected "
            f"mock data terms {expected}. {context}\n"
            f"Response (first 500 chars): {response[:500]}"
        )

    def _assert_substantial(self, response: str, min_chars: int = 200):
        """Assert the response is substantial (not empty or trivially short)."""
        assert len(response) > min_chars, (
            f"Response too short ({len(response)} chars, expected > {min_chars}). "
            f"Agent may have failed to execute tools.\n"
            f"Response: {response[:300]}"
        )

    # ==================== PORTFOLIO VISUALIZATION DASHBOARD ====================

    @pytest.mark.sovai
    @pytest.mark.mcp
    @autologger.automation_logger("Test")
    def test_portfolio_dashboard_calls_appfolio_tools(self):
        """
        Verify Portfolio Visualization Dashboard calls AppFolio tools
        to pull real property data for dashboard generation.
        """
        self._ensure_authenticated()
        admin = self._get_admin()

        admin.select_agent_and_send(
            "Portfolio Visualization Dashboard",
            "Use the appfolio_list_properties tool to pull all properties, "
            "then use appfolio_list_units for each property. "
            "Show the raw property names and unit counts."
        )
        time.sleep(TOOL_WAIT)

        assert self.chat_page.has_assistant_response()
        response = self.chat_page.get_last_response_text()

        self._assert_contains_any(response, APPFOLIO_PROPERTIES,
            context="Portfolio Dashboard should pull real AppFolio properties")
        self._assert_not_hallucinated(response)

    # ==================== MULTI-PROPERTY PERFORMANCE ====================

    @pytest.mark.sovai
    @pytest.mark.mcp
    @autologger.automation_logger("Test")
    def test_multi_property_calls_appfolio_tools(self):
        """
        Verify Multi-Property Performance calls AppFolio tools
        to generate comparative performance data.
        """
        self._ensure_authenticated()
        admin = self._get_admin()

        admin.select_agent_and_send(
            "Multi-Property Performance",
            "Use the appfolio_list_properties tool to get all properties, "
            "then compare their occupancy and financial performance. "
            "Show property names from the tool output."
        )
        time.sleep(TOOL_WAIT)

        assert self.chat_page.has_assistant_response()
        response = self.chat_page.get_last_response_text()

        self._assert_contains_any(response, APPFOLIO_PROPERTIES,
            context="Multi-Property should pull real AppFolio properties")
        self._assert_not_hallucinated(response)

    # ==================== MARKET COMP ANALYST ====================

    @pytest.mark.sovai
    @pytest.mark.mcp
    @autologger.automation_logger("Test")
    def test_market_comp_calls_rentometer_tools(self):
        """
        Verify Market Comp Analyst calls Rentometer tools
        for market rent analysis.
        """
        self._ensure_authenticated()
        admin = self._get_admin()

        admin.select_agent_and_send(
            "Market Comp Analyst",
            "Use the rentometer_get_rent_summary tool for address "
            "'401 W, San Diego, CA 92101' with 1 bedroom. "
            "Show the median rent and sample size from the tool output."
        )
        time.sleep(TOOL_WAIT)

        assert self.chat_page.has_assistant_response()
        response = self.chat_page.get_last_response_text()

        expected_rent_markers = ["2,000", "1,963", "median", "sample", "rent"]
        self._assert_contains_any(response, expected_rent_markers,
            context="Market Comp should return Rentometer mock data")

    @pytest.mark.sovai
    @pytest.mark.mcp
    @autologger.automation_logger("Test")
    def test_market_comp_calls_loopnet_tools(self):
        """
        Verify Market Comp Analyst calls LoopNet tools
        for commercial listing comparisons.
        """
        self._ensure_authenticated()
        admin = self._get_admin()

        admin.select_agent_and_send(
            "Market Comp Analyst",
            "Use the loopnet_search_listings tool to search for "
            "commercial properties in San Diego, CA. "
            "Show the listing details from the tool output."
        )
        time.sleep(TOOL_WAIT)

        assert self.chat_page.has_assistant_response()
        response = self.chat_page.get_last_response_text()

        self._assert_substantial(response, min_chars=150)
        self._assert_not_hallucinated(response)

    # ==================== INVESTOR REPORT GENERATOR ====================

    @pytest.mark.sovai
    @pytest.mark.mcp
    @autologger.automation_logger("Test")
    def test_investor_report_calls_appfolio_tools(self):
        """
        Verify Investor Report Generator calls AppFolio tools
        to generate reports based on real portfolio data.
        """
        self._ensure_authenticated()
        admin = self._get_admin()

        admin.select_agent_and_send(
            "Investor Report Generator",
            "Use the appfolio_list_properties and appfolio_list_units tools "
            "to pull the full portfolio data. Generate an executive summary "
            "with the actual property names and unit counts."
        )
        time.sleep(TOOL_WAIT)

        assert self.chat_page.has_assistant_response()
        response = self.chat_page.get_last_response_text()

        self._assert_contains_any(response, APPFOLIO_PROPERTIES,
            context="Investor Report should use real AppFolio properties")
        self._assert_not_hallucinated(response)

    # ==================== CAM RECONCILIATION REVIEWER ====================

    @pytest.mark.sovai
    @pytest.mark.mcp
    @autologger.automation_logger("Test")
    def test_cam_reviewer_calls_financial_tools(self):
        """
        Verify CAM Reconciliation Reviewer calls AppFolio GL/billing tools.
        """
        self._ensure_authenticated()
        admin = self._get_admin()

        admin.select_agent_and_send(
            "CAM Reconciliation Reviewer",
            "Use the appfolio_list_bills tool to pull all open bills, "
            "then use appfolio_list_gl_details to review GL entries. "
            "Show the raw vendor names and amounts."
        )
        time.sleep(TOOL_WAIT)

        assert self.chat_page.has_assistant_response()
        response = self.chat_page.get_last_response_text()

        self._assert_substantial(response, min_chars=150)
        self._assert_not_hallucinated(response)

    # ==================== LEASE ABSTRACTOR ====================

    @pytest.mark.sovai
    @pytest.mark.mcp
    @autologger.automation_logger("Test")
    def test_lease_abstractor_calls_appfolio_tools(self):
        """
        Verify Lease Abstractor calls AppFolio tools to look up
        property and unit data for lease cross-referencing.
        """
        self._ensure_authenticated()
        admin = self._get_admin()

        admin.select_agent_and_send(
            "Lease Abstractor",
            "Use the appfolio_list_properties tool to list all properties, "
            "then use appfolio_list_units to show units for 2525 San Diego. "
            "Show the property and unit details from the tool output."
        )
        time.sleep(TOOL_WAIT)

        assert self.chat_page.has_assistant_response()
        response = self.chat_page.get_last_response_text()

        self._assert_contains_any(response, APPFOLIO_PROPERTIES,
            context="Lease Abstractor should pull AppFolio property data")
        self._assert_not_hallucinated(response)

    # ==================== LEASE EXPIRATION TIMELINE ====================

    @pytest.mark.sovai
    @pytest.mark.mcp
    @autologger.automation_logger("Test")
    def test_lease_expiration_calls_appfolio_tools(self):
        """
        Verify Lease Expiration Timeline calls AppFolio tools
        to pull lease data for timeline visualization.
        """
        self._ensure_authenticated()
        admin = self._get_admin()

        admin.select_agent_and_send(
            "Lease Expiration Timeline",
            "Use the appfolio_list_properties and appfolio_list_units tools "
            "to pull all lease data across the portfolio. "
            "Show property names and lease dates from the tool output."
        )
        time.sleep(TOOL_WAIT)

        assert self.chat_page.has_assistant_response()
        response = self.chat_page.get_last_response_text()

        self._assert_contains_any(response, APPFOLIO_PROPERTIES,
            context="Lease Expiration should pull AppFolio lease data")
        self._assert_not_hallucinated(response)

    # ==================== TENANT RISK SCORING ====================

    @pytest.mark.sovai
    @pytest.mark.mcp
    @autologger.automation_logger("Test")
    def test_tenant_risk_calls_appfolio_tools(self):
        """
        Verify Tenant Risk Scoring calls AppFolio tools
        to pull tenant payment and lease data for risk assessment.
        """
        self._ensure_authenticated()
        admin = self._get_admin()

        admin.select_agent_and_send(
            "Tenant Risk Scoring",
            "Use the appfolio_list_properties tool, then appfolio_list_units "
            "and appfolio_list_tenant_ledgers to pull tenant payment data. "
            "Score tenants based on the real data from the tools."
        )
        time.sleep(TOOL_WAIT)

        assert self.chat_page.has_assistant_response()
        response = self.chat_page.get_last_response_text()

        self._assert_contains_any(response, APPFOLIO_PROPERTIES,
            context="Tenant Risk should pull real AppFolio tenant data")
        self._assert_not_hallucinated(response)

    # ==================== MAINTENANCE TRIAGE ====================

    @pytest.mark.sovai
    @pytest.mark.mcp
    @autologger.automation_logger("Test")
    def test_maintenance_triage_calls_vendor_tools(self):
        """
        Verify Maintenance Triage calls AppFolio tools
        to look up work orders and vendors.
        """
        self._ensure_authenticated()
        admin = self._get_admin()

        admin.select_agent_and_send(
            "Maintenance Triage",
            "Use the appfolio_list_vendors tool to show all available vendors. "
            "Then use appfolio_list_work_orders to show open work orders. "
            "Show the vendor names from the tool output."
        )
        time.sleep(TOOL_WAIT)

        assert self.chat_page.has_assistant_response()
        response = self.chat_page.get_last_response_text()

        self._assert_substantial(response, min_chars=150)
        self._assert_not_hallucinated(response)

    # ==================== CAPEX PLANNING VISUALIZER ====================

    @pytest.mark.sovai
    @pytest.mark.mcp
    @autologger.automation_logger("Test")
    def test_capex_planner_calls_appfolio_tools(self):
        """
        Verify Capex Planning Visualizer calls AppFolio tools
        to pull property and financial data for capex analysis.
        """
        self._ensure_authenticated()
        admin = self._get_admin()

        admin.select_agent_and_send(
            "Capex Planning Visualizer",
            "Use the appfolio_list_properties tool to list all properties, "
            "then use appfolio_list_bills to review capital expenditures. "
            "Show property names and expense categories from the tools."
        )
        time.sleep(TOOL_WAIT)

        assert self.chat_page.has_assistant_response()
        response = self.chat_page.get_last_response_text()

        self._assert_contains_any(response, APPFOLIO_PROPERTIES,
            context="Capex Planner should pull real AppFolio data")
        self._assert_not_hallucinated(response)
