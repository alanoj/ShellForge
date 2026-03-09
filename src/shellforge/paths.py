from pathlib import Path
from importlib.resources import files

# User home directory
HOME = Path.home()

# Package assets directory (works when installed via pipx)
ASSETS = files("shellforge.assets")

# Source configuration files bundled with the package
OMP_SOURCE = ASSETS / "shellforge.omp.json"
GHOSTTY_SOURCE = ASSETS / "ghostty_config"
NVIM_SOURCE = ASSETS / "nvim_configs"
ZSHRC_SOURCE = ASSETS / ".zshrc"

# Target install locations
OMP_TARGET = HOME / ".config" / "oh-my-posh" / "themes" / "shellforge.omp.json"
GHOSTTY_TARGET = HOME / ".config" / "ghostty" / "config"
NVIM_TARGET = HOME / ".config" / "nvim"
ZSHRC_TARGET = HOME / ".zshrc"