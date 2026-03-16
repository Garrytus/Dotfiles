"""Interactive Ansible Vault password selector."""

import sys

from pathlib import Path
from typing import Optional

from kittens.tui.loop import Loop

from ansible_vault import AnsibleVault, AnsibleVaultError

from clipboard_writer_handler import ClipboardWriterHandler
from fzf import FZF
from utils import load_configuration


class VaultPasswordPickerError(EnvironmentError):
    """Raised when the vault picker returns an error."""


class NoVaultFoundError(VaultPasswordPickerError):
    """Raised when keepassxc-cli is not found in the PATH."""


class VaultPasswordPicker:
    """Interactive ansible-vault password selector."""

    # Files whose first line contains this marker are Ansible vaults
    VAULT_MARKER = "$ANSIBLE_VAULT"

    def __init__(
        self,
        repo_path: str,
        key_file_name: str,
        fzf: Optional[FZF] = None,
    ) -> None:
        self.repo_path = Path(repo_path).expanduser()
        self.key_file = self.repo_path / key_file_name
        self.fzf = fzf or FZF()

    def _find_vaults(self) -> list[Path]:
        """Recursively find vault files in the repository."""
        vault_files = []

        for path in self.repo_path.rglob("*.y*ml"):
            if not path.is_file():
                continue
            try:
                first_line = path.read_text(errors="replace").splitlines()[0]
                if self.VAULT_MARKER in first_line:
                    vault_files.append(path)

            except (OSError, IndexError):
                continue

        return sorted(vault_files)

    def run(self) -> str | None:
        """Run the interactive selection."""
        # pick a vault file
        vault_files = self._find_vaults()

        if not vault_files:
            raise NoVaultFoundError("No Ansible vault files found in the repository.")

        # display paths relative to the repo
        display_names = [str(v.relative_to(self.repo_path)) for v in vault_files]

        selected_vault_file = self.fzf.select_one(
            display_names,
            prompt="Vault > ",
            header="Select a vault  |  Enter : open  |  Esc : quit",
            reverse=True,
            border=True,
            height="50%",
        )

        if selected_vault_file is None:
            return None

        # resolve back to an absolute path
        vault_path = self.repo_path / selected_vault_file

        # pick an entry inside the vault
        vault = AnsibleVault(str(vault_path), key_file=str(self.key_file))
        entries = vault.list_passwords()

        chosen_key = self.fzf.select_one(
            entries,
            prompt="Password > ",
            header=f"{selected_vault_file}  |  Enter : copy  |  Esc : back",
            reverse=True,
            border=True,
            height="50%",
        )

        if chosen_key is None:
            return None

        try:
            return vault.get_password(chosen_key)

        except (KeyError, AnsibleVaultError) as error:
            raise VaultPasswordPickerError(str(error))

    @staticmethod
    def _die(message: str) -> None:
        sys.exit(f"[vault-picker] {message}")


def main(args) -> str | None:
    """Kitty entrypoint."""
    config = load_configuration()

    vault_config = config.get("ansible_vault", {})
    repo_path = vault_config.get("repo_path")
    key_file_name = vault_config.get("key_file_name", "vault.key")

    fzf = FZF()
    picker = VaultPasswordPicker(
        repo_path=repo_path,
        key_file_name=key_file_name,
        fzf=fzf,
    )

    secret = picker.run()

    if secret:
        loop = Loop()
        handler = ClipboardWriterHandler(secret.strip())
        loop.loop(handler)
