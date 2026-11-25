"""Create private local files without replacing an existing destination."""

import os


def private_opener(path: str, flags: int) -> int:
    """Use with exclusive binary creation via open() or anyio.open_file()."""
    return os.open(path, flags, 0o600)
