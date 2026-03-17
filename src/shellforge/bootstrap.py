from rich.console import Console, Group
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
        self.history = []
        self.max_lines = max_lines

    def log(self, message: str):
        self.history.append(message)

    def __rich__(self):
        table = Table.grid()

        for line in self.history[-self.max_lines:]:
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
            steps.append((f"{binary} already installed", None))
        else:
            steps.append((f"Installing {package}", ["brew", "install", package]))

    steps.extend([
        ("Installing Oh-My-Posh theme", ("copy_file", paths.OMP_SOURCE, paths.OMP_TARGET)),
        ("Installing Ghostty config", ("copy_file", paths.GHOSTTY_SOURCE, paths.GHOSTTY_TARGET)),
        ("Installing ZSH configuration", ("copy_file", paths.ZSHRC_SOURCE, paths.ZSHRC_TARGET)),
        ("Installing Neovim configuration", ("copy_tree", paths.NVIM_SOURCE, paths.NVIM_TARGET)),
    ])

    log_panel = LogPanel()

    progress_panel, progress = create_progress_bar(console, len(steps))

    task = progress.add_task("", total=len(steps))

    current_step = "[bold #90DBE5]Initializing ShellForge bootstrap...[/bold #90DBE5]"

    layout = Group(
        Align.center(current_step),
        Align.center(progress_panel),
        log_panel
    )

    with Live(layout, console=console, refresh_per_second=10) as live:

        for description, action in steps:

            current_step = f"[bold #90DBE5]{description}[/bold #90DBE5]"

            layout = Group(
                Align.center(current_step),
                Align.center(progress_panel),
                log_panel
            )

            live.update(layout)

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
                        copy_file(src, dst, dry_run)

                elif kind == "copy_tree":

                    if dry_run:
                        log_panel.log(f"[yellow]DRY RUN[/yellow]: copytree {src} → {dst}")
                    else:
                        log_panel.log(f"[cyan]Copying directory[/cyan] {src} → {dst}")
                        copy_tree(src, dst, dry_run)

            # Advance progress only for non-command steps.
            # Command installs (brew etc.) advance inside run_command() based on output.
            if not isinstance(action, list):
                progress.advance(task)

    console.print("\n[bold green]󰄭 Bootstrap complete.[/bold green]")
    console.print(
        "[bold #90DBE5]Open a new terminal or run [white]exec zsh[/white] to load the new ShellForge environment.[/bold #90DBE5]"
    )