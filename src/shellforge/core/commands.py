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

    dependency_count = 0

    if process.stdout:

        for line in iter(process.stdout.readline, ""):
            line = line.rstrip()

            if not line:
                continue

            # Send all command output to the log panel so Live controls rendering
            if log_callback:
                log_callback(line)

            # Detect dependency list from brew and expand total steps
            if "Installing dependencies for" in line:
                deps = line.split(":")[-1]
                dependency_count = len([d.strip() for d in deps.split(",") if d.strip()])

                try:
                    task = progress.tasks[task_id]
                    progress.update(task_id, total=task.total + dependency_count)
                except Exception:
                    pass

                continue

            # Advance progress only when a package finishes installing
            if line.startswith("🍺"):
                progress.advance(task_id)

    process.wait()