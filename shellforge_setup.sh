#!/usr/bin/env bash
set -euo pipefail

############################################
# ShellForge Setup Script
# - Interactive (default) + Automated (-a) modes
# - Idempotent brew installs
# - Ghostty config + OhMyPosh theme + .zshrc install
# - LazyVim starter clone
# - Inject custom Lua configs BEFORE sync (critical)
# - Headless sync uses explicit init.lua
############################################

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

NVIM_DIR="$HOME/.config/nvim"
OHMY_POSH_DIR="$HOME/.config/ohmyposh"
GHOSTTY_DIR="$HOME/.config/ghostty"
GHOSTTY_DEFAULT_DIR="$HOME/Library/Application\ Support/com.mitchellh.ghostty"

SKIP_BREW=false
CLEAN=false
REINSTALL=false
AUTO=false

############################################
# Helpers + CLI UI
############################################

GREEN="\033[1;32m"
BLUE="\033[1;34m"
CYAN="\033[1;36m"
RESET="\033[0m"

SPINNER_FRAMES=("⠋" "⠙" "⠹" "⠸" "⠼" "⠴" "⠦" "⠧" "⠇" "⠏")

ensure_dir() { mkdir -p "$1"; }

die() {
    echo -e "${GREEN}❌ $*${RESET}" 1>&2
    exit 1
}

info() {
    printf "${GREEN}✔ %s${RESET}\n" "$*"
}

# Dynamic progress bar
progress_bar() {
    local pct="$1"
    local msg="$2"
    
    local cols
    cols=$(tput cols 2>/dev/null || echo 80)
    
    local width=$((cols-40))
    [[ $width -lt 20 ]] && width=20
    
    local filled=$((pct * width / 100))
    local empty=$((width - filled))
    
    printf "\r${CYAN}[%3d%%] [" "$pct"
    
    for ((i=0;i<filled;i++)); do printf "█"; done
    for ((i=0;i<empty;i++)); do printf "░"; done
    
    printf "]${RESET} %-40s" "$msg"
}

