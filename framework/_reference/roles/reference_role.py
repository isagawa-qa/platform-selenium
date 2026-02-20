"""
ReferenceRole - Role pattern example for AI to learn from.

Roles represent user personas (e.g., Admin, Customer, Guest).
This role orchestrates complete business workflows using Task modules.
"""

from interfaces.browser_interface import BrowserInterface
from resources.utilities import autologger
from _reference.tasks.reference_tasks import ReferenceTasks


class ReferenceRole:
    """
    ReferenceRole - orchestrates complete business workflows.

    - @autologger("Role") on workflow methods
    - @autologger("Role Constructor") on __init__
    - Composes Task modules
    - Workflow methods call MULTIPLE tasks
    - NO return values
    - NO locators
    - NO credentials required (credential_strategy='none')
    """

    @autologger.automation_logger("Role Constructor")
    def __init__(self, browser_interface: BrowserInterface):
        """
        Initialize and compose Task modules.

        Args:
            browser_interface: BrowserInterface instance

        Note: No credentials required (credential_strategy='none' from Step 1)
        """
        self.browser = browser_interface
        self.reference_tasks = ReferenceTasks(browser_interface)

    # ==================== WORKFLOW METHODS ====================

    @autologger.automation_logger("Role")
    def search_and_create_customer(self, first_name: str, last_name: str, contact_type: str, contact_identifier: str) -> None:
        """
        Execute search and create customer workflow.

        NO return value - test asserts via POM state-check methods.
        """
        self.reference_tasks.search_and_create_customer(first_name, last_name, contact_type, contact_identifier)
        # NO return - test asserts via POM

    @autologger.automation_logger("Role")
    def submit_inquiry(self, inquiry_type: str, source: str, status: str) -> None:
        """
        Execute submit inquiry workflow.

        NO return value - test asserts via POM state-check methods.
        """
        self.reference_tasks.submit_inquiry(inquiry_type, source, status)
        # NO return - test asserts via POM

    @autologger.automation_logger("Role")
    def submit_new_customer_inquiry(
        self,
        first_name: str,
        last_name: str,
        contact_type: str,
        contact_identifier: str,
        inquiry_type: str,
        source: str,
        status: str
    ) -> None:
        """
        Complete workflow: Create customer and submit inquiry.

        This workflow method orchestrates MULTIPLE task operations:
        1. Search/create customer
        2. Submit inquiry

        NO return value - test asserts via POM state-check methods.
        """
        self.reference_tasks.search_and_create_customer(first_name, last_name, contact_type, contact_identifier)
        self.reference_tasks.submit_inquiry(inquiry_type, source, status)
        # NO return - test asserts via POM
