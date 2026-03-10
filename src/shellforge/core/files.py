import shutil
from pathlib import Path
from importlib.abc import Traversable


def ensure_parent(path: Path, dry_run: bool):
    if dry_run:
        return

    path.parent.mkdir(parents=True, exist_ok=True)


def copy_file(src: Path | Traversable, dst: Path, dry_run: bool):
    src = Path(str(src))

    ensure_parent(dst, dry_run)

    if dry_run:
        return

    shutil.copy2(src, dst)


def copy_tree(src: Path | Traversable, dst: Path, dry_run: bool):
    src = Path(str(src))

    if dry_run:
        return

    if dst.exists():
        shutil.rmtree(dst)

    shutil.copytree(src, dst)