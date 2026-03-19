import shutil
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from shellforge.ui.constants import get_content_width

console = Console()

ESSENTIAL_TOOLS = ["brew", "git"]
OPTIONAL_TOOLS = ["nvim", "oh-my-posh", "zsh"]
TERMINALS = ["ghostty", "kitty", "alacritty", "warp", "wezterm", "iterm"]


def check_tool(name: str):
    return shutil.which(name)


def get_terminal():
    for term in TERMINALS:
        if shutil.which(term) or shutil.which(term.lower()) or shutil.which(term.upper()):
            return term
    return None


def build_table():
    table = Table.grid(padding=(0, 2))

    # ESSENTIAL
    for tool in ESSENTIAL_TOOLS:
        path = check_tool(tool)
        if path:
            table.add_row(f"[bold cyan3][/bold cyan3] {tool}", "[cyan3]Found[/cyan3]", path)
        else:
            table.add_row(f"[bold red3][/bold red3] {tool}", "[red]Missing[/red]", "-")

    # OPTIONAL
    for tool in OPTIONAL_TOOLS:
        path = check_tool(tool)
        if path:
            table.add_row(f"[bold cyan3][/bold cyan3] {tool}", "[cyan3]Found[/cyan3]", path)
        else:
            table.add_row(f"[yellow]󱥸[/yellow] {tool}", "[yellow]Optional[/yellow]", "-")

    return table


def build_legend():
    width = get_content_width()
    legend = Table.grid(padding=(0, 2))
    legend.add_row("[bold cyan3][/bold cyan3]", "Found / OK")
    legend.add_row("[yellow]󱥸[/yellow]", "Optional / Missing")
    legend.add_row("[bold red3][/bold red3]", "Required / Missing")
    return Panel(legend, title="Legend", border_style="#90DBE5", width=width)


def run_checks(verbose: bool = False):

    terminal = get_terminal()
    width = get_content_width()

    if terminal:
        formatted = terminal.capitalize()

        if terminal.lower() == "ghostty":
            formatted = f"[dodger_blue1]󰊠 {formatted}[/dodger_blue1]"

        terminal_line = f"[bold green]Using terminal:[/bold green] [cyan]{formatted}[/cyan]"
    else:
        terminal_line = "[bold red]No supported terminal found (ghostty / kitty / alacritty)[/bold red]"

    table = build_table()

    panel = Panel(
        table,
        title="ShellForge Doctor",
        border_style="#90DBE5",
        expand=True,
        width=width,
    )


    console.print(Panel(terminal_line, border_style="#90DBE5", width=width))
    console.print(panel)
    console.print(build_legend())

    if verbose:
        console.print("\n[bold cyan]Doctor run complete.[/bold cyan]")