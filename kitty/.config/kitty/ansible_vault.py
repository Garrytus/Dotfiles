"""Custom Python wrapper around ansible-vault to decrypt and parse vault files."""

import shutil
import subprocess
import yaml

from pathlib import Path


class AnsibleVaultError(RuntimeError):
    """Raised when ansible-vault returns an error."""


class AnsibleVaultNotFoundError(EnvironmentError):
    """Raised when ansible-vault is not found in the PATH."""


class AnsibleVault:
    """Wrapper around ansible-vault."""

    def __init__(
        self,
        vault_file: str,
        *,
        key_file: str,
    ) -> None:
        """Initialize the AnsibleVault wrapper."""
        self.key_file = Path(key_file).expanduser()
        self.vault_file = Path(vault_file).expanduser()

        ansible_vault_cli_path = shutil.which("ansible-vault")
        if not ansible_vault_cli_path:
            raise AnsibleVaultNotFoundError(
                "ansible-vault is not installed or not in the PATH."
            )

        self.ansible_vault_cli_path = ansible_vault_cli_path

    def decrypt(self) -> str:
        """Decrypt the vault and return its raw content as a string."""
        cmd = [
            self.ansible_vault_cli_path,
            "decrypt",
            "--output",
            "-",
            "--vault-password-file",
            str(self.key_file),
            str(self.vault_file),
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
            )
        except OSError as error:
            raise AnsibleVaultError(f"Cannot run ansible-vault: {error}") from error

        if result.returncode != 0:
            raise AnsibleVaultError(
                f"ansible-vault returned an error:\n{result.stderr}"
            )

        return result.stdout

    def list_passwords(self) -> list[str]:
        """Return a flat list of dot-notation keys that hold string values."""
        decrypted_ansible_vault = self.decrypt()

        try:
            data = yaml.safe_load(decrypted_ansible_vault)
        except yaml.YAMLError as error:
            raise AnsibleVaultError(f"Failed to parse vault YAML:\n{error}") from error

        if not isinstance(data, dict):
            raise AnsibleVaultError("Vault seems to be empty.")

        return list(self._flatten(data))

    def get_password(self, key: str) -> str:
        """Return the value for the selected key."""
        decrypted_ansible_vault = self.decrypt()

        try:
            data = yaml.safe_load(decrypted_ansible_vault)
        except yaml.YAMLError as error:
            raise AnsibleVaultError(f"Failed to parse the vault:\n{error}") from error

        parts = key.split(".")
        node = data

        for part in parts:
            if not isinstance(node, dict) or part not in node:
                raise KeyError(
                    f"Key '{key}' not found in vault '{self.vault_file.name}'."
                )
            node = node[part]

        return str(node)

    @staticmethod
    def _flatten(
        data: dict,
        prefix: str = "",
    ):
        """Recursively yield dot-notation paths for every leaf string value."""
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key

            if isinstance(value, dict):
                yield from AnsibleVault._flatten(value, prefix=full_key)

            elif value is not None:
                yield full_key
