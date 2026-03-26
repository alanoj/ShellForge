from pathlib import Path
from textual.containers import Vertical, Center
from textual.widgets import Static
from textual_image.widget import Image


ASSET = Path(__file__).resolve().parents[4] / "docs" / "assets" / "shellforge-banner.png"
COLOR = "#90DBE5"

class Banner(Vertical):
    def compose(self):
        yield Center(
            Image(
                str(ASSET),
                id="banner-image"
            )
        )
        yield Center(
            Static(
                "\uf013 ShellForge — Terminal Environment Bootstrap",
                id="subtitle"
            )
        )