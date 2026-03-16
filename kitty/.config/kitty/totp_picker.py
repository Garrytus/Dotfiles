"""My interactive TOTP selection tool."""

from kittens.tui.loop import Loop

from keepassxc import KeePassXC, KeePassXCError

from clipboard_writer_handler import ClipboardWriterHandler
from fzf import FZF
from utils import load_configuration


class TOTPPicker:
    """Interactive TOTP selection."""

    def __init__(self, keepass: KeePassXC, fzf: FZF) -> None:
        """Initialize the TOTPPicker."""
        self.keepass = keepass
        self.fzf = fzf

    def run(self) -> str | None:
        """Run the intereactive selection."""
        entries = self.keepass.list_entries()

        if not entries:
            return None

        selected_entry = self.fzf.select_one(
            entries,
            prompt="TOTP > ",
            header="Enter : Copy TOTP  |  Esc : Quit",
            reverse=True,
            border=True,
            height="50%",
        )

        if selected_entry is None:
            return None

        try:
            return self.keepass.get_totp(selected_entry)
        except KeePassXCError:
            return None


def main(args) -> str | None:
    """Kitty entrypoint."""
    config = load_configuration()

    keepass_config = config.get("keepass", {})
    database_path = keepass_config.get("database_location")
    key_file_path = keepass_config.get("key_file_location")

    # TODO: Handle password protected database
    keepass = KeePassXC(
        database=database_path,
        key_file=key_file_path,
    )

    fzf = FZF()
    picker = TOTPPicker(keepass, fzf)

    totp = picker.run()

    if totp:
        loop = Loop()
        handler = ClipboardWriterHandler(totp.strip())

        loop.loop(handler)
