#!/usr/bin/env bash
set -euo pipefail

############################################
# ShellForge Setup Script
############################################

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

NVIM_DIR="$HOME/.config/nvim"
OHMY_POSH_DIR="$HOME/.config/ohmyposh"
GHOSTTY_DIR="$HOME/.config/ghostty"
GHOSTTY_DEFAULT_DIR="$HOME/Library/Application Support/com.mitchellh.ghostty"

SKIP_BREW=false
CLEAN=false
REINSTALL=false
AUTO=false

############################################
# Colors
############################################

GREEN="\033[1;32m"
BLUE="\033[1;34m"
CYAN="\033[1;36m"
YELLOW="\033[1;33m"
RESET="\033[0m"

############################################
# Banner
############################################

banner() {
    printf "%b\n" "$CYAN"
    printf "███████╗██╗  ██╗███████╗██╗     ██╗      ███████╗ ██████╗ ██████╗  ██████╗ ███████╗\n"
    printf "██╔════╝██║  ██║██╔════╝██║     ██║      ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝\n"
    printf "███████╗███████║█████╗  ██║     ██║      █████╗  ██║   ██║██████╔╝██║  ███╗█████╗  \n"
    printf "╚════██║██╔══██║██╔══╝  ██║     ██║      ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝  \n"
    printf "███████║██║  ██║███████╗███████╗███████╗ ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗\n"
    printf "╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝ ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝\n"
    printf "%b\n" "$RESET"
    
    printf "%bDeveloper Environment Installer%b\n\n" "$CYAN" "$RESET"
}

############################################
# Step Counter
############################################

TOTAL_STEPS=8
CURRENT_STEP=0

next_step() {
    CURRENT_STEP=$((CURRENT_STEP+1))
    printf "\n%b[%d/%d]%b %s\n" "$CYAN" "$CURRENT_STEP" "$TOTAL_STEPS" "$RESET" "$1"
}

############################################
# UI Helpers
############################################

section() {
    printf "\n%b━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━%b\n" "$BLUE" "$RESET"
    printf "%b▶ %s%b\n" "$BLUE" "$1" "$RESET"
    printf "%b━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━%b\n" "$BLUE" "$RESET"
}

step() { printf "  %b✔%b %s\n" "$GREEN" "$RESET" "$1"; }
task() { printf "  %b➜%b %s\n" "$CYAN" "$RESET" "$1"; }
warn() { printf "  %b⚠%b %s\n" "$YELLOW" "$RESET" "$1"; }

die() {
    printf "%b❌ %s%b\n" "$YELLOW" "$1" "$RESET"
    exit 1
}

ensure_dir() { mkdir -p "$1"; }

############################################
# Spinner
############################################

spinner() {
    local pid=$1
    local msg="$2"
    local spin='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    local i=0
    
    tput civis
    
    while kill -0 "$pid" 2>/dev/null; do
        i=$(( (i+1) %10 ))
        printf "\r%b[%s]%b %s" "$BLUE" "${spin:$i:1}" "$RESET" "$msg"
        sleep .1
    done
    
    tput cnorm
    printf "\r%b✔%b %s\n" "$GREEN" "$RESET" "$msg"
}

run_with_spinner() {
    local msg="$1"
    shift
    
    "$@" >/dev/null 2>&1 &
    local pid=$!
    
    spinner "$pid" "$msg"
    wait "$pid"
}

############################################
# Unified Progress Bar Renderer
############################################

progress_block() {
    
    local pct=$1
    local pkg="$2"
    
    local cols
    cols=$(tput cols 2>/dev/null || echo 80)
    
    local width=$((cols-30))
    [[ $width -lt 20 ]] && width=20
    
    local filled=$((pct * width / 100))
    local empty=$((width - filled))
    
    local spin='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
    local s=$((RANDOM % 10))
    
    printf "\033[3A"        # move cursor up 3 lines
    printf "\033[2K\r%b[%s]%b Installing packages\n" "$BLUE" "${spin:$s:1}" "$RESET"
    
    printf "\033[2K\r["
    for ((i=0;i<filled;i++)); do printf "█"; done
    for ((i=0;i<empty;i++)); do printf "░"; done
    printf "] %d%%\n" "$pct"
    
    printf "\033[2K\rCurrent: %s\n" "$pkg"
    
}

