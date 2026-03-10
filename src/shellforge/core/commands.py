import subprocess
from rich.progress import Progress


def run_command(progress: Progress, cmd: list[str], dry_run: bool, verbose: bool = False):

    if dry_run:
        progress.update(
            progress.tasks[0].id,
            description=f"DRY RUN: {' '.join(cmd)}"
        )
        return

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    if process.stdout:
        for line in process.stdout:
            line = line.rstrip()

            if verbose:
                progress.console.print(line)
                continue

            if line.startswith("==>") or line.startswith("🍺"):
                progress.update(
                    progress.tasks[0].id,
                    description=line
                )

    process.wait()