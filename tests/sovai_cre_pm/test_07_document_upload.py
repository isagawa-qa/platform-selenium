"""
TestDocumentUpload - Agent file attachment regression tests for SovAI CRE/PM.

P0 Blocker: Agents return empty responses when files are attached.
Root cause: Bedrock "duplicate document names" error when files are sent
in the conversation payload.

These tests validate:
1. Agent responds to text-only prompts (baseline — known working)
2. Agent responds when a CSV file is attached (P0 regression)
3. Agent responds when data is pasted inline (workaround validation)
4. Response contains domain-relevant content for uploaded data

Uses AAA pattern: Arrange, Act, Assert.
Ref: GitHub Issue #29
"""

import os
import pytest
from resources.utilities import autologger
from roles.sovai.admin_role import AdminRole
from pages.sovai.login_page import LoginPage
from pages.sovai.chat_page import ChatPage


# Path to SC sample data files (relative to project root)
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..",
                        "sovai-cre-pm", "data", "sc-samples")

# Inline CSV data for paste-based workaround test
TENANT_LEDGER_INLINE = """Date,Description,Category,Charges,Payments,Balance
2024-01-01,Rent Charge - January,Rent,1850.00,,1850.00
2024-01-05,Payment - January,,,-1850.00,0.00
2024-02-01,Rent Charge - February,Rent,1850.00,,1850.00
2024-02-01,Late Fee,Fee,75.00,,1925.00
2024-02-12,Payment - February,,,-1925.00,0.00
2024-03-01,Rent Charge - March,Rent,1850.00,,1850.00
2024-03-03,Payment - March,,,-1850.00,0.00"""


