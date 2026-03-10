from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.panel import Panel

console = Console()


def create_progress_bar(total_steps: int):

    progress = Progress(
        SpinnerColumn(style="#90DBE5"),
        TextColumn("[bold #90DBE5]{task.description}"),
        BarColumn(
            bar_width=120,
            complete_style="#90DBE5",
            finished_style="#DD4874",
            pulse_style="#90DBE5",
        ),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        expand=True,
        console=None,   # ⭐ CRITICAL: prevents duplicate rendering
    )

    progress_panel = Panel(
        progress,
        border_style="#90DBE5",
        padding=(2, 4),
        title="[bold #90DBE5]ShellForge Progress[/bold #90DBE5]",
        expand=True
    )

    return progress_panel, progress, total_steps