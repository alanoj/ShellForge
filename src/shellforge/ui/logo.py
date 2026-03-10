import shutil
import subprocess
import textwrap
from pathlib import Path
from rich.console import Console
from importlib.resources import files

console = Console()

def show_logo() -> None:
    console.clear()

    # Detect Docker (kitty graphics usually unsupported there)
    running_in_docker = Path("/.dockerenv").exists()

    logo = files("shellforge.assets").joinpath("logo.png")
    logo_path = Path(str(logo))

    image_rendered = False
    cols, rows = shutil.get_terminal_size()
    width = int(cols * 0.7)
    height = 6

    if not running_in_docker and logo_path.exists():
        try:
            subprocess.run(
                [
                    "kitten",
                    "icat",
                    "--align=center",
                    "--place",
                    f"{width}x{height}@{(cols-width)//2}x0",
                    str(logo_path),
                ],
                check=False,
            )
            print("\n" * (height + 1))
            image_rendered = True
        except Exception:
            image_rendered = False

    # ASCII fallback if image rendering failed
    if not image_rendered:
        ascii_logo = textwrap.dedent("""
███████╗██╗  ██╗███████╗██╗     ██╗     ███████╗ ██████╗ ██████╗  ██████╗ ███████╗
██╔════╝██║  ██║██╔════╝██║     ██║     ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
███████╗███████║█████╗  ██║     ██║     █████╗  ██║   ██║██████╔╝██║  ███╗█████╗
╚════██║██╔══██║██╔══╝  ██║     ██║     ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝
███████║██║  ██║███████╗███████╗███████╗██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
""")
        console.print(f"[bold #90DBE5]{ascii_logo}[/bold #90DBE5]", justify="center")

    # Subtitle
    console.print(
        "[bold #90DBE5]  ShellForge — Terminal Environment Bootstrap[/bold #90DBE5]\n",
        justify="center",
    )