# Spinner for long tasks
spinner() {
    local pid=$!
    local msg="$1"
    local i=0
    
    while kill -0 "$pid" 2>/dev/null; do
        printf "\r${BLUE}[%s]${RESET} %s" "${SPINNER_FRAMES[i]}" "$msg"
        i=$(((i+1)%${#SPINNER_FRAMES[@]}))
        sleep 0.08
    done
}

# progress() parses existing [xx%] lines and converts them
progress() {
    local msg="$*"
    
    if [[ $msg =~ \[[[:space:]]*([0-9]+)%[[:space:]]*\] ]]; then
        local pct="${BASH_REMATCH[1]}"
        
        local clean
        clean=$(echo "$msg" | sed -E 's/^\[[[:space:]]*[0-9]+%[[:space:]]*\][[:space:]]*//')
        
        progress_bar "$pct" "$clean"
        
        if [[ "$pct" -ge 100 ]]; then
            echo
        fi
    else
        printf "\r%s\n" "$msg"
    fi
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

############################################
# REINSTALL MODE
############################################
if [[ "$REINSTALL" == "true" ]]; then
    progress "[ 1% ] Reinstall mode: wiping Neovim config & state…"
    rm -rf "$NVIM_DIR" "$HOME/.local/share/nvim" "$HOME/.local/state/nvim"
fi

############################################
# BREW + PACKAGE INSTALL
############################################
if [[ "$SKIP_BREW" == "false" ]]; then
    progress "[ 5% ] Checking Homebrew…"
    if ! command -v brew &>/dev/null; then
        progress "Homebrew not found — installing…"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    else
        progress "Homebrew already installed"
    fi
    
    progress "[ 8% ] Updating Homebrew…"
    brew update >/dev/null 2>&1 || true
    
    FORMULAS=(
        git gh neovim oh-my-posh fzf zoxide
        zsh-autosuggestions zsh-syntax-highlighting zsh-completions
        ripgrep fd bat eza lazygit
        dart-sdk
    )
    
    progress "[12%] Installing required Homebrew formulae (idempotent)…"
    for f in "${FORMULAS[@]}"; do
        if brew list "$f" &>/dev/null; then
            progress "  • $f already installed"
        else
            progress "  • Installing $f"
            brew install "$f" >/dev/null 2>&1
        fi
    done
    
    # Buf for protobuf/gRPC tooling
    progress "[16%] Ensuring buf is installed…"
    brew tap bufbuild/buf 2>/dev/null || true
    if brew list buf &>/dev/null; then
        progress "  • buf already installed"
    else
        progress "  • Installing buf…"
        brew install buf
    fi
    
    # Xcode CLT if missing
    progress "[18%] Checking Xcode Command Line Tools…"
    if xcode-select -p &>/dev/null; then
        progress "  • Xcode CLI tools already installed"
    else
        progress "  • Installing Xcode CLI tools…"
        xcode-select --install || true
    fi
    
    # Ghostty cask (safe if already installed)
    progress "[20%] Ensuring Ghostty is installed…"
    if [[ -d "/Applications/Ghostty.app" ]]; then
        progress "  • Ghostty already installed"
    else
        progress "  • Installing Ghostty (cask)…"
        brew install --cask ghostty
    fi
else
    progress "[12%] Skipping Homebrew installs (--skip-brew)"
fi

############################################
# CONFIG FILES (Ghostty + OhMyPosh + .zshrc)
############################################
progress "[25%] Setting up terminal config files…"

ensure_dir "$GHOSTTY_DIR"
ensure_dir "$GHOSTTY_DEFAULT_DIR"
ensure_dir "$OHMY_POSH_DIR"

if [[ -f "$GHOSTTY_DEFAULT_DIR/config" ]]; then
    rm -f "$GHOSTTY_DEFAULT_DIR/config"
    progress "  • Removed default ghostty config file from $GHOSTTY_DIR/config"
fi

# Ghostty config (repo root file named: config)
if [[ -f "$REPO_DIR/ghostty_config" ]]; then
    cp -f "$REPO_DIR/ghostty_config" "$GHOSTTY_DIR/config"
    progress "  • Ghostty config installed → $GHOSTTY_DIR/config"
else
    progress "  • Ghostty config file not found in repo root (expected: ./config) — skipping"
fi

# OhMyPosh theme (repo root file named: shellforge.omp.json)
if [[ -f "$REPO_DIR/shellforge.omp.json" ]]; then
    cp -f "$REPO_DIR/shellforge.omp.json" "$OHMY_POSH_DIR/shellforge.omp.json"
    progress "  • OhMyPosh theme installed → $OHMY_POSH_DIR/shellforge.omp.json"
else
    progress "  • OhMyPosh theme not found in repo root (expected: ./shellforge.omp.json) — skipping"
fi

# .zshrc (repo root file named: .zshrc)
if [[ -f "$REPO_DIR/.zshrc" ]]; then
    progress "  • Installing .zshrc"
    if [[ -f "$HOME/.zshrc" ]]; then
        if [[ "$CLEAN" == "true" ]]; then
            rm -f "$HOME/.zshrc"
            progress "    - Removed existing ~/.zshrc (--clean)"
        else
            mv -f "$HOME/.zshrc" "$HOME/.zshrc_old"
            progress "    - Backed up existing ~/.zshrc → ~/.zshrc_old"
        fi
    fi
    cp -f "$REPO_DIR/.zshrc" "$HOME/.zshrc"
    progress "    - Copied repo .zshrc → ~/.zshrc"
else
    progress "  • No .zshrc found in repo root — skipping"
fi

# Ensure GHOSTTY_CONFIG_HOME is defined so Ghostty uses ~/.config/ghostty
if ! grep -q "export GHOSTTY_CONFIG_HOME" "$HOME/.zshrc"; then
    {
        echo ""
        echo "# Set Ghostty config dir to ~/.config/ghostty"
        echo "export GHOSTTY_CONFIG_HOME=\"\$HOME/.config/ghostty\""
    } >> "$HOME/.zshrc"
    progress "  • Added GHOSTTY_CONFIG_HOME to ~/.zshrc"
else
    progress "  • GHOSTTY_CONFIG_HOME already defined in ~/.zshrc — skipping"
fi

############################################
# LAZYVIM STARTER (clone if missing)
############################################
progress "[40%] Ensuring LazyVim starter exists…"
if [[ ! -d "$NVIM_DIR" ]]; then
    progress "  • Cloning LazyVim starter to $NVIM_DIR …"
    git clone https://github.com/LazyVim/starter "$NVIM_DIR" >/dev/null 2>&1
    rm -rf "$NVIM_DIR/.git"
    progress "  • LazyVim starter installed"
else
    progress "  • $NVIM_DIR already exists — leaving as-is"
fi

############################################
# INSTALL CUSTOM init.lua (override)
############################################

CUSTOM_INIT_SRC="$REPO_DIR/nvim_configs/init.lua"
CUSTOM_INIT_DST="$NVIM_DIR/init.lua"

if [[ -f "$CUSTOM_INIT_SRC" ]]; then
    progress "[50%] Installing custom init.lua…"
    
    # Backup LazyVim's default init.lua
    if [[ -f "$CUSTOM_INIT_DST" ]]; then
        cp -f "$CUSTOM_INIT_DST" "$CUSTOM_INIT_DST.lazybak"
        progress "  • Backed up default init.lua → init.lua.lazybak"
    fi
    
    # Copy custom init.lua from repo
    cp -f "$CUSTOM_INIT_SRC" "$CUSTOM_INIT_DST"
    progress "  • Custom init.lua installed → $CUSTOM_INIT_DST"
else
    progress "[50%] No custom init.lua found at $CUSTOM_INIT_SRC — skipping"
fi


############################################
# APPLY CUSTOM NVIM LUA CONFIGS BEFORE SYNC (critical)
############################################
progress "[55%] Applying Neovim custom Lua configs BEFORE plugin sync…"

LUA_SRC="$REPO_DIR/nvim_configs/lua_configs"
LUA_DST="$NVIM_DIR/lua"

if [[ -d "$LUA_SRC" ]]; then
    ensure_dir "$LUA_DST"
    
    # 1) Plugin specs
    if [[ -d "$LUA_SRC/plugins" ]]; then
        ensure_dir "$LUA_DST/plugins"
        rsync -a "$LUA_SRC/plugins/" "$LUA_DST/plugins/"
        progress "  • Updated plugin specs → $LUA_DST/plugins"
    else
        progress "  • No plugins dir found at $LUA_SRC/plugins — skipping"
    fi
    
    # 2) Config dir (merge + backup any files we overwrite)
    if [[ -d "$LUA_SRC/config" ]]; then
        ensure_dir "$LUA_DST/config"
        
        # backup only the files we're about to overwrite
        for f in "$LUA_SRC/config/"*.lua; do
            [[ -e "$f" ]] || continue
            base="$(basename "$f")"
            if [[ -f "$LUA_DST/config/$base" ]]; then
                if [[ "$CLEAN" == "true" ]]; then
                    rm -f "$LUA_DST/config/$base"
                    progress "    - Overwriting $base (--clean)"
                else
                    cp -f "$LUA_DST/config/$base" "$LUA_DST/config/${base}.backup"
                    progress "    - Backed up $base → ${base}.backup"
                fi
            fi
        done
        
        rsync -a "$LUA_SRC/config/" "$LUA_DST/config/"
        progress "  • Merged config files → $LUA_DST/config (backups created where overwritten)"
    else
        progress "  • No config dir found at $LUA_SRC/config — skipping"
    fi
else
    progress "  • No custom Lua source dir found at $LUA_SRC — skipping"
fi

############################################
# PLUGIN INSTALL / SYNC STEP
############################################
if [[ "$AUTO" == "true" ]]; then
    progress "[70%] Automated mode (-a): Running Lazy sync + lock headlessly…"
    # Use explicit init.lua to avoid any ambiguity
    nvim --headless -u "$NVIM_DIR/init.lua" "+Lazy! sync" "+Lazy! lock" +qa
    progress "[85%] Headless Lazy sync complete"
else
    progress "[70%] Interactive mode: Launching Neovim…"
    progress "     • In Neovim, run :Lazy sync if it doesn’t auto-run"
    progress "     • Quit Neovim with :qa when done"
    nvim
    progress "[85%] Returned from Neovim"
fi

############################################
# VERIFY (lockfile check only in AUTO; skip in interactive)
############################################
if [[ "$AUTO" == "true" ]]; then
    if [[ -f "$NVIM_DIR/lazy-lock.json" ]]; then
        progress "[90%] Verified: lazy-lock.json exists"
    else
        die "LazyVim sync finished but lazy-lock.json is missing. Open nvim and run :Lazy lock"
    fi
else
    progress "[90%] Interactive mode: skipping lockfile verification"
fi

############################################
# DONE
############################################
progress "[100%] ShellForge setup complete!"
echo
echo "🎉 ShellForge + LazyVim installation finished!"
echo "📌 Notes:"
echo "   • Restart terminal or run: exec zsh"
echo "   • Open Neovim with: nvim"
echo "   • Neo-tree: <leader>e (toggle), <leader>fe (focus), <leader>fr (reveal)"
echo