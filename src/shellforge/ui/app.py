import asyncio
import itertools

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer
from textual.containers import Vertical
from textual.widgets import Static
from textual.widgets import ProgressBar

from shellforge.ui.views.demo import DemoView
from shellforge.ui.views.doctor import DoctorView
from shellforge.ui.widgets.banner import Banner
from shellforge.ui.widgets.input import CommandInput

from shellforge.runtime.events import subscribe
from shellforge.runtime.replay import replay_logs
from shellforge.ui.widgets.logs import Logs


class ShellForgeApp(App):
    def __init__(self, start_mode: str = "demo"):
        super().__init__()
        self.start_mode = start_mode

    # =====================
    # GLOBAL KEY HANDLING
    # =====================

    def on_key(self, event):
        if event.key in ("escape", "ctrl+q"):
            self.exit()

    CSS_PATH = [
        "styles/base.css",
        "styles/banner.css",
        "styles/panels.css",
        "styles/doctor.css",
        "styles/demo.css",
        "styles/input.css",
    ]

    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
    ]

    # =====================
    # BASE LAYOUT
    # =====================

    def compose(self) -> ComposeResult:
        yield Vertical(
            Banner(),
            Static(id="mode-root"),
            id="container",
        )

        yield Footer(show_command_palette=False, compact=True)

    # =====================
    # MODE SWITCHING
    # =====================

    def set_mode_view(self, view):
        self.root.remove_children()
        self.root.mount(view)

    def on_mount(self):
        self.root = self.query_one("#mode-root")

        if self.start_mode in ("doctor", "doctor-check"):
            self.set_mode_view(DoctorView())

        elif self.start_mode == "demo":
            view = DemoView()
            self.running = True
            self.set_mode_view(view)
            self.call_after_refresh(self.start_spinner)
            self.logs = view.query_one("#logs", Logs)
            self.progress = view.query_one("#progress", ProgressBar)
            self.progress.update(total=100, progress=0)
            subscribe("log", self.on_log)
            subscribe("task", self.on_task)

            self.run_demo()

        else:
            self.set_mode_view(DemoView())

    # =====================
    # EVENT HANDLERS
    # =====================

    def on_log(self, payload):
        self.logs.add(payload["message"])

    def on_task(self, payload):
        step = payload.get("step")
        total = payload.get("total")

        if step is not None and total:
            percent = int((step / total) * 100)
            self.progress.update(progress=percent)

    # =====================
    # DEMO MODE
    # =====================

    async def _run_demo_worker(self):
        await asyncio.to_thread(replay_logs, speed="normal")
        self.running = False

    def run_demo(self):
        self.mode = "demo"
        self.run_worker(self._run_demo_worker, exclusive=True)


    async def handle_command(self, cmd: str):
        if cmd == "demo":
            view = DemoView()
            self.set_mode_view(view)

            self.running = True
            self.call_after_refresh(self.start_spinner)

            self.logs = view.query_one("#logs", Logs)
            self.progress = view.query_one("#progress", ProgressBar)
            self.progress.update(total=100, progress=0)

            subscribe("log", self.on_log)
            subscribe("task", self.on_task)

            self.run_demo()

        elif cmd in ("doctor", "doctor-check"):
            self.set_mode_view(DoctorView())

        elif cmd == "clear":
            if hasattr(self, "logs"):
                self.logs.clear()

        else:
            if hasattr(self, "logs"):
                self.logs.add(f"Unknown command: {cmd}")
    
    def start_spinner(self):
        frames = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])

        async def spin():
            try:
                spinner = self.query_one("#spinner", Static)
            except:
                return
            while self.running:
                spinner.update(f"{next(frames)} Working...")
                await asyncio.sleep(0.1)
            spinner.update("✓ Complete")

        self.run_worker(spin(), exclusive=False)
