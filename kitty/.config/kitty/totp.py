"""My interactive TOTP selection tool."""

import sys
import tomllib

from pathlib import Path
from typing import Optional

from kittens.tui.handler import Handler
from kittens.tui.loop import Loop

try:
    from fzf import FZF
except ImportError:
    sys.exit("fzf.py file not found")

try:
    from keepassxc import KeePassXC, KeePassXCError
except ImportError:
    sys.exit("keepassxc.py file not found")


class ClipboardWriterHandler(Handler):
    """Write into the system clipboard."""

    def __init__(self, totp: str) -> None:
        """Initialize the ClipboardWriterHandler."""
        self.totp = totp

    def initialize(self) -> None:
        """Initialize the handler."""
        if self.totp:
            self.cmd.write_to_clipboard(self.totp)

        self.quit_loop()


class TOTPPicker:
    """Interactive TOTP selection."""

    def __init__(self, keepass: KeePassXC, fzf: Optional[FZF] = None) -> None:
        """Initialize the TOTPPicker."""
        self.keepass = keepass
        self.fzf = fzf or FZF()

    def run(self) -> str | None:
        """Run the intereactive selection."""
        entries = self.keepass.list_entries()

        if not entries:
            return None

        chosen = self.fzf.select_one(
            entries,
            prompt="TOTP > ",
            header="Enter : Copy TOTP  |  Esc : Quit",
            reverse=True,
            border=True,
            height="50%",
        )

        if chosen is None:
            return None

        try:
            return self.keepass.get_totp(chosen)
        except KeePassXCError:
            return None


def load_custom_configuration() -> dict:
    """Load a custom my custom configuration file."""
    config_path = Path.home() / ".config/kitty/custom_config.toml"

    with open(config_path, "rb") as file_handler:
        config = tomllib.load(file_handler)

    return config


def main(args) -> str | None:
    """Kitty entrypoint."""
    config = load_custom_configuration()

    # TODO: Handle password protected database
    keepass = KeePassXC(
        config["keepass"]["database_location"],
        key_file=config["keepass"]["key_file_location"],
    )

    fzf = FZF()
    picker = TOTPPicker(keepass, fzf)

    totp = picker.run()

    if totp:
        loop = Loop()
        handler = ClipboardWriterHandler(totp.strip())

        loop.loop(handler)
