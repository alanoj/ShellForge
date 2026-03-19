from rich.console import Console
from shellforge.runtime.events import emit, set_record_mode
from shellforge.core.commands import run_command
from shellforge.core.files import copy_file, copy_tree
from shellforge.core.tools import tool_exists
from shellforge.core.packages import PACKAGES
from shellforge import paths

console = Console()


def bootstrap(
    dry_run=False,
    compact=False,
    speed="normal",
    terminal: str = "ghostty",
    skip_terminal: bool = False,
    record: bool = False,
):

    if record:
        set_record_mode(True)
        print("Starting log recording...")

    emit("log", {"message": "Starting ShellForge bootstrap..."})

    steps = []

    # ----------------------------
    # Build install steps
    # ----------------------------
    for group_name, group in PACKAGES.items():
        for binary, package in group:
            if tool_exists(binary):
                steps.append((f"{binary} already installed", None))
            else:
                steps.append((f"Installing {package}", ["brew", "install", package]))

    terminal_configs = {
        "ghostty": (paths.GHOSTTY_SOURCE, paths.GHOSTTY_TARGET),
    }

    if not skip_terminal and terminal in terminal_configs:
        src, dst = terminal_configs[terminal]
        steps.append((f"Installing {terminal} config", ("copy_file", src, dst)))

    steps.extend([
        ("Installing Oh-My-Posh theme", ("copy_file", paths.OMP_SOURCE, paths.OMP_TARGET)),
        ("Installing ZSH configuration", ("copy_file", paths.ZSHRC_SOURCE, paths.ZSHRC_TARGET)),
        ("Installing Neovim configuration", ("copy_tree", paths.NVIM_SOURCE, paths.NVIM_TARGET)),
    ])

    # ----------------------------
    # Progress init
    # ----------------------------
    emit("progress", {"total": len(steps)})

    # ----------------------------
    # Execute steps
    # ----------------------------
    for description, action in steps:
        emit("task", {"message": description})

        if action is None:
            emit("log", {"message": f"✓ {description}"})
            emit("progress", {"advance": 1})
            continue

        if isinstance(action, list):
            run_command(action, dry_run)
            emit("progress", {"advance": 1})
            continue

        kind, src, dst = action

        if kind == "copy_file":
            copy_file(src, dst, dry_run)

        elif kind == "copy_tree":
            copy_tree(src, dst, dry_run)

        emit("progress", {"advance": 1})

    # ----------------------------
    # Finish
    # ----------------------------
    if record:
        print("Done")
    else:
        emit("log", {"message": "Bootstrap complete."})