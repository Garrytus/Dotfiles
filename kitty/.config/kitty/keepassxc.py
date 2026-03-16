"""Custom made Python wrapper around keepassxc-cli."""

import shutil
import subprocess

from pathlib import Path
from typing import Optional


class KeePassXCNotFoundError(EnvironmentError):
    """Raised when keepassxc-cli is not found in the PATH."""


class KeePassXCError(RuntimeError):
    """Raised when keepassxc-cli returns an error."""


class KeePassXC:
    """Wrapper around keepassxc-cli."""

    def __init__(
        self,
        database: str,
        *,
        key_file: Optional[str] = None,
    ):
        """Initialize Keepassxc."""
        self.database = Path(database).expanduser()
        self.key_file = Path(key_file).expanduser() if key_file else None

        keepassxc_cli_path = shutil.which("keepassxc-cli")
        if not keepassxc_cli_path:
            raise KeePassXCNotFoundError(
                "keepassxc-cli not installed or not in the PATH."
            )
        self.cli_path = keepassxc_cli_path

    def _run(self, subcommand_args: list[str]) -> str:
        """Runs keepassxc-cli and returns to stdout."""
        keepassxc_command_verb = subcommand_args[0]
        keepassxc_command_flags = subcommand_args[1:]

        cmd = (
            [self.cli_path, keepassxc_command_verb]
            + self._base_args()
            + keepassxc_command_flags
        )

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
            )
        except OSError as error:
            raise KeePassXCError(f"Cannot run keepassxc-cli: {error}") from error

        if result.returncode != 0:
            raise KeePassXCError(
                f"Unexpected keepassxc-cli return code: {result.stderr}"
            )

        return result.stdout

    def _base_args(self) -> list[str]:
        """Common args."""
        args = []

        if self.key_file:
            args.extend(["--key-file", self.key_file])

            # Deactivates the password key for the database
            args.append("--no-password")

        return args

    @staticmethod
    def _parse_ls(output: str) -> list[str]:
        """Parse keepassxc entries."""
        entries = []

        for line in output.splitlines():
            line = line.strip()
            if not line:
                # ignore empty lines
                continue

            if line.endswith("/"):
                # only keep entries, ignore folders
                continue

            if line.lower().startswith("enter ") or line.lower().startswith("warning"):
                # ignore interactive prompts
                continue
            entries.append(line)

        return entries

    def list_entries(self, recursive: bool = True) -> list[str]:
        """Lists the entries in the keepassxc database."""
        args = ["ls"]

        if recursive:
            args.append("--recursive")
        args.append(self.database)

        stdout = self._run(args)
        return self._parse_ls(stdout)

    def show_entry(self, entry: str) -> dict[str, str]:
        """Returns the attributes of an entry (no password)."""
        args = ["show", self.database, entry]
        stdout = self._run(args)
        return self._parse_show(stdout)

    def get_totp(self, entry: str) -> str:
        """Retrieves the current TOTP code for an entry."""
        args = ["show", "--totp", self.database, entry]
        return self._run(args)

    @staticmethod
    def _parse_show(output: str) -> dict[str, str]:
        """Parse the output of keepassxc-cli show."""
        fields: dict[str, str] = {}

        for line in output.splitlines():
            if ":" in line:
                key, _, value = line.partition(":")
                fields[key.strip()] = value.strip()
        return fields
