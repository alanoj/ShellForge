from rich.console import Console, Group
from rich.progress import Progress, SpinnerColumn, BarColumn, TaskProgressColumn, TextColumn
from rich.panel import Panel
from rich.align import Align
from rich.live import Live
from rich.table import Table

from shellforge.ui.logo import show_logo
from shellforge.ui.splash import splash_intro
from shellforge.core.commands import run_command
from shellforge.core.files import copy_file, copy_tree
from shellforge.core.tools import tool_exists
from shellforge.ui.progress import create_progress_bar
from shellforge import paths

console = Console()


class LogPanel:
    def __init__(self, max_lines=10):
        self.lines = []
        self.max_lines = max_lines

    def log(self, message: str):
        self.lines.append(message)
        if len(self.lines) > self.max_lines:
            self.lines.pop(0)

    def __rich__(self):
        table = Table.grid()
        for line in self.lines:
            table.add_row(line)
        return Panel(
            table,
            title="Logs",
            border_style="#90DBE5",
            expand=True
        )


def bootstrap(dry_run=False, compact=False):

    show_logo()
    console.rule(style="#90DBE5")
    splash_intro()

    console.print("[bold #90DBE5]Starting ShellForge bootstrap...[/bold #90DBE5]\n")

    steps = []

    tools = {
        "nvim": "neovim",
        "oh-my-posh": "oh-my-posh",
        "zsh": "zsh",
    }

    for binary, package in tools.items():

        if tool_exists(binary):
            steps.append((f"[bold dark_orange]{binary}[/bold dark_orange] already installed", None))

        else:
            steps.append((f"Installing {package}", ["brew", "install", package]))

    steps.extend([
        ("Installing Oh-My-Posh theme", ("copy_file", paths.OMP_SOURCE, paths.OMP_TARGET)),
        ("Installing Ghostty config", ("copy_file", paths.GHOSTTY_SOURCE, paths.GHOSTTY_TARGET)),
        ("Installing ZSH configuration", ("copy_file", paths.ZSHRC_SOURCE, paths.ZSHRC_TARGET)),
        ("Installing Neovim configuration", ("copy_tree", paths.NVIM_SOURCE, paths.NVIM_TARGET)),
    ])

    log_panel = LogPanel()

    progress_panel, progress, _ = create_progress_bar(len(steps))
    task = progress.add_task(
        "[bold #90DBE5]Initializing ShellForge bootstrap...[/bold #90DBE5]",
        total=len(steps)
    )

    layout = Group(
        Align.center(progress_panel, vertical="middle"),
        log_panel
    )

    with Live(layout, console=console, refresh_per_second=10) as live:
        # Force an initial render so Rich tracks the layout correctly
        live.update(layout)

        for description, action in steps:
            progress.update(task, description=f"[bold #90DBE5]{description}[/bold #90DBE5]")
            if action is None:
                log_panel.log(f"[green]✓ {description}[/green]")
            elif isinstance(action, list):

                log_panel.log(f"[cyan]➜ Running[/cyan]: {' '.join(action)}")
                run_command(
                    progress,
                    task,
                    action,
                    dry_run,
                    verbose=not compact,
                    log_callback=log_panel.log
                )

            elif isinstance(action, tuple):

                kind, src, dst = action

                if kind == "copy_file":

                    if dry_run:
                        log_panel.log(f"[yellow]DRY RUN[/yellow]: copy {src} → {dst}")                        
                    else:
                        log_panel.log(f"[cyan]Copying[/cyan] {src} → {dst}")
                        copy_file(progress, task, src, dst, dry_run)

                elif kind == "copy_tree":

                    if dry_run:
                        log_panel.log(f"[yellow]DRY RUN[/yellow]: copytree {src} → {dst}")
                    else:
                        log_panel.log(f"[cyan]Copying directory[/cyan] {src} → {dst}")
                        copy_tree(progress, task, src, dst, dry_run)

            progress.advance(task)

    console.print("\n[bold green]Bootstrap complete.[/bold green]")