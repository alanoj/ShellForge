from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console
import time

console = Console()


def splash_intro():

    steps = [
        "Initializing environment",
        "Checking dependencies",
        "Preparing installer",
    ]

    with Progress(
        SpinnerColumn(style="#90DBE5"),
        TextColumn("[bold #90DBE5]{task.description}"),
        console=console,
        transient=True,
    ) as progress:

        for step in steps:
            task = progress.add_task(step, total=None)
            time.sleep(0.6)
            progress.remove_task(task)