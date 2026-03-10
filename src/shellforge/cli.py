from typing import Optional
import typer
from shellforge import doctor, installer
import platform, subprocess, shutil

shellforge = typer.Typer(help="ShellForge Python CLI")

@shellforge.command()
def doctor_check(verbose: bool = False) -> None:
    """Run system health checks"""
    doctor.run_checks(verbose=verbose)


@shellforge.command()
def install(dry_run: bool = False) -> None:
    """Deploy ShellForge configs."""
    installer.install(dry_run=dry_run)


@shellforge.command()
def bootstrap(
    dry_run: bool = typer.Option(False, "--dry-run", help="Run without making changes"),
    compact: bool = typer.Option(False, "--compact", help="Hide install logs"),
):
    installer.bootstrap(dry_run=dry_run, compact=compact)


@shellforge.command()
def version() -> None:
    """Print CLI Version."""
    print("shellforge 0.1.0")
    

def main() -> None:
    shellforge()


