from rich.panel import Panel
from rich.text import Text
from collections import deque
from shellforge.ui.constants import get_content_width, PANEL_COLOR, PANEL_TITLE_STYLE


class LogPanel:
    def __init__(self, max_lines: int = 12):
        self.lines = deque(maxlen=max_lines)

    def log(self, message: str):
        self.lines.append(message)

    def render(self):
        log_content = Text("\n".join(self.lines))

        return Panel(
            log_content,
            title=f"[{PANEL_TITLE_STYLE}]Logs[/]",
            border_style=PANEL_COLOR,
            width=get_content_width(),
        )