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

        progress.update(task_id, description=f"DRY RUN: {' '.join(cmd)}")
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
    dependency_installed = 0

    if process.stdout:

        for line in iter(process.stdout.readline, ""):
            line = line.rstrip()

            if not line:
                continue

            if verbose and log_callback:
                log_callback(line)

            # Detect dependency list
            if "Installing dependencies for" in line:
                if log_callback:
                    log_callback(line)

                deps = line.split(":")[-1]
                dependency_count = len([d.strip() for d in deps.split(",") if d.strip()])

                # Increase the progress total so dependency installs move the bar
                try:
                    task = progress.tasks[task_id]
                    progress.update(task_id, total=task.total + dependency_count)
                except Exception:
                    pass

                continue

            # Detect individual dependency install
            if line.startswith("==> Installing"):
                progress.update(task_id, description=line)
                dependency_installed += 1
                progress.advance(task_id)

            # Bottle finished installing
            elif line.startswith("🍺"):
                progress.update(task_id, description=line)

            elif log_callback:
                log_callback(line)

    process.wait()