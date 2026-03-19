import subprocess
from shellforge.runtime.events import emit


def run_command(cmd, dry_run=False):
    if dry_run:
        emit("log", {"message": f"DRY RUN: {' '.join(cmd)}"})
        return

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    if process.stdout is not None:
        for line in process.stdout:
            emit("log", {"message": line.rstrip()})

    process.wait()