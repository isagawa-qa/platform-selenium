"""
VaultCommands - Command Object for key-silk vault operations.

The Command Object is the CLI equivalent of a Page Object:
each method maps 1-to-1 with one key-silk CLI command.

Rules (mirrors Page Object conventions):
- No @autologger decorator on the constructor
- Each method stores its raw result in self._last_result
- Methods return self for optional fluent chaining
- NO assertions — assertions live in tests
- NO multi-step workflows — workflows live in Tasks

Interactive commands (init, add, remove, rotate) use run_interactive()
because enquirer renders prompts inside a PTY.

Non-interactive commands (list, groups, expiring, audit, templates)
use run(), which bypasses the PTY entirely. The passphrase for these
commands must be supplied via the MCP_VAULT_PASSPHRASE env var (set on
the CliInterface instance's env dict).
"""

import pexpect
from typing import Optional

from interfaces.cli_interface import CliInterface


class VaultCommands:
    """Command Objects for key-silk vault CLI."""

    def __init__(self, cli: CliInterface):
        """
        Compose CliInterface — no decorator on constructor.

        Args:
            cli: CliInterface instance configured for key-silk
        """
        self.cli = cli
        self._last_result: Optional[dict] = None

    # ──────────────────────────────────────────────────────────────────────────
    # Non-interactive commands (subprocess)
    # ──────────────────────────────────────────────────────────────────────────

    def list_secrets(self, group: Optional[str] = None) -> "VaultCommands":
        """
        Run `key-silk list [--group GROUP]`.

        Requires MCP_VAULT_PASSPHRASE in cli.env.
        """
        args = ["list"]
        if group:
            args += ["--group", group]
        self._last_result = self.cli.run(*args)
        return self

    def list_groups(self) -> "VaultCommands":
        """Run `key-silk groups`."""
        self._last_result = self.cli.run("groups")
        return self

    def expiring(self, days: int = 7) -> "VaultCommands":
        """Run `key-silk expiring --days DAYS`."""
        self._last_result = self.cli.run("expiring", "--days", str(days))
        return self

    def audit(
        self,
        key: Optional[str] = None,
        action: Optional[str] = None,
        since: Optional[str] = None,
        limit: int = 50,
    ) -> "VaultCommands":
        """Run `key-silk audit` with optional filters."""
        args = ["audit", "--limit", str(limit)]
        if key:
            args += ["--key", key]
        if action:
            args += ["--action", action]
        if since:
            args += ["--since", since]
        self._last_result = self.cli.run(*args)
        return self

    def templates(self) -> "VaultCommands":
        """Run `key-silk templates`."""
        self._last_result = self.cli.run("templates")
        return self

    # ──────────────────────────────────────────────────────────────────────────
    # Interactive commands (pexpect / PTY)
    # ──────────────────────────────────────────────────────────────────────────

    def init(self, passphrase: str) -> "VaultCommands":
        """
        Run `key-silk init` and supply the master passphrase via PTY.

        Note: init does NOT respect MCP_VAULT_PASSPHRASE — it always
        prompts interactively — so we must use run_interactive here.
        """
        self._last_result = self.cli.run_interactive(
            args=["init"],
            interactions=[
                {"expect": "passphrase",   "send": passphrase},
                {"expect": pexpect.EOF},
            ],
        )
        return self

    def add_secret(
        self,
        key: str,
        value: str,
        secret_type: str = "api_key",
        group: Optional[str] = None,
        description: Optional[str] = None,
        expires: Optional[str] = None,
    ) -> "VaultCommands":
        """
        Run `key-silk add KEY` and supply the secret value via PTY.

        The vault passphrase is handled automatically via MCP_VAULT_PASSPHRASE.
        This method only needs to supply the 'value' prompt.
        """
        args = ["add", key, "--type", secret_type]
        if group:
            args += ["--group", group]
        if description:
            args += ["--description", description]
        if expires:
            args += ["--expires", expires]

        self._last_result = self.cli.run_interactive(
            args=args,
            interactions=[
                {"expect": f"Enter value for {key}", "send": value},
                {"expect": pexpect.EOF},
            ],
        )
        return self

    def remove_secret(self, key: str) -> "VaultCommands":
        """
        Run `key-silk remove KEY` and confirm the deletion via PTY.

        The vault passphrase is handled automatically via MCP_VAULT_PASSPHRASE.
        """
        self._last_result = self.cli.run_interactive(
            args=["remove", key],
            interactions=[
                {"expect": f'Remove secret "{key}"', "send": "y"},
                {"expect": pexpect.EOF},
            ],
        )
        return self

    def rotate_secret(self, key: str, new_value: str) -> "VaultCommands":
        """
        Run `key-silk rotate KEY` and supply the new value via PTY.

        The vault passphrase is handled automatically via MCP_VAULT_PASSPHRASE.
        """
        self._last_result = self.cli.run_interactive(
            args=["rotate", key],
            interactions=[
                {"expect": f"Enter new value for {key}", "send": new_value},
                {"expect": pexpect.EOF},
            ],
        )
        return self

    def inject_secrets(
        self,
        group: str,
        target: str,
        template: Optional[str] = None,
        overwrite: bool = True,
    ) -> "VaultCommands":
        """
        Run `key-silk inject --group GROUP --target TARGET`.

        Non-interactive: passphrase comes from MCP_VAULT_PASSPHRASE env var.
        The target path is the .env file that should be written.
        """
        args = ["inject", "--group", group, "--target", target]
        if template:
            args += ["--template", template]
        if overwrite:
            args += ["--overwrite"]
        self._last_result = self.cli.run(*args)
        return self

    # ──────────────────────────────────────────────────────────────────────────
    # Result accessors (used by Tasks for assertions)
    # ──────────────────────────────────────────────────────────────────────────

    def succeeded(self) -> bool:
        """Return True if the last command exited with code 0."""
        if self._last_result is None:
            return False
        return self._last_result.get("returncode", -1) == 0

    def stdout(self) -> str:
        """Return stdout of the last non-interactive command."""
        if self._last_result is None:
            return ""
        return self._last_result.get("stdout", "")

    def output(self) -> str:
        """Return captured PTY output of the last interactive command."""
        if self._last_result is None:
            return ""
        return self._last_result.get("output", "")

    def contains(self, text: str) -> bool:
        """Return True if stdout OR PTY output contains the given text."""
        combined = self.stdout() + self.output()
        return text in combined
