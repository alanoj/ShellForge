import time
from shellforge.runtime.events import emit


def run_demo(speed: str = "normal"):

    delay_map = {
        "fast": 0.05,
        "normal": 0.15,
        "slow": 0.3,
    }

    delay = delay_map.get(speed, 0.15)

    steps = [
        ("Installing neovim", 5),
        ("Installing oh-my-posh", 4),
        ("Installing zsh", 3),
        ("Copying config files", 4),
        ("Finalizing setup", 2),
    ]

    total = sum(count for _, count in steps)
    emit("progress", {"total": total})

    for step, count in steps:
        emit("task", {"message": step})

        for i in range(count):
            emit("log", {"message": f"[cyan]➜[/cyan] {step} (step {i+1}/{count})"})
            time.sleep(delay)
            emit("progress", {"advance": 1})

    emit("log", {"message": "[bold green]󰄭 Demo complete.[/bold green]"})
