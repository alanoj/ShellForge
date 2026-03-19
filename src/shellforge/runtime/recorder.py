from pathlib import Path
import json

LOG_FILE = Path("shellforge_demo.log")


def record_event(event_type: str, payload: dict):
    with LOG_FILE.open("a") as f:
        f.write(json.dumps({
            "type": event_type,
            "payload": payload
        }) + "\n")
