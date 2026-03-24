"""
Pytest fixtures for key-silk CLI integration tests.

Session-scoped vault
--------------------
A single encrypted vault is created once per pytest session inside a
temporary directory. All tests in this suite share it. Individual tests
are responsible for cleaning up any secrets they add (or they should add
uniquely-named keys to avoid collision).

Environment isolation
---------------------
MCP_VAULT_PATH and MCP_AUDIT_LOG_PATH are pointed at the temp dir so
tests never touch the developer's real vault at ~/.mcp-secrets.

MCP_VAULT_PASSPHRASE is set so non-interactive commands (list, audit,
expiring, inject) don't prompt for the passphrase.

Binary resolution
-----------------
The key-silk binary is resolved from the KEY_SILK_BINARY env var if set,
otherwise it defaults to the dist/index.js path relative to this repo.

Usage in tests:
    def test_something(cli, vault_tasks, developer, tmp_env_dir):
        ...
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

import pytest

# ── Path setup ──────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent.parent.parent
FRAMEWORK_PATH = str(PROJECT_ROOT / "framework")
if FRAMEWORK_PATH not in sys.path:
    sys.path.insert(0, FRAMEWORK_PATH)

# key-silk repo is expected to be a sibling of platform-selenium.
# Override with KEY_SILK_BINARY env var if needed.
_DEFAULT_KEY_SILK_BINARY = str(
    PROJECT_ROOT.parent / "key-silk" / "dist" / "index.js"
)

from interfaces.cli_interface import CliInterface
from tasks.key_silk.vault_tasks import VaultTasks
from roles.key_silk.developer_role import DeveloperRole

# ── Constants ────────────────────────────────────────────────────────────────

TEST_PASSPHRASE = "test-passphrase-do-not-use-in-prod"


# ── Session fixtures ─────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def vault_dir():
    """
    Create an isolated temp directory for the test vault.
    Cleaned up after the entire session completes.
    """
    tmp = tempfile.mkdtemp(prefix="key_silk_test_")
    yield tmp
    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture(scope="session")
def cli(vault_dir):
    """
    CliInterface configured for key-silk with the test vault and passphrase.

    Environment variables set here are forwarded to every subprocess and
    pexpect spawn, so individual tests don't need to worry about them.
    """
    binary = os.environ.get("KEY_SILK_BINARY", _DEFAULT_KEY_SILK_BINARY)

    env = {
        "MCP_VAULT_PASSPHRASE": TEST_PASSPHRASE,
        "MCP_VAULT_PATH":       os.path.join(vault_dir, "vault.enc"),
        "MCP_AUDIT_LOG_PATH":   os.path.join(vault_dir, "audit.log"),
    }

    interface = CliInterface(binary=binary, env=env)

    # Initialise the vault once for the whole session.
    from commands.key_silk.vault_commands import VaultCommands
    VaultCommands(interface).init(TEST_PASSPHRASE)

    yield interface


@pytest.fixture(scope="session")
def vault_tasks(cli):
    """Session-scoped VaultTasks bound to the test vault."""
    yield VaultTasks(cli)


@pytest.fixture(scope="session")
def developer(cli):
    """Session-scoped DeveloperRole bound to the test vault."""
    yield DeveloperRole(cli)


# ── Function-scoped helpers ──────────────────────────────────────────────────

@pytest.fixture()
def tmp_env_dir():
    """
    Provide (and clean up) a temporary directory for .env file injection tests.
    Fresh per test function.
    """
    tmp = tempfile.mkdtemp(prefix="key_silk_env_")
    yield tmp
    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture()
def tmp_template_dir():
    """
    Provide (and clean up) a temporary directory for template files.
    Fresh per test function.
    """
    tmp = tempfile.mkdtemp(prefix="key_silk_tmpl_")
    yield tmp
    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture()
def template_vault_tasks(vault_dir, tmp_template_dir):
    """
    Function-scoped VaultTasks whose CliInterface has MCP_TEMPLATE_DIR set
    to a fresh temp directory.  The test is responsible for writing template
    files into that directory before calling inject.
    """
    binary = os.environ.get("KEY_SILK_BINARY", _DEFAULT_KEY_SILK_BINARY)
    env = {
        "MCP_VAULT_PASSPHRASE": TEST_PASSPHRASE,
        "MCP_VAULT_PATH":       os.path.join(vault_dir, "vault.enc"),
        "MCP_AUDIT_LOG_PATH":   os.path.join(vault_dir, "audit.log"),
        "MCP_TEMPLATE_DIR":     tmp_template_dir,
    }
    interface = CliInterface(binary=binary, env=env)
    yield VaultTasks(interface), tmp_template_dir
