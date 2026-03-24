"""
DeveloperRole - Role module for key-silk vault workflows.

Represents a Developer persona who manages secrets through the key-silk CLI.
Orchestrates complete business workflows by composing VaultTasks.

Rules (mirrors browser Role conventions):
- @autologger("Role Constructor") on __init__
- @autologger("Role") on every workflow method
- Composes Task modules, never Command Objects or CliInterface directly
- Workflow methods call MULTIPLE tasks
- NO return values — results are observable via VaultTasks accessors
  that tests call directly
"""

from interfaces.cli_interface import CliInterface
from tasks.key_silk.vault_tasks import VaultTasks
from resources.utilities import autologger


class DeveloperRole:
    """Developer persona — orchestrates all key-silk vault workflows."""

    @autologger.automation_logger("Role Constructor")
    def __init__(self, cli: CliInterface):
        """
        Initialize and compose Task modules.

        Args:
            cli: CliInterface configured for key-silk (vault path, passphrase, etc.)
        """
        self.cli = cli
        self.vault_tasks = VaultTasks(cli)

    # ──────────────────────────────────────────────────────────────────────────
    # Workflow methods
    # ──────────────────────────────────────────────────────────────────────────

    @autologger.automation_logger("Role")
    def set_up_fresh_vault(self, passphrase: str) -> None:
        """
        Initialise a brand-new encrypted vault with the given passphrase.

        Workflow:
        1. Run key-silk init and supply the passphrase

        Args:
            passphrase: Master passphrase for the vault.
        """
        self.vault_tasks.initialise_vault(passphrase)

    @autologger.automation_logger("Role")
    def store_and_verify_secret(
        self,
        key: str,
        value: str,
        secret_type: str = "api_key",
        group: str = "test",
    ) -> None:
        """
        Add a secret and confirm it appears in the vault listing.

        Workflow:
        1. Add the secret
        2. List the vault (result is available to the test via vault_tasks)

        Args:
            key:         Secret key name.
            value:       Secret value.
            secret_type: key-silk type string (default: 'api_key').
            group:       Group to assign the secret to.
        """
        self.vault_tasks.add_secret(key=key, value=value, secret_type=secret_type, group=group)
        self.vault_tasks.list_secrets()

    @autologger.automation_logger("Role")
    def remove_and_verify_gone(self, key: str) -> None:
        """
        Remove a secret and confirm it no longer appears in the listing.

        Workflow:
        1. Remove the secret
        2. List the vault (result available to the test)

        Args:
            key: Secret key to remove.
        """
        self.vault_tasks.remove_secret(key)
        self.vault_tasks.list_secrets()

    @autologger.automation_logger("Role")
    def inject_group_to_env_file(
        self, group: str, target_path: str
    ) -> None:
        """
        Inject all secrets from a group into a .env file.

        Workflow:
        1. Run key-silk inject for the given group and target path

        Args:
            group:       Secret group to inject.
            target_path: Absolute path of the .env file to write.
        """
        self.vault_tasks.inject_secrets_to_env(group=group, target_path=target_path)

    @autologger.automation_logger("Role")
    def review_audit_trail(self, key: str) -> None:
        """
        Pull the audit trail for a specific secret key.

        Workflow:
        1. Query the audit log for the given key (result available to the test)

        Args:
            key: Secret key to audit.
        """
        self.vault_tasks.get_audit_output(key=key)
