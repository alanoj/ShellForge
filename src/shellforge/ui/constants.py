from shutil import get_terminal_size

PANEL_COLOR = "#90DBE5"
PANEL_TITLE_STYLE = "bold #90DBE5"


def get_content_width():
    return int(get_terminal_size().columns * 0.75)


def center_renderable(renderable):
    from rich.align import Align
    return Align.center(renderable)