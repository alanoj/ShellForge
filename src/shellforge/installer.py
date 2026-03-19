from shellforge.runtime.events import emit
from shellforge.core.files import copy_file, copy_tree
from shellforge import paths


def install(dry_run=False):

    steps = [
        ("Installing Oh-My-Posh theme", ("copy_file", paths.OMP_SOURCE, paths.OMP_TARGET)),
        ("Installing Ghostty config", ("copy_file", paths.GHOSTTY_SOURCE, paths.GHOSTTY_TARGET)),
        ("Installing ZSH configuration", ("copy_file", paths.ZSHRC_SOURCE, paths.ZSHRC_TARGET)),
        ("Installing Neovim configuration", ("copy_tree", paths.NVIM_SOURCE, paths.NVIM_TARGET)),
    ]

    emit("progress", {"total": len(steps)})

    for description, action in steps:

        emit("task", {"message": description})

        kind, src, dst = action

        if kind == "copy_file":
            copy_file(src, dst, dry_run)

        elif kind == "copy_tree":
            copy_tree(src, dst, dry_run)

        emit("progress", {"advance": 1})

    emit("log", {"message": "[bold green]Install complete.[/bold green]"})