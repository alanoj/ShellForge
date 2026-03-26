from textual.containers import Horizontal
from textual.containers import Vertical, Center
from textual.widgets import Static
from textual.widgets import DataTable
from shellforge.ui.widgets.panel import Panel
from shellforge.modes.doctor import run_checks
from shellforge.modes.doctor import check_tool
from shellforge.ui.widgets.input import CommandInput


class DoctorView(Vertical):
    found = "#00d7af"
    missing = "#d70000"
    optional = "#ffaf00"

    def compose(self):
        results = run_checks()

        raw_terminal = results["terminal"]
        if raw_terminal:
            terminal_name = raw_terminal.capitalize()

            if raw_terminal == "ghostty":
                terminal = f"[bold #90DBE5]󱙝 {terminal_name}[/bold #90DBE5]"
            else:
                terminal = f"[bold #00d7af]{terminal_name}[/bold #00d7af]"
        else:
            terminal = "[bold #d70000]⚠ Unknown Terminal[/bold #d70000]"

        yield Center(
            Panel(
                "Environment",
                Static(
                    f"[bold]Terminal:[/bold] {terminal}",
                    expand=True,
                    classes="center-text",
                ),
                classes="panel doctor-mode-panel terminal-env-panel",
            )
        )

        table = DataTable()
        table.add_columns("Tool", "Status", "Path")
        table.zebra_stripes = False
        table.show_row_labels = False
        table.show_cursor = False
        table.show_header = False

        for tool, found, level in results["tools"]:
            # Color tool name instead of separate column
            if not found:
                tool_label = f"[bold {self.missing}]{tool}[/bold {self.missing}]"
            elif level == "optional":
                tool_label = f"[bold {self.optional}]{tool}[/bold {self.optional}]"
            else:
                tool_label = f"[bold #ffffff]{tool}[/bold #ffffff]"

            if found:
                status = f"[bold {self.found}] Found[/bold {self.found}]"
            else:
                status = f"[bold {self.missing}] Missing[/bold {self.missing}]"

            path = check_tool(tool) or "-"

            table.add_row(tool_label, status, path)

        yield Center(
            Panel(
                "Environment Checks",
                table,
                classes="panel doctor-mode-panel results-panel",
            )
        )

        yield Center(
            Panel(
                "Legend",
                Horizontal(
                    Static(f"[bold {self.found}] Found[/bold {self.found}]"),
                    Static(f"[bold {self.optional}]󱥸 Optional[/bold {self.optional}]"),
                    Static(f"[bold {self.missing}] Missing[/bold {self.missing}]"),
                    classes="legend-row",
                ),
                classes="panel doctor-mode-panel",
            )
        )

        yield Center(
            CommandInput(placeholder="Enter command (e.g. demo, doctor, clear)...")
        )
