"""
TestReferenceWorkflow - Test pattern example for AI to learn from.

Test suite for submitting a new customer inquiry through the dealership portal.
Uses AAA pattern: Arrange, Act, Assert.
"""

import pytest
from faker import Faker
from resources.utilities import autologger
from _reference.roles.reference_role import ReferenceRole
from _reference.pages.inquiry_form_page import InquiryFormPage


class TestReferenceWorkflow:
    """
    TestReferenceWorkflow - Test pattern example for AI.

    - @autologger("Test") decorator
    - Call ONE Role workflow method
    - Assert via Page Object state-check methods
    - NO orchestration (Role handles workflow)
    """

    @pytest.fixture(autouse=True)
    def setup(self, browser):
        """Setup test fixtures."""
        self.browser = browser
        self.inquiry_form_page = InquiryFormPage(self.browser)

    # ==================== TEST METHODS ====================

    @pytest.mark.reference
    @autologger.automation_logger("Test")
    def test_submit_new_customer_inquiry(self):
        """
        Test complete workflow: create customer and submit inquiry.

        AAA Pattern:
        1. Arrange - Create role (no credentials needed) + generate unique test data
        2. Act - Call ONE workflow method (no return value)
        3. Assert - Use POM state-check methods
        """
        # Arrange - Generate unique customer data using Faker
        fake = Faker()
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()

        user = ReferenceRole(self.browser)

        # Act - ONE workflow call that orchestrates multiple operations
        user.submit_new_customer_inquiry(
            first_name=first_name,
            last_name=last_name,
            contact_type="Email",
            contact_identifier=email,
            inquiry_type="Service",
            source="Dealership",
            status="New"
        )

        # Assert - Via Page Object state-check methods (NOT return value)
        assert self.inquiry_form_page.is_inquiry_saved(), "Inquiry should be saved successfully"