############################################
# ARGUMENT PARSING
############################################

for arg in "$@"; do
    case "$arg" in
        -b|--skip-brew) SKIP_BREW=true ;;
        -c|--clean) CLEAN=true ;;
        --reinstall) REINSTALL=true ;;
        -a) AUTO=true ;;
        *)
            echo "Unknown argument: $arg"
            echo "Usage: $0 [-a] [--skip-brew] [-c|--clean] [--reinstall]"
            exit 1
        ;;
    esac
done

banner

############################################
# Reinstall Mode
############################################

if [[ "$REINSTALL" == "true" ]]; then
    next_step "Reinstall Mode"
    task "Removing existing Neovim state"
    
    rm -rf "$NVIM_DIR"
    rm -rf "$HOME/.local/share/nvim"
    rm -rf "$HOME/.local/state/nvim"
    
    step "Neovim reset complete"
fi

############################################
# Brew Setup
############################################

if [[ "$SKIP_BREW" == "false" ]]; then
    
    next_step "Homebrew Setup"
    
    if ! command -v brew &>/dev/null; then
        run_with_spinner \
        "Installing Homebrew" \
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
        step "Homebrew already installed"
    fi
    
    run_with_spinner "Updating Homebrew" brew update
    
    FORMULAS=(
        git gh neovim oh-my-posh fzf zoxide
        zsh-autosuggestions zsh-syntax-highlighting zsh-completions
        ripgrep fd bat eza lazygit
        dart-sdk
    )
    
    section "Installing Packages"
    echo
    echo "Installing packages"
    echo
    echo
    
    total=${#FORMULAS[@]}
    count=0
    
    for f in "${FORMULAS[@]}"; do
        
        count=$((count + 1))
        pct=$((count * 100 / total))
        
        if ! brew list "$f" &>/dev/null; then
            
            brew install "$f" >/dev/null 2>&1 &
            pid=$!
            
            progress_block "$pct" "$f"
            
            wait "$pid"
            
        else
            progress_block "$pct" "Skipping: $f"
            sleep 0.2
        fi
        
    done
    
    progress_block 100 "All packages installed"
    printf "\n"
    
    ############################################
    # Buf
    ############################################
    
    next_step "Buf Setup"
    
    brew tap bufbuild/buf >/dev/null 2>&1 || true
    
    if brew list buf &>/dev/null; then
        step "buf already installed"
    else
        run_with_spinner "Installing buf" brew install buf
    fi
    
    ############################################
    # Xcode CLI
    ############################################
    
    next_step "Xcode CLI Tools"
    
    if xcode-select -p &>/dev/null; then
        step "Xcode CLI tools already installed"
    else
        warn "Installing Xcode CLI tools"
        xcode-select --install || true
    fi
    
    
else
    next_step "Skipping Brew Installs"
    warn "--skip-brew enabled"
fi

############################################
# Ghostty
############################################

next_step "Ghostty Terminal"

if [[ -d "/Applications/Ghostty.app" ]]; then
    step "Ghostty already installed"
else
    if [[ "$SKIP_BREW" == "false" ]]; then
        run_with_spinner "Installing Ghostty" brew install --cask ghostty
    else
        warn "Ghostty install skipped because --skip-brew is enabled"
    fi
fi

############################################
# Config Files
############################################

next_step "Installing Config Files"

ensure_dir "$GHOSTTY_DIR"
ensure_dir "$GHOSTTY_DEFAULT_DIR"
ensure_dir "$OHMY_POSH_DIR"

if [[ -f "$GHOSTTY_DEFAULT_DIR/config" ]]; then
    rm -f "$GHOSTTY_DEFAULT_DIR/config"
    step "Removed default ghostty config"
fi

if [[ -f "$REPO_DIR/ghostty_config" ]]; then
    cp -f "$REPO_DIR/ghostty_config" "$GHOSTTY_DIR/config"
    step "Ghostty config installed"
else
    warn "Ghostty config missing"
fi

if [[ -f "$REPO_DIR/shellforge.omp.json" ]]; then
    cp -f "$REPO_DIR/shellforge.omp.json" "$OHMY_POSH_DIR/shellforge.omp.json"
    step "OhMyPosh theme installed"
else
    warn "OhMyPosh theme missing"
fi

############################################
# ZSHRC
############################################

next_step "Installing .zshrc"

if [[ -f "$REPO_DIR/.zshrc" ]]; then
    
    if [[ -f "$HOME/.zshrc" ]]; then
        
        if [[ "$CLEAN" == "true" ]]; then
            rm "$HOME/.zshrc"
            step "Removed old .zshrc (--clean)"
        else
            mv "$HOME/.zshrc" "$HOME/.zshrc_old"
            step "Backed up old .zshrc"
        fi
        
    fi
    
    cp "$REPO_DIR/.zshrc" "$HOME/.zshrc"
    
    step ".zshrc installed"
    
else
    warn ".zshrc missing"
fi

############################################
# Neovim Setup
############################################

next_step "Neovim Setup"

if [[ ! -d "$NVIM_DIR" ]]; then
    
    run_with_spinner \
    "Cloning LazyVim starter" \
    git clone https://github.com/LazyVim/starter "$NVIM_DIR"
    
    rm -rf "$NVIM_DIR/.git"
    
    step "LazyVim starter installed"
    
else
    step "Neovim config already exists"
fi

############################################
# init.lua
############################################

CUSTOM_INIT_SRC="$REPO_DIR/nvim_configs/init.lua"
CUSTOM_INIT_DST="$NVIM_DIR/init.lua"

if [[ -f "$CUSTOM_INIT_SRC" ]]; then
    
    task "Installing custom init.lua"
    
    if [[ -f "$CUSTOM_INIT_DST" ]]; then
        cp "$CUSTOM_INIT_DST" "$CUSTOM_INIT_DST.lazybak"
        step "Backed up existing init.lua"
    fi
    
    cp "$CUSTOM_INIT_SRC" "$CUSTOM_INIT_DST"
    
    step "Custom init.lua installed"
    
else
    warn "init.lua missing"
fi

############################################
# Lua configs
############################################

next_step "Installing Lua Configs"

LUA_SRC="$REPO_DIR/nvim_configs/lua_configs"
LUA_DST="$NVIM_DIR/lua"

if [[ -d "$LUA_SRC" ]]; then
    
    ensure_dir "$LUA_DST"
    
    rsync -a "$LUA_SRC/" "$LUA_DST/"
    
    step "Lua configs installed"
    
else
    warn "Lua configs missing"
fi

############################################
# Lazy Sync
############################################

next_step "Neovim Plugin Sync"

if [[ "$AUTO" == "true" ]]; then
    
    run_with_spinner \
    "Running Lazy sync" \
    nvim --headless -u "$NVIM_DIR/init.lua" "+Lazy! sync" "+Lazy! lock" +qa
    
    step "Plugins installed"
    
else
    warn "Interactive mode — launching Neovim"
    echo "Run :Lazy sync inside Neovim"
    nvim
fi

############################################
# Done
############################################

section "Installation Complete"

echo "🎉 ShellForge installation finished!"
echo
echo "Next steps:"
echo "  exec zsh"
echo "  nvim"
echo
echo
echo "Reloading shell to apply Oh My Posh and zsh config..."
exec zsh