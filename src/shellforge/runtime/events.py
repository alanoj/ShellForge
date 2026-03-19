import json
from pathlib import Path
from collections import defaultdict
from typing import Callable

RECORD_MODE = False
LOG_FILE = Path("shellforge_demo.log")

# 🔥 Pub/Sub registry
SUBSCRIBERS: dict[str, list[Callable]] = defaultdict(list)


def set_record_mode(enabled: bool):
    global RECORD_MODE
    RECORD_MODE = enabled

    if enabled:
        LOG_FILE.write_text("")


def subscribe(event_type: str, handler: Callable):
    SUBSCRIBERS[event_type].append(handler)


def emit(event_type: str, payload: dict):
    """
    Event dispatcher

    - RECORD MODE → write ONLY raw logs to file
    - NORMAL MODE → notify subscribers
    """

    if RECORD_MODE:
        # 🔥 Only record RAW LOG EVENTS (ignore UI/meta events)
        if event_type == "log":
            with LOG_FILE.open("a") as f:
                f.write(payload["message"] + "\n")
        return

    # 🔥 dispatch to subscribers
    for handler in SUBSCRIBERS.get(event_type, []):
        handler(payload)