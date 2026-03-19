from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from shellforge.runtime.events import subscribe
from shellforge.ui.logs import LogPanel
from shellforge.ui.constants import get_content_width, PANEL_COLOR, PANEL_TITLE_STYLE, center_renderable


class Renderer:
    def __init__(self):
        self.progress = Progress(
            SpinnerColumn(),
            BarColumn(bar_width=None),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
        )

        self.task_id = self.progress.add_task("", total=100)
        self.logs = LogPanel(max_lines=20)

        self.layout = Layout()
        self.layout.split_column(
            Layout(name="progress", size=5),
            Layout(name="logs"),
        )

        subscribe("log", self.handle_log)
        subscribe("progress", self.handle_progress)
        subscribe("task", self.handle_task)

    def handle_log(self, payload):
        self.logs.log(payload["message"])
        if hasattr(self, "live"):
            self.live.update(self.render())

    def handle_progress(self, payload):
        if "advance" in payload:
            self.progress.advance(self.task_id, payload["advance"])
        if "total" in payload:
            self.progress.update(self.task_id, total=payload["total"])
        if hasattr(self, "live"):
            self.live.update(self.render())

    def handle_task(self, payload):
        self.progress.update(self.task_id, description=payload["message"])
        if hasattr(self, "live"):
            self.live.update(self.render())

    def render(self):
        width = get_content_width()
        progress_panel = Panel(
            self.progress,
            title=f"[{PANEL_TITLE_STYLE}]ShellForge Progress[/]",
            border_style=PANEL_COLOR,
            width=width,
        )

        logs_panel = self.logs.render()

        self.layout["progress"].update(center_renderable(progress_panel))
        self.layout["logs"].update(center_renderable(logs_panel))

        return self.layout

    def run(self, fn):
        with Live(self.render(), refresh_per_second=20, screen=False) as live:
            self.live = live
            fn()
            live.update(self.render())