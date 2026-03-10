import subprocess
from rich.progress import Progress


def run_command(
    progress: Progress,
    task_id,
    cmd: list[str],
    dry_run: bool,
    verbose: bool = False,
    log_callback=None
):

    if dry_run:
        if log_callback:
            log_callback(f"[yellow]DRY RUN[/yellow]: {' '.join(cmd)}")
        return

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )

    if process.stdout:

        for line in iter(process.stdout.readline, ""):
            line = line.rstrip()

            if not line:
                continue

            if verbose and log_callback:
                log_callback(line)

            if line.startswith("==> Installing dependency"):
                progress.advance(task_id)

            elif line.startswith("==> Installing"):
                progress.advance(task_id)

            elif line.startswith("🍺"):
                progress.advance(task_id)

    process.wait()