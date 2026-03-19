export PATH="$HOME/bin:/usr/local/bin:/Library/TeX/texbin:$PATH"
# Set XDG config dir so Ghostty uses ~/.config/ghostty
export XDG_CONFIG_HOME="$HOME/.config"
export GHOSTTY_CONFIG_HOME="$HOME/.config/ghostty"
# ESP-IDF (optional – only if installed)
export IDF_TOOLS_PATH="$HOME/.espressif"
export PATH="$IDF_TOOLS_PATH/tools/xtensa-esp-elf/esp-14.2.0_20241119/xtensa-esp-elf/bin:$PATH"
export PATH="$IDF_TOOLS_PATH/tools/openocd-esp32/v0.12.0-esp32-20241016/openocd-esp32/bin:$PATH"

export TERM="xterm-256color"
export POSH_THEME_RELOAD=true
########################################
# Homebrew Environment
########################################
if command -v brew &>/dev/null; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
fi

########################################
# Zinit Plugin Manager
########################################
ZINIT_HOME="${XDG_DATA_HOME:-${HOME}/.local/share}/zinit/zinit.git"

if [ ! -d "$ZINIT_HOME" ]; then
    mkdir -p "$(dirname "$ZINIT_HOME")"
    git clone https://github.com/zdharma-continuum/zinit.git "$ZINIT_HOME"
fi

source "${ZINIT_HOME}/zinit.zsh"

########################################
# Plugins
########################################
zinit light zsh-users/zsh-syntax-highlighting
zinit light zsh-users/zsh-completions
zinit light zsh-users/zsh-autosuggestions
zinit light Aloxaf/fzf-tab

autoload -Uz compinit && compinit
zinit cdreplay -q

########################################
# Oh My Posh (ShellForge Theme)
########################################
if [[ "$TERM_PROGRAM" != "Apple_Terminal" ]]; then
    eval "$(oh-my-posh init zsh --config ~/.config/ohmyposh/themes/shellforge.omp.json)"
fi

########################################
# History Configuration
########################################
export HISTSIZE=100000000
export SAVEHIST=$HISTSIZE
export HISTFILE="$HOME/.zsh_history"
export HISTTIMEFORMAT="[%F %T] "

setopt appendhistory
setopt sharehistory
setopt hist_ignore_space
setopt hist_ignore_all_dups
setopt hist_save_no_dups
setopt hist_ignore_dups
setopt hist_find_no_dups

########################################
# Keybindings
########################################
bindkey "^[[A" history-search-backward
bindkey "^[[B" history-search-forward
bindkey '^R' history-substring-search-up
bindkey '^[w' kill-region
bindkey "^[b" backward-word
bindkey "^[f" forward-word

########################################
# Completion Styling
########################################
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=#666666'
fpath+=("$(brew --prefix)/share/zsh-completions")

zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'
zstyle ':completion:*' menu no
zstyle ':fzf-tab:complete:cd:*' fzf-preview 'ls --color $realpath'
zstyle ':fzf-tab:complete:__zoxide_z:*' fzf-preview 'ls --color $realpath'

########################################
# CLI Enhancements
########################################
eval "$(fzf --zsh)"
eval "$(zoxide init zsh)"

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh
if [ -f "$HOME/.local/bin/env" ]; then
    . "$HOME/.local/bin/env"
fi

########################################
# Aliases
########################################
alias vim="nvim"
alias ls="eza"
alias grep="grep --color=auto"
alias tree="tree -C"
alias pip="pip3"
alias python="python3"
alias get_networks=". /usr/local/bin/get_network_info.sh"

########################################
# Man Page Colors
########################################
export LESS_TERMCAP_mb=$'\e[1;34m'
export LESS_TERMCAP_md=$'\e[1;33m'
export LESS_TERMCAP_me=$'\e[0m'
export LESS_TERMCAP_se=$'\e[0m'
export LESS_TERMCAP_so=$'\e[1;44;33m'
export LESS_TERMCAP_ue=$'\e[0m'
export LESS_TERMCAP_us=$'\e[1;32m'

########################################
# End of ShellForge ZSH Config
########################################
