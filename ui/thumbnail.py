from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Optional
from urllib.request import urlretrieve

from rich.console import Console

from core.formats import human_size

console = Console()


def show_thumbnail(info: dict, console: Console) -> None:
    """Download and display the video thumbnail in the terminal."""
    thumb_url = info.get("thumbnail")
    if not thumb_url:
        return

    tmp = None
    try:
        tmp = Path(tempfile.mktemp(suffix=".webp"))
        urlretrieve(thumb_url, tmp)

        from term_image.image import from_file

        img = from_file(str(tmp))
        img.set_size(30)
        img.draw()
        console.print()
    except Exception:
        pass
    finally:
        if tmp and tmp.exists():
            tmp.unlink()
