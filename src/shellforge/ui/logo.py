import os
import shutil
import base64
from pathlib import Path
from rich.console import Group
from rich.console import Console
from rich.align import Align
from rich.text import Text

console = Console()

ROOT = Path(__file__).resolve().parents[3]
ASSETS_DIR = ROOT / "docs" / "assets"


def supports_graphics():
    return os.environ.get("TERM_PROGRAM", "").lower() in ["ghostty", "kitty", "wezterm"]


def _encode_image(path: Path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _render_image(encoded: str, width_px: int, height_px: int):
    print(f"\033_Gf=100,a=T,s={width_px},v={height_px};{encoded}\033\\", flush=True)


def show_logo():
    banner = ASSETS_DIR / "shellforge-banner.png"
    if supports_graphics():
        try:
            cols, rows = shutil.get_terminal_size()

            cell_w = 8
            cell_h = 16

            banner_width = int(cols * cell_w * 0.55)
            banner_height = int(rows * cell_h * 0.18)

            encoded_banner = _encode_image(banner)

            padding = " " * int((cols - (banner_width // cell_w)) / 2)

            print(padding, end="")
            _render_image(encoded_banner, banner_width, banner_height)
            subtitle = Text(
                "\uf013 ShellForge — Terminal Environment Bootstrap",
                style="bold #90DBE5"
            )

            console.print(Align.center(subtitle))
            print()
            return

        except Exception as e:
            print("IMAGE RENDER ERROR:", e)

    _render_ascii()


def _render_ascii():
    ascii_logo = r"""
███████╗██╗  ██╗███████╗██╗     ██╗     ███████╗ ██████╗ ██████╗  ██████╗ ███████╗
██╔════╝██║  ██║██╔════╝██║     ██║     ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
███████╗███████║█████╗  ██║     ██║     █████╗  ██║   ██║██████╔╝██║  ███╗█████╗
╚════██║██╔══██║██╔══╝  ██║     ██║     ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝
███████║██║  ██║███████╗███████╗███████╗██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
"""

    console.print(Align.center(f"[bold #90DBE5]{ascii_logo}[/bold #90DBE5]"))

    subtitle = Text(
        "⚙ ShellForge — Terminal Environment Bootstrap",
        style="bold #90DBE5"
    )

    console.print(Align.center(subtitle))