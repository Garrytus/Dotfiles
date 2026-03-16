"""Utils.py."""

import sys
import tomllib

from pathlib import Path


def load_configuration() -> dict:
    """Load my custom configuration file."""
    config_path = Path.home() / ".config/kitty/custom_config.toml"

    try:
        with open(config_path, "rb") as fh:
            return tomllib.load(fh)

    except FileNotFoundError:
        sys.exit(f"Configuration file not found: {config_path}")

    except tomllib.TOMLDecodeError as exc:
        sys.exit(f"Invalid TOML configuration: {exc}")
