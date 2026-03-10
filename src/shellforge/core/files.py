import shutil
from pathlib import Path
from rich.progress import Progress, TaskID
from importlib.abc import Traversable


def ensure_parent(progress: Progress, task_id: TaskID, path: Path, dry_run: bool):
    if dry_run:
        progress.console.print(f"[yellow]DRY RUN:[/yellow] mkdir -p {path.parent}")
        return

    path.parent.mkdir(parents=True, exist_ok=True)


def copy_file(progress: Progress, task_id: TaskID, src: Path | Traversable, dst: Path, dry_run: bool):
    src = Path(str(src))

    ensure_parent(progress, task_id, dst, dry_run)

    if dry_run:
        progress.console.print(f"[yellow]DRY RUN:[/yellow] copy {src.name} -> {dst}")
        return

    shutil.copy2(src, dst)

    progress.console.print(f"[green]Copied[/green] {src.name} -> {dst}")


def copy_tree(progress: Progress, task_id: TaskID, src: Path | Traversable, dst: Path, dry_run: bool):
    src = Path(str(src))

    if dry_run:
        progress.console.print(f"[yellow]DRY RUN:[/yellow] copytree {src} -> {dst}")
        return

    if dst.exists():
        shutil.rmtree(dst)

    shutil.copytree(src, dst)

    progress.console.print(f"[green]Copied[/green] {src} -> {dst}")