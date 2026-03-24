"""
TestVaultLifecycle

Integration tests for the key-silk CLI via the CliInterface + 5-layer
platform-selenium architecture.

Each test follows the Arrange / Act / Assert pattern.
Tests share a session-scoped vault (created once by conftest.py).
Secret keys are unique per test to avoid cross-test state collisions.

Coverage:
  1. Empty vault reports 'No secrets found'
  2. Adding a secret succeeds and the key appears in the listing
  3. Removing a secret succeeds and the key disappears from the listing
  4. Rotating a secret succeeds
  5. inject writes secrets into a .env file
  6. Audit log records 'add' and 'remove' events for a secret
  7. Expiring command flags a secret whose expiry date is in the past
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
from roles.key_silk.developer_role import DeveloperRole
from tasks.key_silk.vault_tasks import VaultTasks


class TestVaultLifecycle:

    @pytest.fixture(autouse=True)
    def setup(self, developer, vault_tasks, tmp_env_dir):
        self.developer:   DeveloperRole = developer
        self.vault:       VaultTasks    = vault_tasks
        self.tmp_env_dir: str           = tmp_env_dir

    # ──────────────────────────────────────────────────────────────────────────
    # 1. Empty vault
    # ──────────────────────────────────────────────────────────────────────────

    @pytest.mark.key_silk
    @autologger.automation_logger("Test")
    def test_empty_vault_reports_no_secrets(self):
        """
        As a developer, when the vault is empty I should see 'No secrets found'
        so that I know the vault is clean.
        """
        # ── Arrange ──────────────────────────────────────────────────────────
        # Vault is initialised empty by the session fixture.

        # ── Act ───────────────────────────────────────────────────────────────
        output = self.vault.list_secrets()

        # ── Assert ────────────────────────────────────────────────────────────
        assert "No secrets found" in output, (
            f"Expected 'No secrets found' in empty vault output, got:\n{output}"
        )

    # ──────────────────────────────────────────────────────────────────────────
    # 2. Add a secret
    # ──────────────────────────────────────────────────────────────────────────

    @pytest.mark.key_silk
    @autologger.automation_logger("Test")
    def test_add_secret_appears_in_listing(self):
        """
        As a developer, after adding a secret I should see it in the vault list
        so that I can confirm it was stored.
        """
        # ── Arrange ──────────────────────────────────────────────────────────
        key   = "TEST_ADD_KEY"
        value = "super-secret-value"

        # ── Act ───────────────────────────────────────────────────────────────
        self.developer.store_and_verify_secret(
            key=key, value=value, secret_type="api_key", group="ci"
        )

        # ── Assert ────────────────────────────────────────────────────────────
        assert self.vault.secret_is_listed(key), (
            f"Expected '{key}' to appear in the vault listing after add."
        )

        # Cleanup
        self.vault.remove_secret(key)

    # ──────────────────────────────────────────────────────────────────────────
    # 3. Remove a secret
    # ──────────────────────────────────────────────────────────────────────────

    @pytest.mark.key_silk
    @autologger.automation_logger("Test")
    def test_remove_secret_disappears_from_listing(self):
        """
        As a developer, after removing a secret it should no longer appear in
        the vault list so that I can confirm it was deleted.
        """
        # ── Arrange ──────────────────────────────────────────────────────────
        key = "TEST_REMOVE_KEY"
        self.vault.add_secret(key=key, value="temp-value", group="ci")

        # Pre-condition: key must be present before we remove it
        assert self.vault.secret_is_listed(key), (
            f"Pre-condition failed: '{key}' should exist before removal."
        )

        # ── Act ───────────────────────────────────────────────────────────────
        self.developer.remove_and_verify_gone(key)

        # ── Assert ────────────────────────────────────────────────────────────
        assert not self.vault.secret_is_listed(key), (
            f"Expected '{key}' to be absent from the vault listing after remove."
        )

    # ──────────────────────────────────────────────────────────────────────────
    # 4. Rotate a secret
    # ──────────────────────────────────────────────────────────────────────────

    @pytest.mark.key_silk
    @autologger.automation_logger("Test")
    def test_rotate_secret_succeeds(self):
        """
        As a developer, rotating a secret should succeed and the key should
        remain listed so that I can confirm the rotation was applied.
        """
        # ── Arrange ──────────────────────────────────────────────────────────
        key = "TEST_ROTATE_KEY"
        self.vault.add_secret(key=key, value="original-value", group="ci")

        # ── Act ───────────────────────────────────────────────────────────────
        rotated = self.vault.rotate_secret(key=key, new_value="rotated-value")

        # ── Assert ────────────────────────────────────────────────────────────
        assert rotated, f"Expected rotate to succeed for '{key}'."
        assert self.vault.secret_is_listed(key), (
            f"Expected '{key}' to remain in the vault after rotation."
        )

        # Cleanup
        self.vault.remove_secret(key)

    # ──────────────────────────────────────────────────────────────────────────
    # 5. Inject secrets into a .env file
    # ──────────────────────────────────────────────────────────────────────────

    @pytest.mark.key_silk
    @autologger.automation_logger("Test")
    def test_inject_writes_secret_to_env_file(self):
        """
        As a developer, injecting a group of secrets into a .env file should
        produce a file that contains the expected key so that the application
        can load it at runtime.
        """
        # ── Arrange ──────────────────────────────────────────────────────────
        key           = "TEST_INJECT_KEY"
        secret_value  = "injected-value-xyz-789"
        group         = "inject-test"
        target_env    = os.path.join(self.tmp_env_dir, ".env")

        self.vault.add_secret(key=key, value=secret_value, group=group)

        # ── Act ───────────────────────────────────────────────────────────────
        self.developer.inject_group_to_env_file(
            group=group, target_path=target_env
        )

        # ── Assert ────────────────────────────────────────────────────────────
        assert os.path.exists(target_env), (
            f"Expected .env file to be created at {target_env}."
        )

        # 1. Key name appears
        assert self.vault.env_file_contains_key(target_env, key), (
            f"Expected '{key}' to appear in {target_env} after inject."
        )

        # 2. Correct value is written (KEY="value" form) — catches wrong-value bugs
        assert self.vault.env_file_entry_has_value(target_env, key, secret_value), (
            f"Expected {key}=\"{secret_value}\" in {target_env}. "
            f"Possible inject bug: value mismatch."
        )

        # Cleanup
        self.vault.remove_secret(key)

    # ──────────────────────────────────────────────────────────────────────────
    # 6. Audit log
    # ──────────────────────────────────────────────────────────────────────────

    @pytest.mark.key_silk
    @autologger.automation_logger("Test")
    def test_audit_log_records_add_and_remove(self):
        """
        As a developer, the audit log should record both 'add' and 'remove'
        events for a secret so that I have a tamper-evident trail.
        """
        # ── Arrange ──────────────────────────────────────────────────────────
        key = "TEST_AUDIT_KEY"
        self.vault.add_secret(key=key, value="audit-value", group="ci")

        # ── Act ───────────────────────────────────────────────────────────────
        self.vault.remove_secret(key)
        self.developer.review_audit_trail(key)

        # ── Assert ────────────────────────────────────────────────────────────
        assert self.vault.audit_contains_action(key=key, action="add"), (
            f"Expected 'add' event for '{key}' in audit log."
        )
        assert self.vault.audit_contains_action(key=key, action="remove"), (
            f"Expected 'remove' event for '{key}' in audit log."
        )

    # ──────────────────────────────────────────────────────────────────────────
    # 7. Expiration warning
    # ──────────────────────────────────────────────────────────────────────────

    @pytest.mark.key_silk
    @autologger.automation_logger("Test")
    def test_expiring_flags_past_expiry_secret(self):
        """
        As a developer, a secret whose expiry date is in the past should be
        flagged by `key-silk expiring` so that I know to rotate it.
        """
        # ── Arrange ──────────────────────────────────────────────────────────
        key = "TEST_EXPIRED_KEY"
        past_date = "2020-01-01T00:00:00Z"  # well in the past

        self.vault.add_secret(
            key=key,
            value="expired-value",
            group="ci",
            expires=past_date,
        )

        # ── Act ───────────────────────────────────────────────────────────────
        # Look-ahead of 1 day — an already-expired secret should always appear.
        output = self.vault.get_expiring_output(days=1)

        # ── Assert ────────────────────────────────────────────────────────────
        assert key in output, (
            f"Expected '{key}' to appear in expiring output. Got:\n{output}"
        )
        assert "EXPIRED" in output, (
            f"Expected 'EXPIRED' status in expiring output. Got:\n{output}"
        )

        # Cleanup
        self.vault.remove_secret(key)

    # ──────────────────────────────────────────────────────────────────────────
    # 8. Group filtering
    # ──────────────────────────────────────────────────────────────────────────

    @pytest.mark.key_silk
    @autologger.automation_logger("Test")
    def test_list_filtered_by_group_returns_only_matching_secrets(self):
        """
        As a developer, `key-silk list --group GROUP` should return only
        secrets tagged with that group so that inject targeting a specific
        group delivers exactly the right secrets.
        """
        # ── Arrange ──────────────────────────────────────────────────────────
        key_a, key_b = "TEST_FILTER_A_KEY", "TEST_FILTER_B_KEY"
        self.vault.add_secret(key=key_a, value="val-a", group="grp-alpha")
        self.vault.add_secret(key=key_b, value="val-b", group="grp-beta")

        # ── Act ───────────────────────────────────────────────────────────────
        output_alpha = self.vault.list_secrets(group="grp-alpha")
        output_beta  = self.vault.list_secrets(group="grp-beta")

        # ── Assert ────────────────────────────────────────────────────────────
        assert key_a in output_alpha, (
            f"Expected '{key_a}' in grp-alpha listing. Got:\n{output_alpha}"
        )
        assert key_b not in output_alpha, (
            f"'{key_b}' (grp-beta) should NOT appear in grp-alpha listing."
        )
        assert key_b in output_beta, (
            f"Expected '{key_b}' in grp-beta listing. Got:\n{output_beta}"
        )
        assert key_a not in output_beta, (
            f"'{key_a}' (grp-alpha) should NOT appear in grp-beta listing."
        )

        # Cleanup
        self.vault.remove_secret(key_a)
        self.vault.remove_secret(key_b)

    # ──────────────────────────────────────────────────────────────────────────
    # 9. inject --overwrite
    # ──────────────────────────────────────────────────────────────────────────

    @pytest.mark.key_silk
    @autologger.automation_logger("Test")
    def test_inject_overwrite_replaces_existing_key(self):
        """
        As a developer, injecting with --overwrite should replace a key that
        already exists in the .env file so that stale values are never left
        behind.
        """
        # ── Arrange ──────────────────────────────────────────────────────────
        key          = "TEST_OVERWRITE_KEY"
        old_value    = "old-stale-value"
        new_value    = "new-fresh-value"
        group        = "overwrite-test"
        target_env   = os.path.join(self.tmp_env_dir, ".env")

        # Pre-populate the .env file with the old (stale) value.
        with open(target_env, "w", encoding="utf-8") as f:
            f.write(f'{key}="{old_value}"\n')

        # Add the secret to the vault with the new value.
        self.vault.add_secret(key=key, value=new_value, group=group)

        # ── Act ───────────────────────────────────────────────────────────────
        self.vault.inject_secrets_to_env(
            group=group, target_path=target_env, overwrite=True
        )

        # ── Assert ────────────────────────────────────────────────────────────
        assert self.vault.env_file_entry_has_value(target_env, key, new_value), (
            f"Expected {key}=\"{new_value}\" after overwrite inject. "
            f"Old value may still be present."
        )
        assert not self.vault.env_file_entry_has_value(target_env, key, old_value), (
            f"Old value '{old_value}' should have been overwritten but is still present."
        )

        # Cleanup
        self.vault.remove_secret(key)

    # ──────────────────────────────────────────────────────────────────────────
    # 10. inject --template
    # ──────────────────────────────────────────────────────────────────────────

    @pytest.mark.key_silk
    @autologger.automation_logger("Test")
    def test_inject_with_template_preserves_structure(
        self, template_vault_tasks
    ):
        """
        As a developer, injecting with --template should use the template file
        as the base of the .env so that static config values and comments in
        the template are preserved alongside the injected secrets.
        """
        # ── Arrange ──────────────────────────────────────────────────────────
        tmpl_vault, tmpl_dir = template_vault_tasks

        key           = "TEST_TMPL_KEY"
        secret_value  = "tmpl-injected-val"
        group         = "tmpl-test"
        target_env    = os.path.join(self.tmp_env_dir, ".env")
        template_name = "ci-service"

        # Write a template file into the temp template directory.
        tmpl_content = (
            "# CI Service configuration\n"
            'STATIC_CONFIG_VAR="hardcoded-constant"\n'
        )
        with open(
            os.path.join(tmpl_dir, f"{template_name}.env.tmpl"),
            "w", encoding="utf-8",
        ) as f:
            f.write(tmpl_content)

        # Add the secret using the session vault (no template needed for add).
        self.vault.add_secret(key=key, value=secret_value, group=group)

        # ── Act ───────────────────────────────────────────────────────────────
        # Use the template-aware VaultTasks so MCP_TEMPLATE_DIR is set.
        tmpl_vault.inject_secrets_to_env(
            group=group, target_path=target_env, template=template_name
        )

        # ── Assert ────────────────────────────────────────────────────────────
        assert os.path.exists(target_env), (
            f"Expected .env file to be created at {target_env}."
        )
        assert self.vault.env_file_contains_key(target_env, "STATIC_CONFIG_VAR"), (
            "Expected static template variable 'STATIC_CONFIG_VAR' to be "
            "preserved in the output file."
        )
        assert self.vault.env_file_entry_has_value(target_env, key, secret_value), (
            f"Expected {key}=\"{secret_value}\" to be injected from the vault."
        )

        # Cleanup
        self.vault.remove_secret(key)
