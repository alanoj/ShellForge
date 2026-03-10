from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
)
from rich.panel import Panel

console = Console()


def create_progress_bar(total_steps: int):

    progress = Progress(
        SpinnerColumn(style="#90DBE5"),
        BarColumn(
            bar_width=120,
            complete_style="#DD4874",
            finished_style="green_yellow",
            pulse_style="#90DBE5",
        ),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        expand=True,
        console=None,
    )

    progress_panel = Panel(
        progress,
        border_style="#90DBE5",
        padding=(2, 4),
        title="[bold #90DBE5]ShellForge Progress[/bold #90DBE5]",
        title_align="left",
        expand=True
    )

    return progress_panel, progress