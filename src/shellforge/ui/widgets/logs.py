from textual.widgets import Static
from textual.reactive import reactive


class Logs(Static):
    lines = reactive([])

    def add(self, message: str):
        self.lines.append(message)
        self.update("\n".join(self.lines[-20:]))
        self.refresh(layout=True)

    def clear(self):
        self.lines = []
        self.update("")