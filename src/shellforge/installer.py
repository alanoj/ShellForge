from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TaskProgressColumn, TextColumn
from shellforge.ui.progress import create_progress_bar
from shellforge.core.files import copy_file, copy_tree
from shellforge import paths

console = Console()


def install(dry_run=False):

    steps = [
        ("Installing Oh-My-Posh theme", ("copy_file", paths.OMP_SOURCE, paths.OMP_TARGET)),
        ("Installing Ghostty config", ("copy_file", paths.GHOSTTY_SOURCE, paths.GHOSTTY_TARGET)),
        ("Installing ZSH configuration", ("copy_file", paths.ZSHRC_SOURCE, paths.ZSHRC_TARGET)),
        ("Installing Neovim configuration", ("copy_tree", paths.NVIM_SOURCE, paths.NVIM_TARGET)),
    ]

    progress_panel, progress, _ = create_progress_bar(len(steps))
    console.print(progress_panel)
    with progress:

        task = progress.add_task(
            "[bold #90DBE5]Installing ShellForge configs...[/bold #90DBE5]",
            total=len(steps)
        )

        for description, action in steps:

            progress.update(task, description=description)

            kind, src, dst = action

            if kind == "copy_file":
                copy_file(progress, task, src, dst, dry_run)

            elif kind == "copy_tree":
                copy_tree(progress, task, src, dst, dry_run)

            progress.advance(task)

    console.print("[bold green]Install complete.[/bold green]")