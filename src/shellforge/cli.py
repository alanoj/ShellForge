import typer
from shellforge import doctor, installer
from shellforge.bootstrap import bootstrap as bootstrap_cmd
from shellforge.ui.renderer import Renderer
from shellforge.runtime.replay import replay_logs
from shellforge.ui.logo import show_logo

app = typer.Typer(help="ShellForge CLI")


@app.command()
def doctor_check(verbose: bool = False):
    show_logo()
    doctor.run_checks()


@app.command()
def install(dry_run: bool = False):
    renderer = Renderer()
    renderer.run(lambda: installer.install(dry_run=dry_run))


@app.command()
def demo(
    speed: str = typer.Option("normal", "--speed", help="fast | normal | slow"),
):
    show_logo()  # render banner first
    renderer = Renderer()
    renderer.run(lambda: replay_logs(speed=speed))


@app.command()
def bootstrap(
    dry_run: bool = typer.Option(False, "--dry-run"),
    compact: bool = typer.Option(False, "--compact"),
    terminal: str = typer.Option("ghostty", "--terminal"),
    speed: str = typer.Option("normal", "--speed", help="fast | normal | slow"),
    skip_terminal: bool = typer.Option(False, "--skip-terminal"),
    record: bool = typer.Option(False, "--record", help="Record logs for demo"),
):
    if record:
        print("Starting log recording...")

        bootstrap_cmd(
            dry_run=dry_run,
            compact=compact,
            speed=speed,
            terminal=terminal,
            skip_terminal=skip_terminal,
            record=True
        )

        print("Done")
        return

    renderer = Renderer()
    renderer.run(lambda: bootstrap_cmd(
        dry_run=dry_run,
        compact=compact,
        speed=speed,
        terminal=terminal,
        skip_terminal=skip_terminal,
        record=False
    ))


@app.command()
def version():
    print("shellforge 0.1.0")


def main():
    app()