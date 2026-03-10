import subprocess
from rich.progress import Progress


def run_command(progress: Progress, task_id, cmd: list[str], dry_run: bool, verbose: bool = False, log_callback=None):

    if dry_run:
        if log_callback:
            log_callback(f"[yellow]DRY RUN[/yellow]: {' '.join(cmd)}")
        progress.update(
            task_id,
            description=f"DRY RUN: {' '.join(cmd)}"
        )
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
        # Stream output line-by-line to avoid UI freezing during long installs
        for line in iter(process.stdout.readline, ""):
            line = line.rstrip()

            if not line:
                continue

            if verbose:
                if log_callback:
                    log_callback(line)
                continue

            # Update progress description for important installer events
            if line.startswith("==>") or line.startswith("🍺"):
                progress.update(task_id, description=line)

            # Send other output to the log panel
            elif log_callback:
                log_callback(line)

    process.wait()