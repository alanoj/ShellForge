import typer
from shellforge.ui.app import ShellForgeApp

app = typer.Typer()


@app.command()
def demo():
    ShellForgeApp(start_mode="demo").run()


@app.command()
def doctor_check():
    ShellForgeApp(start_mode="doctor").run()


@app.command()
def install():
    ShellForgeApp(start_mode="install").run()


@app.command()
def bootstrap():
    ShellForgeApp(start_mode="bootstrap").run()


def main():
    app()