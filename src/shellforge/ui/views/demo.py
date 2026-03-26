from textual.containers import Vertical, Horizontal
from textual.widgets import ProgressBar, Static
from shellforge.ui.widgets.logs import Logs
from shellforge.ui.widgets.input import CommandInput


class DemoView(Vertical):
    def compose(self):
        yield Horizontal(
            Static("⠋", id="spinner"),
            ProgressBar(total=100, id="progress"),
            id="progress-row",
            classes="panel"
        )

        yield Logs(id="logs", classes="panel")
        yield CommandInput(id="input", classes="panel")