"""
VaultTasks - Task module for key-silk vault workflows.

Tasks compose Command Objects into single domain operations.
They sit between Command Objects (1 CLI command each) and Roles
(full multi-step business workflows).

Rules (mirrors browser Task conventions):
- No @autologger decorator on the constructor
- @autologger("Task") on every method
- Composes VaultCommands, never CliInterface directly
- One logical domain operation per method
- Returns meaningful data (dicts/strings) so Roles can chain
- NO assertions — assertions live in tests
"""

from commands.key_silk.vault_commands import VaultCommands
from interfaces.cli_interface import CliInterface
from resources.utilities import autologger


class VaultTasks:
    """Task module for key-silk vault domain operations."""

    def __init__(self, cli: CliInterface):
        """
        Compose VaultCommands — no decorator on constructor.

        Args:
            cli: CliInterface instance configured for key-silk
        """
        self.vault = VaultCommands(cli)

    # ──────────────────────────────────────────────────────────────────────────
    # Setup / teardown
    # ──────────────────────────────────────────────────────────────────────────

    @autologger.automation_logger("Task")
    def initialise_vault(self, passphrase: str) -> bool:
        """
        Initialise a fresh encrypted-file vault.

        Args:
            passphrase: Master passphrase for the new vault.

        Returns:
            True if the init command succeeded.
        """
        self.vault.init(passphrase)
        return self.vault.succeeded()

    # ──────────────────────────────────────────────────────────────────────────
    # Secret management
    # ──────────────────────────────────────────────────────────────────────────

    @autologger.automation_logger("Task")
    def add_secret(
        self,
        key: str,
        value: str,
        secret_type: str = "api_key",
        group: str = "test",
        description: str = "",
        expires: str = None,
    ) -> bool:
        """
        Add a secret to the vault.

        Returns:
            True if the add command succeeded.
        """
        self.vault.add_secret(
            key=key,
            value=value,
            secret_type=secret_type,
            group=group,
            description=description or None,
            expires=expires,
        )
        return self.vault.succeeded()

    @autologger.automation_logger("Task")
    def remove_secret(self, key: str) -> bool:
        """
        Remove a secret from the vault.

        Returns:
            True if the remove command succeeded.
        """
        self.vault.remove_secret(key)
        return self.vault.succeeded()

    @autologger.automation_logger("Task")
    def rotate_secret(self, key: str, new_value: str) -> bool:
        """
        Rotate (update the value of) an existing secret.

        Returns:
            True if the rotate command succeeded.
        """
        self.vault.rotate_secret(key, new_value)
        return self.vault.succeeded()

    # ──────────────────────────────────────────────────────────────────────────
    # Read operations
    # ──────────────────────────────────────────────────────────────────────────

    @autologger.automation_logger("Task")
    def list_groups(self) -> str:
        """
        Retrieve the formatted list of all secret groups.

        Returns:
            Raw stdout string from `key-silk groups`.
        """
        self.vault.list_groups()
        return self.vault.stdout()

    @autologger.automation_logger("Task")
    def list_secrets(self, group: str = None) -> str:
        """
        Retrieve the formatted list of secret metadata.

        Returns:
            Raw stdout string from `key-silk list`.
        """
        self.vault.list_secrets(group=group)
        return self.vault.stdout()

    @autologger.automation_logger("Task")
    def secret_is_listed(self, key: str, group: str = None) -> bool:
        """
        Return True if the given key appears in the vault listing.

        Args:
            key:   Secret key to look for.
            group: Optional group filter.
        """
        self.vault.list_secrets(group=group)
        return key in self.vault.stdout()

    @autologger.automation_logger("Task")
    def vault_is_empty(self) -> bool:
        """Return True if the vault contains no secrets."""
        self.vault.list_secrets()
        return "No secrets found" in self.vault.stdout()

    @autologger.automation_logger("Task")
    def get_expiring_output(self, days: int = 7) -> str:
        """
        Return the raw stdout of `key-silk expiring`.

        Args:
            days: Look-ahead window in days.
        """
        self.vault.expiring(days=days)
        return self.vault.stdout()

    @autologger.automation_logger("Task")
    def get_audit_output(
        self,
        key: str = None,
        action: str = None,
        limit: int = 50,
    ) -> str:
        """
        Return the raw stdout of `key-silk audit`.

        Args:
            key:    Filter to a specific secret key.
            action: Filter to a specific action type.
            limit:  Maximum entries to return.
        """
        self.vault.audit(key=key, action=action, limit=limit)
        return self.vault.stdout()

    @autologger.automation_logger("Task")
    def inject_secrets_to_env(
        self,
        group: str,
        target_path: str,
        overwrite: bool = True,
        template: str = None,
    ) -> bool:
        """
        Inject secrets from the given group into a .env file.

        Args:
            group:       Secret group to inject.
            target_path: Absolute path of the .env file to write.
            overwrite:   If True, overwrite existing keys in the file.
            template:    Optional template name to use as the file base.

        Returns:
            True if the inject command succeeded.
        """
        self.vault.inject_secrets(
            group=group, target=target_path, overwrite=overwrite, template=template
        )
        return self.vault.succeeded()

    @autologger.automation_logger("Task")
    def env_file_contains_key(self, env_path: str, key: str) -> bool:
        """
        Read a .env file and return True if it contains the given key.

        Args:
            env_path: Path to the .env file.
            key:      Secret key to look for (e.g. 'ANTHROPIC_API_KEY').
        """
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                contents = f.read()
            return key in contents
        except FileNotFoundError:
            return False

    @autologger.automation_logger("Task")
    def env_file_entry_has_value(self, env_path: str, key: str, value: str) -> bool:
        """
        Return True if the .env file contains KEY="value" (quoted form).

        key-silk always writes values in double-quoted form: KEY="value".
        Double quotes within the value are escaped as \\".

        Args:
            env_path: Path to the .env file.
            key:      Secret key (e.g. 'API_KEY').
            value:    Expected plaintext value (unescaped).
        """
        escaped = value.replace('"', '\\"')
        expected_line = f'{key}="{escaped}"'
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                contents = f.read()
            return expected_line in contents
        except FileNotFoundError:
            return False

    @autologger.automation_logger("Task")
    def audit_contains_action(
        self, key: str, action: str, limit: int = 50
    ) -> bool:
        """
        Return True if the audit log contains the given action for a key.

        Args:
            key:    Secret key to look for.
            action: Action string, e.g. 'add', 'remove', 'rotate'.
            limit:  Maximum audit entries to scan.
        """
        output = self.get_audit_output(key=key, action=action, limit=limit)
        return key in output and action in output
