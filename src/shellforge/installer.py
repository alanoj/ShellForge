import os
from pathlib import Path
import platform
import shutil
import subprocess
import textwrap
from rich.console import Console
from rich.progress import Progress, BarColumn, SpinnerColumn, TextColumn, TaskProgressColumn, TimeElapsedColumn
from shellforge import paths
from importlib.abc import Traversable
from importlib.resources import files

console = Console()


def ensure_parent(path: Path, dry_run: bool) -> None:
    if dry_run:
        console.print(f"[yellow]DRY RUN:[/yellow] mkdir -p {path.parent}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)


def copy_file(progress: Progress, src: Path | Traversable, dst: Path, dry_run: bool) -> None:
    src = Path(str(src))
    ensure_parent(dst, dry_run=dry_run)
    if dry_run:
        progress.console.print(f"[yellow]DRY RUN:[/yellow] copy {src} -> {dst}")
        return
    shutil.copy2(src, dst)
    progress.console.print(f"[green]Copied[/green] {src.name} -> {dst}")


def copy_tree(progress: Progress, src: Path | Traversable, dst: Path, dry_run: bool) -> None:
    src = Path(str(src))
    if dry_run:
        progress.console.print(f"[yellow]DRY RUN:[/yellow] copytree {src} -> {dst}")
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    progress.console.print(f"[green]Copied[/green] {src} -> {dst}")


def install(dry_run: bool = False, compact: bool = False) -> None:

    steps = [
        ("Installing Oh-My-Posh theme", copy_file, paths.OMP_SOURCE, paths.OMP_TARGET),
        ("Installing Ghostty config", copy_file, paths.GHOSTTY_SOURCE, paths.GHOSTTY_TARGET),
        ("Installing ZSH configuration", copy_file, paths.ZSHRC_SOURCE, paths.ZSHRC_TARGET),
        ("Installing Neovim configuration", copy_tree, paths.NVIM_SOURCE, paths.NVIM_TARGET),
    ]

    with Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[bold #90DBE5]{task.description}", justify="center"),
        BarColumn(
            bar_width=120,              # MUCH wider
            complete_style="#90DBE5",
            finished_style="#90DBE5",
            pulse_style="#90DBE5",
        ),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=console,
        expand=True
    ) as progress:

        task = progress.add_task("Installing configs...", total=len(steps))

        for description, func, src, dst in steps:
            progress.update(task, description=description)
            func(src, dst, dry_run=dry_run)
            progress.advance(task)


def splash_intro() -> None:
    steps = [
        "Initializing environment",
        "Checking dependencies",
        "Preparing installer",
    ]

    with Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[bold #90DBE5]{task.description}"),
        console=console,
        transient=True,
    ) as progress:

        for step in steps:
            task = progress.add_task(step, total=None)
            import time
            time.sleep(0.6)
            progress.remove_task(task)

def bootstrap(dry_run: bool = False, compact: bool = False) -> None:
    show_logo()
    splash_intro()

    console.print("[bold #90DBE5]Starting ShellForge bootstrap...[/bold #90DBE5]\n")

    # ---------- ALL INSTALL STEPS ----------
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

    # ---------- PROGRESS UI ----------
    current_task = ""

    with Progress(
        SpinnerColumn(style="cyan"),
        BarColumn(
            bar_width=None,
            complete_style="#90DBE5",
            finished_style="#90DBE5",
            pulse_style="#90DBE5",
        ),
        TaskProgressColumn(),
        console=console,
        expand=True,
    ) as progress:

        task = progress.add_task("", total=len(steps))

        for description, action in steps:

            if description != current_task:
                progress.update(task, description=description)
                current_task = description

            if action is None:
                pass

            elif isinstance(action, list):
                run_command(progress, action, dry_run, compact)

            elif isinstance(action, tuple):
                kind, src, dst = action
                if kind == "copy_file":
                    copy_file(progress, src, dst, dry_run)
                elif kind == "copy_tree":
                    copy_tree(progress, src, dst, dry_run)

            progress.advance(task)

    console.print("\n[bold green]Bootstrap complete.[/bold green]")

def tool_exists(name:str) -> bool:
    return shutil.which(name) is not None

def run_command(progress: Progress, cmd: list[str], dry_run: bool, compact: bool = False) -> None:
    if dry_run:
        progress.console.print(f"[yellow]DRY RUN:[/yellow] {' '.join(cmd)}")
        return

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    if process.stdout:
        for line in process.stdout:
            if not compact:
                progress.console.print(line.rstrip())

    process.wait()

def show_logo() -> None:
    console.clear()

    # Detect Docker (kitty graphics usually unsupported there)
    running_in_docker = Path("/.dockerenv").exists()

    logo = files("shellforge.assets").joinpath("logo.png")
    logo_path = Path(str(logo))

    image_rendered = False
    cols, rows = shutil.get_terminal_size()
    width = int(cols * 0.7)
    height = 6

    if not running_in_docker and logo_path.exists():
        try:
            subprocess.run(
                [
                    "kitten",
                    "icat",
                    "--align=center",
                    "--place",
                    f"{width}x{height}@{(cols-width)//2}x0",
                    str(logo_path),
                ],
                check=False,
            )
            print("\n" * (height + 1))
            image_rendered = True
        except Exception:
            image_rendered = False

    # ASCII fallback if image rendering failed
    if not image_rendered:
        ascii_logo = textwrap.dedent("""
███████╗██╗  ██╗███████╗██╗     ██╗     ███████╗ ██████╗ ██████╗  ██████╗ ███████╗
██╔════╝██║  ██║██╔════╝██║     ██║     ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
███████╗███████║█████╗  ██║     ██║     █████╗  ██║   ██║██████╔╝██║  ███╗█████╗
╚════██║██╔══██║██╔══╝  ██║     ██║     ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝
███████║██║  ██║███████╗███████╗███████╗██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
""")
        console.print(f"[bold #90DBE5]{ascii_logo}[/bold #90DBE5]", justify="center")

    # Subtitle
    console.print(
        "[bold #90DBE5]  ShellForge — Terminal Environment Bootstrap[/bold #90DBE5]\n",
        justify="center",
    )

def install_system_tools(dry_run: bool, compact: bool = False) -> None:
    if not shutil.which("brew"):
        console.print("[red]Homebrew is required but was not found on this system.[/red]")
        console.print("[yellow]Install Homebrew first: https://brew.sh[/yellow]")
        return

    tools = {
        "nvim": "neovim",
        "oh-my-posh": "oh-my-posh",
        "zsh": "zsh",
    }

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold #90DBE5]{task.description}"),
        BarColumn(bar_width=80),
        TaskProgressColumn(),
        console=console,
        expand=True,
    ) as progress:

        task = progress.add_task("Installing system tools...", total=len(tools))

        for binary, package in tools.items():

            if tool_exists(binary):
                progress.update(task, description=f"{binary} already installed")
                progress.advance(task)
                continue

            progress.update(task, description=f"Installing {package}")
            run_command(["brew", "install", package], dry_run)
            progress.advance(task)