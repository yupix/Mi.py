import logging

from rich import pretty
from rich.console import Console
from rich.logging import RichHandler

console = None
log = None


def init(debug):
    global console
    global log

    level = "DEBUG" if debug else "INFO"
    console = Console()
    pretty.install()
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=debug)],
    )

    log = logging.getLogger("rich")
