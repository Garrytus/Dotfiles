"""Clipboard Writer."""

from kittens.tui.handler import Handler


class ClipboardWriterHandler(Handler):
    """Write into the system clipboard."""

    def __init__(self, data: str) -> None:
        """Initialize the ClipboardWriterHandler."""
        self.data = data

    def initialize(self) -> None:
        """Initialize the handler."""
        if self.data:
            self.cmd.write_to_clipboard(self.data)

        self.quit_loop()
