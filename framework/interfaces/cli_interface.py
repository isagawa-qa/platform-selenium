"""
CliInterface - subprocess + pexpect wrapper for CLI automation.

Parallel to BrowserInterface, but drives a terminal process instead of
a browser. Used to test key-silk (and any future CLI tools) within the
same 5-layer architecture.

Non-interactive commands (list, audit, expiring, etc.) use subprocess.
Interactive commands (init, add, remove, rotate) use pexpect to drive
PTY prompts that enquirer renders inside a pseudo-terminal.

Environment variables set on the instance are forwarded to every
spawned process, so callers set MCP_VAULT_PASSPHRASE / MCP_VAULT_PATH
once and all commands inherit them automatically.
"""

import logging
import os
import subprocess
from typing import Dict, List, Optional

import pexpect


class CliInterface:
    """CLI process driver with logging, environment isolation, and PTY support."""

    DEFAULT_TIMEOUT = 30  # seconds for pexpect waits

    def __init__(
        self,
        binary: str,
        env: Optional[Dict[str, str]] = None,
        timeout: int = DEFAULT_TIMEOUT,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize CliInterface.

        Args:
            binary:  Path to (or name of) the CLI binary, e.g.
                     'key-silk' or '/path/to/dist/index.js'.
                     If the path ends in '.js', commands are prefixed
                     with 'node' automatically.
            env:     Extra environment variables merged over os.environ.
                     Pass MCP_VAULT_PASSPHRASE, MCP_VAULT_PATH, etc. here.
            timeout: Default pexpect timeout in seconds.
            logger:  Optional logger; a default one is created if omitted.
        """
        self.binary = binary
        self.timeout = timeout
        self.logger = logger or logging.getLogger(self.__class__.__name__)

        # Build merged environment: inherit current env, then overlay extras.
        self.env = dict(os.environ)
        if env:
            self.env.update(env)

        # If the binary is a .js file we need to invoke it via node.
        self._use_node = binary.endswith('.js')

    # ──────────────────────────────────────────────────────────────────────────
    # Non-interactive (subprocess)
    # ──────────────────────────────────────────────────────────────────────────

    def run(self, *args: str) -> Dict:
        """
        Run a CLI command non-interactively via subprocess.

        Returns a dict with keys: stdout, stderr, returncode.

        Args:
            *args: CLI sub-command and flags, e.g. 'list', '--group', 'backend'.
        """
        cmd = self._build_cmd(*args)
        self.logger.info(f"[CLI] run: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=self.env,
        )

        self.logger.debug(f"[CLI] stdout: {result.stdout.strip()}")
        if result.stderr.strip():
            self.logger.debug(f"[CLI] stderr: {result.stderr.strip()}")
        self.logger.info(f"[CLI] exit: {result.returncode}")

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }

    # ──────────────────────────────────────────────────────────────────────────
    # Interactive (pexpect / PTY)
    # ──────────────────────────────────────────────────────────────────────────

    def run_interactive(
        self,
        args: List[str],
        interactions: List[Dict],
        timeout: Optional[int] = None,
    ) -> Dict:
        """
        Run a CLI command that requires PTY prompts, driven by pexpect.

        Args:
            args:         CLI sub-command and flags as a list.
            interactions: Ordered list of {expect, send} dicts.
                          'expect' is a string/regex pexpect will wait for.
                          'send'   is the text to type (newline appended).
                          Use expect=pexpect.EOF to just wait for the process
                          to finish without sending anything.
            timeout:      Override the instance default timeout.

        Returns:
            Dict with keys: output (full captured text), returncode.

        Example interactions for `key-silk add MY_KEY -t api_key`:
            [
                {"expect": "Enter value for MY_KEY", "send": "s3cret"},
                {"expect": pexpect.EOF},
            ]
        """
        t = timeout if timeout is not None else self.timeout
        cmd = self._build_cmd(*args)
        self.logger.info(f"[CLI] run_interactive: {' '.join(cmd)}")

        child = pexpect.spawn(
            cmd[0],
            args=cmd[1:],
            env=self.env,
            encoding="utf-8",
            timeout=t,
        )

        output_parts = []
        try:
            for step in interactions:
                expect_val = step["expect"]
                send_val = step.get("send")

                if expect_val is pexpect.EOF:
                    child.expect(pexpect.EOF)
                    output_parts.append(child.before or "")
                else:
                    child.expect(expect_val)
                    output_parts.append(child.before or "")
                    output_parts.append(child.after or "")
                    if send_val is not None:
                        child.sendline(send_val)

            child.wait()
        except pexpect.TIMEOUT:
            self.logger.error(f"[CLI] pexpect TIMEOUT after {t}s")
            child.terminate(force=True)
            raise
        except pexpect.EOF:
            # Process exited before expected — capture remaining output
            output_parts.append(child.before or "")

        output = "".join(output_parts)
        returncode = child.exitstatus if child.exitstatus is not None else -1

        self.logger.debug(f"[CLI] output: {output.strip()}")
        self.logger.info(f"[CLI] exit: {returncode}")

        return {"output": output, "returncode": returncode}

    # ──────────────────────────────────────────────────────────────────────────
    # Internal helpers
    # ──────────────────────────────────────────────────────────────────────────

    def _build_cmd(self, *args: str) -> List[str]:
        """Construct the full command list, prepending 'node' when needed."""
        base = ["node", self.binary] if self._use_node else [self.binary]
        return base + list(args)
