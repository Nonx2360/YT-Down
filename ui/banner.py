from __future__ import annotations

from rich.console import Console, Theme
from rich.panel import Panel
from rich.text import Text

APP_NAME = "YT-Down"
VERSION = "1.0.0"

THEME = Theme(
    {
        "success": "bold green",
        "error": "bold red",
        "warning": "bold yellow",
        "info": "cyan",
        "accent": "bold magenta",
        "title": "bold cyan",
        "dim": "dim",
    }
)

console = Console(theme=THEME)

ART = """██╗   ██╗████████╗
╚██╗ ██╔╝╚══██╔══╝
 ╚████╔╝    ██║
  ╚██╔╝     ██║
   ╚═╝      ╚═╝"""


def build_banner() -> Text:
    art = Text()
    art.append(ART + "\n\n", style="bold cyan")
    art.append(f"─ YouTube Downloader CLI · v{VERSION} ─", style="accent")
    return art


def print_banner() -> None:
    console.print(
        Panel(build_banner(), border_style="bold cyan", padding=(1, 2), expand=False)
    )
