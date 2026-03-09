from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
HOME = Path.home()

# Fetch all(iterable) Configuration file paths
OMP_SOURCE = REPO_ROOT / "shellforge.omp.json"
GHOSTTY_SOURCE = REPO_ROOT / "ghostty_config"
NVIM_SOURCE = REPO_ROOT / "nvim_configs"
ZSHRC_SOURCE = REPO_ROOT / ".zshrc"

#  Set all configuration file targets
OMP_TARGET = HOME / ".config" / "oh-my-posh" / "themes" / "shellforge.omp.json"
GHOSTTY_TARGET = HOME / ".config" / "ghostty" / "config"
NVIM_TARGET = HOME / ".config" / "nvim" / "config"
ZSHRC_TARGET = HOME / ".zshrc"