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

    total = len(lines)

    emit("task", {
        "step": 0,
        "total": total,
        "message": "Replaying installation logs..."
    })

    for i, line in enumerate(lines, start=1):
        emit("log", {"message": line})
        emit("task", {
            "step": i,
            "total": total
        })
        time.sleep(delay)

    emit("task", {
        "step": total,
        "total": total,
        "message": "Demo complete"
    })