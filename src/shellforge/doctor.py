from dataclasses import dataclass
import shutil
from rich.console import Console
from rich.table import Table

console = Console()

@dataclass
class CheckResult:
    name: str
    found: bool
    path: str | None
    
REQUIRED_TOOLS = ["git", "zsh", "nvim"]
OPTIONAL_TOOLS = ["brew", "oh-my-posh"]

def check_tool(name:str) -> CheckResult:
    path = shutil.which(name)
    return CheckResult(name=name, found=path is not None, path=path)

def run_checks(verbose: bool = False) -> None:
    table = Table(title="ShellForge Doctor")
    table.add_column("Tool")
    table.add_column("Status")
    table.add_column("Resolved Path")
    
    for tool in REQUIRED_TOOLS + OPTIONAL_TOOLS:
        result = check_tool(tool)
        status = "[bold cyan3]\uf05d[/bold cyan3] Found" if result.found else "[bold red3]\uea87[/bold red3] missing"
        resolved = result.path if result.path else "-"
        table.add_row(result.name, status, resolved)
    
    console.print(table)
    
    if verbose:
        console.print("[bold cyan]Doctor run complete.[/bold cyan]")