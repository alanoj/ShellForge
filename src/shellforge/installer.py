from pathlib import Path
import shutil
from rich.console import Console
from shellforge import paths
from importlib.abc import Traversable

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
    copy_file(paths.OMP_SOURCE, paths.OMP_TARGET, dry_run=dry_run)
    copy_tree(paths.GHOSTTY_SOURCE, paths.GHOSTTY_TARGET, dry_run=dry_run)
    copy_file(paths.ZSHRC_SOURCE, paths.ZSHRC_TARGET, dry_run=dry_run)
    copy_tree(paths.NVIM_SOURCE, paths.NVIM_TARGET, dry_run=dry_run)


def bootstrap(dry_run: bool = False) -> None:
    console.print("[bold cyan]Starting ShellForge bootstrap...[/bold cyan]")
    install(dry_run=dry_run)
    console.print("[bold green]Bootstrap complete.[/bold green]")