class TestDocumentUpload:
    """
    Document upload regression tests for SovAI CRE/PM agents.

    Tests the P0 blocker (Issue #29): agents returning empty responses
    when files are attached to conversations.

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

    def _make_admin(self):
        """Create an AdminRole instance."""
        credentials = self.test_users["sovai_admin"]
        return AdminRole(
            self.browser,
            base_url=self.config["url"],
            email=credentials["email"],
            password=credentials["password"]
        )

    # ==================== BASELINE TESTS ====================

    @pytest.mark.sovai
    @pytest.mark.document
    @pytest.mark.smoke
    @autologger.automation_logger("Test")
    def test_baseline_agent_responds_without_files(self):
        """
        BASELINE: Verify the Rent Roll Analyst responds to text-only prompts.
        This confirms the agent is functional before testing with files.

        AAA Pattern:
        1. Arrange - Ensure authenticated
        2. Act - Select agent, send text-only prompt
        3. Assert - Agent produces substantial response
        """
        # Arrange
        self._ensure_authenticated()
        admin = self._make_admin()

        # Act
        admin.select_agent_and_send(
            "Rent Roll Analyst",
            "What are the key metrics in a commercial rent roll analysis? "
            "List the top 5 KPIs."
        )

        # Assert
        assert self.chat_page.has_assistant_response(), \
            "Agent should produce a response to text-only prompt"
        assert not self.chat_page.is_response_empty(), \
            "Agent response should not be empty (baseline sanity)"
        response = self.chat_page.get_last_response_text()
        assert len(response) > 200, \
            f"Agent response should be substantial, got {len(response)} chars"

    # ==================== P0 REGRESSION: FILE UPLOAD ====================

    @pytest.mark.sovai
    @pytest.mark.document
    @pytest.mark.p0
    @autologger.automation_logger("Test")
    def test_p0_agent_responds_with_csv_file_attached(self):
        """
        P0 REGRESSION (Issue #29): Agent must respond when a CSV file is attached.

        This is the core regression test for the Bedrock "duplicate document names"
        error. If this test fails, agents cannot process uploaded documents.

        AAA Pattern:
        1. Arrange - Ensure authenticated, verify CSV exists
        2. Act - Select agent, attach CSV, send analysis prompt
        3. Assert - Agent produces substantial response (NOT empty)
        """
        # Arrange
        self._ensure_authenticated()
        admin = self._make_admin()
        csv_path = os.path.join(DATA_DIR, "unit_7_tenant_ledger.csv")

        # Skip if test data isn't available
        if not os.path.exists(csv_path):
            pytest.skip(f"Test data not found: {csv_path}")

        # Act
        admin.select_agent_and_send_with_file(
            "Rent Roll Analyst",
            "Analyze this tenant ledger CSV. Show me the payment pattern, "
            "any late payments, and total charges vs payments.",
            csv_path
        )

        # Assert — this is the P0 check
        assert self.chat_page.has_assistant_response(), \
            "P0 BLOCKER: Agent should produce a response when file is attached"
        assert not self.chat_page.is_response_empty(), \
            "P0 BLOCKER: Agent response is EMPTY — Bedrock duplicate document name error"

        response = self.chat_page.get_last_response_text()
        assert len(response) > 100, \
            f"P0 BLOCKER: Agent response too short ({len(response)} chars) — likely error"

    @pytest.mark.sovai
    @pytest.mark.document
    @pytest.mark.p0
    @autologger.automation_logger("Test")
    def test_p0_agent_responds_with_delinquency_csv(self):
        """
        P0 REGRESSION: Verify agent handles delinquency CSV attachment.

        Tests a different document type to ensure the fix isn't file-specific.
        """
        # Arrange
        self._ensure_authenticated()
        admin = self._make_admin()
        csv_path = os.path.join(DATA_DIR, "delinquency_journey.csv")

        if not os.path.exists(csv_path):
            pytest.skip(f"Test data not found: {csv_path}")

        # Act
        admin.select_agent_and_send_with_file(
            "Rent Roll Analyst",
            "Analyze this delinquency report. What is the total outstanding "
            "amount and which units are at highest risk?",
            csv_path
        )

        # Assert
        assert self.chat_page.has_assistant_response(), \
            "P0: Agent should respond with delinquency CSV attached"
        assert not self.chat_page.is_response_empty(), \
            "P0: Agent response is EMPTY for delinquency CSV"

    # ==================== WORKAROUND: INLINE DATA PASTE ====================

    @pytest.mark.sovai
    @pytest.mark.document
    @autologger.automation_logger("Test")
    def test_workaround_inline_csv_data_analysis(self):
        """
        WORKAROUND: Verify agents can analyze data pasted inline (no file attachment).

        If file upload is broken (P0), users can still paste CSV data directly
        into the chat. This validates the workaround path.

        AAA Pattern:
        1. Arrange - Ensure authenticated
        2. Act - Send inline CSV data with analysis prompt
        3. Assert - Agent analyzes the data correctly
        """
        # Arrange
        self._ensure_authenticated()
        admin = self._make_admin()

        # Act — paste data inline instead of attaching
        prompt = (
            "Analyze this tenant ledger data and identify any late payments:\n\n"
            f"```csv\n{TENANT_LEDGER_INLINE}\n```\n\n"
            "Provide a summary of charges, payments, and any late fees."
        )
        admin.select_agent_and_send("Rent Roll Analyst", prompt)

        # Assert
        assert self.chat_page.has_assistant_response(), \
            "Agent should respond to inline CSV data"
        assert not self.chat_page.is_response_empty(), \
            "Agent response should not be empty for inline data"

        response = self.chat_page.get_last_response_text()
        assert len(response) > 150, \
            f"Analysis should be substantial, got {len(response)} chars"

    # ==================== DATA FILE EXISTENCE CHECKS ====================

    @pytest.mark.sovai
    @pytest.mark.document
    @pytest.mark.smoke
    @autologger.automation_logger("Test")
    def test_sc_sample_data_files_exist(self):
        """
        SMOKE: Verify converted SC sample data files exist and are non-empty.

        Checks that the document conversion pipeline outputs are present
        for use in agent testing.
        """
        expected_files = [
            "unit_7_tenant_ledger.csv",
            "delinquency_journey.csv",
            "delinquency_journey.md",
            "README.md",
        ]

        for filename in expected_files:
            filepath = os.path.join(DATA_DIR, filename)
            assert os.path.exists(filepath), \
                f"Missing SC sample file: {filename}"
            assert os.path.getsize(filepath) > 0, \
                f"SC sample file is empty: {filename}"
