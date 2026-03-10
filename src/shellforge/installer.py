import os
from pathlib import Path
import platform
import shutil
import subprocess
from rich.console import Console
from rich.progress import Progress, BarColumn, SpinnerColumn, TextColumn, TaskProgressColumn
from shellforge import paths
from importlib.abc import Traversable
from importlib.resources import files

console = Console()


def ensure_parent(path: Path, dry_run: bool) -> None:
    if dry_run:
        console.print(f"[yellow]DRY RUN:[/yellow] mkdir -p {path.parent}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)


def copy_file(src: Path | Traversable, dst: Path, dry_run: bool) -> None:
    src = Path(str(src))
    ensure_parent(dst, dry_run=dry_run)
    if dry_run:
        console.print(f"[yellow]DRY RUN:[/yellow] copy {src} -> {dst}")
        return
    shutil.copy2(src, dst)
    console.print(f"[green]Copied[/green] {src.name} -> {dst}")


def copy_tree(src: Path | Traversable, dst: Path, dry_run: bool) -> None:
    src = Path(str(src))
    if dry_run:
        console.print(f"[yellow]DRY RUN:[/yellow] copytree {src} -> {dst}")
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    console.print(f"[green]Copied[/green] {src} -> {dst}")


def install(dry_run: bool = False) -> None:

    steps = [
        ("Installing Oh-My-Posh theme", copy_file, paths.OMP_SOURCE, paths.OMP_TARGET),
        ("Installing Ghostty config", copy_file, paths.GHOSTTY_SOURCE, paths.GHOSTTY_TARGET),
        ("Installing ZSH configuration", copy_file, paths.ZSHRC_SOURCE, paths.ZSHRC_TARGET),
        ("Installing Neovim configuration", copy_tree, paths.NVIM_SOURCE, paths.NVIM_TARGET),
    ]

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}"),
        TextColumn("[bold]{task.completed}/{task.total}"),
        BarColumn(bar_width=60),
        TaskProgressColumn(),
        console=console,
    ) as progress:

        task = progress.add_task("Installing configs...", total=len(steps))

        for description, func, src, dst in steps:
            progress.update(task, description=description)
            func(src, dst, dry_run=dry_run)
            progress.advance(task)


def bootstrap(dry_run: bool = False) -> None:
    show_logo()
    console.print("[bold cyan]Starting ShellForge bootstrap...[/bold cyan]")
    with console.status("[bold cyan]Installing system tools..."):
        install_system_tools(dry_run)
    install(dry_run=dry_run)
    console.print("[bold green]Bootstrap complete.[/bold green]")
    

def tool_exists(name:str) -> bool:
    return shutil.which(name) is not None

def run_command(cmd: list[str], dry_run: bool) -> None:
    if dry_run:
        console.print(f"[yellow]DRY RUN:[/yellow] {' '.join(cmd)}")
        return
    
    # Automatically use sudo for apt installs if available
    if cmd[0] == "apt" and shutil.which("sudo"):
        cmd = ["sudo"] + cmd
    subprocess.run(cmd, check=True)
    

def show_logo() -> None:
    console.clear()

    logo = files("shellforge.assets").joinpath("logo.png")
    logo_path = Path(str(logo))

    if logo_path.exists():
        subprocess.run(
            [
                "kitten",
                "icat",
                "--align=center",
                "--scale-up",
                str(logo_path),
            ],
            check=False,
        )

    console.print(
        "\n[bold cyan]⚙ ShellForge — Terminal Environment Bootstrap[/bold cyan]\n"
    )

def install_system_tools(dry_run: bool) -> None:
    system = platform.system()
    
    if system == "Linux":
        package_manager = "apt"
    elif system == "Darwin":
        package_manager = "brew"
    else:
        console.print(f"[red]Unsupported OS:[/red] {system}")
        return
    tools = {
        "nvim": "neovim",
        "oh-my-posh": "oh-my-posh",
        "zsh": "zsh",
    }
    
    for binary, package in tools.items():
        if tool_exists(binary):
            console.print(f"[green]{binary} already installed[/green]")
            continue
        
        console.print(f"[cyan]Installing {package}...[/cyan]")
        
        if package_manager == "apt":
            run_command(["apt", "update"], dry_run)
            run_command(["apt", "install", "-y", package], dry_run)
        elif package_manager == "brew":
            run_command(["brew", "install", package], dry_run)