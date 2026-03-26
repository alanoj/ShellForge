from textual.widgets import Input


class CommandInput(Input):

    def on_mount(self):
        self.focus()
        self.cursor_blink = True
        self.placeholder = "› Enter command..."

    def on_show(self):
        self.focus()

    async def on_input_submitted(self, event: Input.Submitted):
        command = event.value.strip()
        self.value = ""

        app = self.app  # type: ignore

        if hasattr(app, "handle_command"):
            await app.handle_command(command)  # type: ignore