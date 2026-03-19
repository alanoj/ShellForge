from pathlib import Path
import time
from shellforge.runtime.events import emit

LOG_FILE = Path("shellforge_demo.log")


def replay_logs(speed: str = "normal"):
    if not LOG_FILE.exists():
        emit("log", {"message": "No demo log found. Run with --record first."})
        return

    # 🔥 speed control
    delays = {
        "fast": 0.005,
        "normal": 0.02,
        "slow": 0.05,
    }

    delay = delays.get(speed, 0.02)

    lines = LOG_FILE.read_text().splitlines()

    # 🔥 fake total for progress bar
    emit("progress", {"total": len(lines)})

    emit("task", {"message": "Replaying installation logs..."})

    for line in lines:
        emit("log", {"message": line})
        emit("progress", {"advance": 1})
        time.sleep(delay)

    emit("task", {"message": "Demo complete"})