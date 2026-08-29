from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Optional

from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)


def create_progress() -> Progress:
    return Progress(
        TextColumn("[bold cyan]{task.description}", justify="left"),
        BarColumn(bar_width=32),
        "[progress.percentage]{task.percentage:>3.0f}%",
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        expand=False,
    )


class DownloadHook:
    """Bridge between yt-dlp's progress_hooks and a rich Progress bar."""

    def __init__(
        self,
        progress: Progress,
        task_id: int,
        on_finished: Optional[Callable[[], None]] = None,
    ):
        self.progress = progress
        self.task_id = task_id
        self.on_finished = on_finished
        self._named = False

    def __call__(self, data: dict[str, Any]) -> None:
        status = data.get("status")
        if status == "downloading":
            if not self._named:
                self._named = True
                name = Path(data.get("filename") or "").name
                if len(name) > 42:
                    name = name[:39] + "…"
                self.progress.update(self.task_id, description=name or "Downloading")
            total = data.get("total_bytes") or data.get("total_bytes_estimate") or 0
            downloaded = float(data.get("downloaded_bytes") or 0)
            if total:
                self.progress.update(
                    self.task_id, completed=downloaded, total=float(total)
                )
            else:
                self.progress.update(self.task_id, completed=downloaded)
        elif status == "finished":
            total = data.get("total_bytes") or data.get("total_bytes_estimate") or 0
            self.progress.update(
                self.task_id,
                completed=float(total) if total else 1.0,
                total=float(total) if total else None,
            )
            if self.on_finished:
                self.on_finished()
