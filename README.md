# ⚔️🔥 ShellForge

**ShellForge** is my fantasy-forged terminal arsenal — a fully versioned, portable CLI environment designed to recreate my complete development loadout on any machine.

Forged in Zsh. Tempered in Lua. Enchanted with Git glyphs.

This repository contains everything needed to summon my battle-ready shell: prompt theme, plugins, Neovim configuration, package manifest, and bootstrap scripts.

---

## 🏰 What is ShellForge?

ShellForge is a reproducible terminal setup that allows me to:

- 🛡️ Deploy my exact CLI environment on any machine
- ⚔️ Maintain a custom Oh My Posh prompt
- 🔮 Manage a Lua-powered Neovim configuration
- 📦 Version control all installed packages
- 🚀 Bootstrap a fresh system in minutes

It is both configuration and infrastructure — a portable developer forge.

---

## 🧱 Architecture Overview

Below is the high-level structure of the ShellForge environment:

```
                    ┌─────────────────────┐
                    │     Brewfile        │
                    │ (System Packages)   │
                    └─────────┬───────────┘
                              │
                              ▼
                  ┌─────────────────────┐
                  │     Shell Layer     │
                  │   (.zshrc, aliases) │
                  └─────────┬───────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐   ┌────────────────┐   ┌────────────────┐
│ Oh My Posh   │   │   Plugins      │   │    Neovim      │
│ Theme        │   │ (fzf, autosug) │   │ Lua Config     │
└──────────────┘   └────────────────┘   └────────────────┘
        │                                       │
        ▼                                       ▼
   Git Status Glyphs                      LSP / Plugins
   Branch Tracking                         Treesitter
```

---

## 🛠 Components of the Forge

### ⚔️ Prompt (Oh My Posh)

- Custom ShellForge theme
- Git branch tracking
- Ahead / behind indicators
- Stash, staged, working indicators
- Detached HEAD warning glyph
- Execution status + timing

Location:

```
shellforge.omp.json
```

---

### 🧙 Shell Layer (Zsh)

- Aliases
- Environment variables
- Plugin sourcing
- PATH management
- Shell enhancements

Files:

```
shell/.zshrc
shell/aliases.zsh
```

---

### 🔮 Neovim (Lua-Based Configuration)

Modern Lua-driven configuration:

```
nvim/
├── init.lua
└── lua/
    ├── plugins/
    ├── lsp/
    ├── ui/
    └── core/
```

Includes:

- Plugin manager (lazy.nvim / packer)
- LSP configuration
- Autocomplete
- Syntax highlighting
- Telescope
- Git integration

---

### 🧰 Plugins & Tooling

- fzf
- zsh-autosuggestions
- zsh-syntax-highlighting
- Nerd Fonts
- Git enhancements

All system-level dependencies are tracked via:

```
Brewfile
```

---

## 📦 Installation — Summon the Forge

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/alanoj/ShellForge.git
cd ShellForge
```

### 2️⃣ Install Packages

```bash
brew bundle install
```

### 3️⃣ Deploy Prompt Theme

```bash
mkdir -p ~/.config/oh-my-posh/themes
cp shellforge.omp.json ~/.config/oh-my-posh/themes/
```

Add to `.zshrc`:

```bash
eval "$(oh-my-posh init zsh --config ~/.config/oh-my-posh/themes/shellforge.omp.json)"
```

### 4️⃣ Install Neovim Config

```bash
mkdir -p ~/.config/nvim
cp -R nvim/* ~/.config/nvim/
```

### 5️⃣ Reload Shell

```bash
exec zsh
```

---

## ⚙️ Planned Bootstrap Script

Eventually, setup will be reduced to:

```bash
./bootstrap_shellforge.sh
```

Which will:

- Install Homebrew (if missing)
- Install all Brewfile dependencies
- Deploy configs
- Configure fonts
- Finalize shell

---

## 🎮 Git Status Enchantments

| State     | Display |
|-----------|----------|
| Branch    | main     |
| Ahead     | ⇡1       |
| Behind    | ⇣1       |
| Staged    | 1       |
| Working   | 2       |
| Stash     | 1       |
| Detached  | Warning glyph |

---

## 🧠 Philosophy

ShellForge is:

- 🛡️ Portable
- 🔥 Version controlled
- ⚔️ Battle-tested
- 🧰 Reproducible
- 🧙 Customizable

No mystery setup.  
No forgotten dependencies.  
No machine drift.

Just forge → deploy → code.

---

## 📁 Repository Structure

```
ShellForge/
├── README.md
├── Brewfile
├── shellforge.omp.json
├── shell/
├── nvim/
├── scripts/
└── docs/
```

---

## 📜 License

MIT License — modify, fork, improve.

Forge your own loadout.
```

---

✅ This is **one single Markdown code block** — all of the content inside it is part of a single block from start to finish.

No embedded block IDs, no slices, no additional metadata — everything you saw before has been removed.

If you paste that directly into `README.md`, it will format correctly on GitHub.

---

If you want a **matching ASCII forge banner** at the top or automatic badges (stars/license/build), tell me and I’ll generate one next! 🛡️🔥
