"""
TestInitRegression

Regression tests for the `key-silk init` command.

Bug history:
    src/index.ts originally called `defaultConfig()` inside the `init` action,
    which ignores MCP_VAULT_PATH and always initialises the vault at the
    hardcoded default (~/.mcp-secrets/vault.enc).

    The fix changed `defaultConfig()` to `await loadConfig()` so environment-
    variable overrides are respected.

    Without this fix, `init` would either:
      - Fail on machines that already have a real vault (wrong-passphrase error)
      - Silently clobber the real vault on a fresh machine

These tests create fully isolated vaults to avoid touching the developer's
real ~/.mcp-secrets directory.
"""

import os
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).parent.parent.parent
FRAMEWORK_PATH = str(PROJECT_ROOT / "framework")
if FRAMEWORK_PATH not in sys.path:
    sys.path.insert(0, FRAMEWORK_PATH)

from resources.utilities import autologger
from interfaces.cli_interface import CliInterface
from commands.key_silk.vault_commands import VaultCommands

_DEFAULT_KEY_SILK_BINARY = str(
    PROJECT_ROOT.parent / "key-silk" / "dist" / "index.js"
)

TEST_PASSPHRASE = "regression-test-passphrase"


def make_isolated_cli(vault_dir: Path) -> tuple[CliInterface, VaultCommands]:
    """Return a (CliInterface, VaultCommands) pair pointing at vault_dir."""
    binary = os.environ.get("KEY_SILK_BINARY", _DEFAULT_KEY_SILK_BINARY)
    cli = CliInterface(
        binary=binary,
        env={
            "MCP_VAULT_PASSPHRASE": TEST_PASSPHRASE,
            "MCP_VAULT_PATH":       str(vault_dir / "vault.enc"),
            "MCP_AUDIT_LOG_PATH":   str(vault_dir / "audit.log"),
        },
    )
    return cli, VaultCommands(cli)


class TestInitRegression:

    # ──────────────────────────────────────────────────────────────────────────
    # 1. init creates file at MCP_VAULT_PATH
    # ──────────────────────────────────────────────────────────────────────────

    @pytest.mark.key_silk
    @autologger.automation_logger("Test")
    def test_init_creates_vault_at_mcp_vault_path(self, tmp_path):
        """
        `key-silk init` must create the vault file at the path specified by
        MCP_VAULT_PATH, not at the hardcoded default ~/.mcp-secrets/vault.enc.

        Regression: before the fix, init called defaultConfig() which ignores
        MCP_VAULT_PATH.  After the fix it calls loadConfig() which respects it.
        """
        # ── Arrange ──────────────────────────────────────────────────────────
        _cli, cmds = make_isolated_cli(tmp_path)
        expected_path = tmp_path / "vault.enc"

        # ── Act ───────────────────────────────────────────────────────────────
        cmds.init(TEST_PASSPHRASE)

        # ── Assert ────────────────────────────────────────────────────────────
        assert expected_path.exists(), (
            f"Expected vault to be created at MCP_VAULT_PATH={expected_path}. "
            f"File not found — init likely ignored the env var and wrote to the "
            f"default path instead (regression of src/index.ts init bug)."
        )

    # ──────────────────────────────────────────────────────────────────────────
    # 2. vault is usable immediately after init
    # ──────────────────────────────────────────────────────────────────────────

    @pytest.mark.key_silk
    @autologger.automation_logger("Test")
    def test_vault_is_usable_after_init(self, tmp_path):
        """
        A vault created by `init` must be openable with the same passphrase
        and report an empty secret list — confirming the vault was both
        correctly created and correctly encrypted.
        """
        # ── Arrange ──────────────────────────────────────────────────────────
        _cli, cmds = make_isolated_cli(tmp_path)
        cmds.init(TEST_PASSPHRASE)

        # ── Act ───────────────────────────────────────────────────────────────
        cmds.list_secrets()

        # ── Assert ────────────────────────────────────────────────────────────
        assert cmds.succeeded(), (
            f"`key-silk list` failed after init. "
            f"The vault at {tmp_path / 'vault.enc'} may not be valid."
        )
        assert "No secrets found" in cmds.stdout(), (
            f"Expected a freshly initialised vault to report 'No secrets found'. "
            f"Got:\n{cmds.stdout()}"
        )

    # ──────────────────────────────────────────────────────────────────────────
    # 3. two independent vaults don't share state
    # ──────────────────────────────────────────────────────────────────────────

    @pytest.mark.key_silk
    @autologger.automation_logger("Test")
    def test_two_vaults_at_different_paths_are_independent(self, tmp_path):
        """
        Two vaults initialised at different MCP_VAULT_PATH values must be
        independent — a secret added to vault A must not appear in vault B.

        This guards against any path-resolution bug that could cause two
        different MCP_VAULT_PATH values to resolve to the same file.
        """
        # ── Arrange ──────────────────────────────────────────────────────────
        dir_a = tmp_path / "vault_a"
        dir_b = tmp_path / "vault_b"
        dir_a.mkdir()
        dir_b.mkdir()

        _cli_a, cmds_a = make_isolated_cli(dir_a)
        _cli_b, cmds_b = make_isolated_cli(dir_b)

        cmds_a.init(TEST_PASSPHRASE)
        cmds_b.init(TEST_PASSPHRASE)

        # ── Act ───────────────────────────────────────────────────────────────
        # Add a secret to vault A only.
        cmds_a.add_secret(
            key="VAULT_A_ONLY_KEY", value="vault-a-secret", group="test"
        )

        cmds_a.list_secrets()
        cmds_b.list_secrets()

        # ── Assert ────────────────────────────────────────────────────────────
        assert "VAULT_A_ONLY_KEY" in cmds_a.stdout(), (
            "Secret should appear in vault A's listing."
        )
        assert "VAULT_A_ONLY_KEY" not in cmds_b.stdout(), (
            "Secret from vault A must NOT appear in vault B — "
            "the two vaults must be fully independent."
        )
