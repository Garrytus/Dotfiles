"""Custom Python wrapper around fzf to provide interactive terminal selection."""

import shutil
import subprocess

from pathlib import Path
from typing import Optional, Union


class FZFError(RuntimeError):
    """Raised when fzf returns an error."""


class FZFNotFoundError(EnvironmentError):
    """Raised when fzf is not found in the PATH."""


class FZF:
    """Wrapper around fzf."""

    def __init__(self, fzf_path: Optional[str] = None) -> None:
        """Initialize the fzf wrapper."""
        if fzf_path:
            if not Path(fzf_path).is_file():
                raise FZFNotFoundError(f"fzf binary not found in: {fzf_path}")

            self.fzf_path = fzf_path

        else:
            found = shutil.which("fzf")
            if not found:
                raise FZFNotFoundError("fzf not installed or not in the PATH.")

            self.fzf_path = found

    def prompt(
        self,
        items: list[str],
        *,
        multi: bool = False,
        query: str = "",
        prompt: str = "> ",
        header: str = "",
        preview: str = "",
        preview_window: str = "",
        height: Union[str, int] = "",
        border: bool = False,
        reverse: bool = False,
        case_sensitive: bool = False,
        exact: bool = False,
        no_sort: bool = False,
        tac: bool = False,
        nth: str = "",
        with_nth: str = "",
        delimiter: str = "",
        bind: Optional[list[str]] = None,
        extra_args: Optional[list[str]] = None,
    ) -> list[str]:
        """Run fzf with the provided list of items and return the selection."""

        cmd = self._build_command(
            multi=multi,
            query=query,
            prompt=prompt,
            header=header,
            preview=preview,
            preview_window=preview_window,
            height=height,
            border=border,
            reverse=reverse,
            case_sensitive=case_sensitive,
            exact=exact,
            no_sort=no_sort,
            tac=tac,
            nth=nth,
            with_nth=with_nth,
            delimiter=delimiter,
            bind=bind or [],
            extra_args=extra_args or [],
        )

        input_data = "\n".join(items)

        try:
            result = subprocess.run(
                cmd,
                input=input_data,
                capture_output=True,
                text=True,
            )
        except OSError as error:
            raise FZFError(f"Unable to run fzf : {error}") from error

        if result.returncode == 130:
            # Canceled by the user (Esc / Ctrl-C)
            return []

        if result.returncode == 1:
            # No match found
            return []

        if result.returncode == 2:
            # Errored
            raise FZFError(f"Oops:\n{result.stderr}")

        if result.returncode != 0:
            # Errored
            raise FZFError(
                f"fzf returned an unexpected error {result.returncode} :\n{result.stderr}"
            )

        output = result.stdout.strip()
        if not output:
            return []
        return output.splitlines()

    def select_one(self, items: list[str], **kwargs) -> Optional[str]:
        """Select only one element."""
        kwargs.pop("multi", None)
        results = self.prompt(items, multi=False, **kwargs)
        return results[0] if results else None

    def select_many(self, items: list[str], **kwargs) -> list[str]:
        """Multiple selection."""
        kwargs.pop("multi", None)
        return self.prompt(items, multi=True, **kwargs)

    def select_files(
        self,
        directory: str = ".",
        pattern: str = "",
        **kwargs,
    ) -> list[str]:
        """Scans a directory and runs fzf on the files found."""
        files = [str(f) for f in Path(directory).rglob(pattern or "*") if f.is_file()]

        if not files:
            return []

        return self.prompt(files, **kwargs)

    def _build_command(
        self,
        multi: bool,
        query: str,
        prompt: str,
        header: str,
        preview: str,
        preview_window: str,
        height: Union[str, int],
        border: bool,
        reverse: bool,
        case_sensitive: bool,
        exact: bool,
        no_sort: bool,
        tac: bool,
        nth: str,
        with_nth: str,
        delimiter: str,
        bind: list[str],
        extra_args: list[str],
    ) -> list[str]:
        """Build the fzf command."""

        cmd = [self.fzf_path]

        fzf_boolean_flags = [
            (border, "--border"),
            (exact, "--exact"),
            (multi, "--multi"),
            (no_sort, "--no-sort"),
            (reverse, "--reverse"),
            (tac, "--tac"),
        ]

        for cond, flag in fzf_boolean_flags:
            if cond:
                cmd.append(flag)

        if not case_sensitive:
            # default is case insensitive
            cmd.append("--ignore-case")

        fzf_value_flags = [
            (delimiter, "--delimiter"),
            (header, "--header"),
            (height, "--height"),
            (nth, "--nth"),
            (preview, "--preview"),
            (preview_window, "--preview-window"),
            (prompt, "--prompt"),
            (query, "--query"),
            (with_nth, "--with-nth"),
        ]

        for value, flag in fzf_value_flags:
            if value:
                cmd.extend([flag, str(value)])

        for b in bind:
            cmd.extend(["--bind", b])

        cmd.extend(extra_args)

        return cmd

    def __repr__(self) -> str:
        """Visual representation."""
        return f"FZF(fzf_path={self.fzf_path!r})"
