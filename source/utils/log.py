import sys

PREFIX = "[TouchView]"


def log(message: str, level: str | None = None) -> None:
    """Print a structured console line prefixed with ``PREFIX``.

    Args:
        message: Text to print.
        level: Optional uppercase level tag (INFO, WARNING, ERROR, DEBUG).
    """
    tag = f"{level}: " if level else ""
    sys.stdout.write(f"{PREFIX} {tag}{message}\n")
    sys.stdout.flush()
