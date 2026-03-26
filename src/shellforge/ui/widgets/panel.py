from textual.containers import Container


class Panel(Container):
    def __init__(self, title: str, *children, **kwargs):
        super().__init__(*children, **kwargs)
        self.border_title = title
        self.border_title_align = "center"