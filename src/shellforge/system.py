import subprocess
from typing import Sequence

def run_command(cmd: Sequence[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        check=True,
        text=True,
        capture_output=True
    )