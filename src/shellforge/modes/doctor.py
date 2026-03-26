import os
import shutil

ESSENTIAL_TOOLS = ["brew", "git"]
OPTIONAL_TOOLS = ["nvim", "oh-my-posh", "zsh"]
TERMINALS = ["ghostty", "kitty", "alacritty", "warp", "wezterm", "iterm"]


def check_tool(name: str):
    return shutil.which(name)


def get_terminal():
    term_env = os.environ.get("TERM_PROGRAM", "").lower()

    for term in TERMINALS:
        if term in term_env:
            return term

    return None


def run_checks():
    results = []

    for tool in ESSENTIAL_TOOLS:
        results.append((tool, bool(check_tool(tool)), "required"))

    for tool in OPTIONAL_TOOLS:
        results.append((tool, bool(check_tool(tool)), "optional"))

    return {"terminal": get_terminal(), "tools": results}
