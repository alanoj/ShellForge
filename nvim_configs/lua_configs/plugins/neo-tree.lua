-- ShellForge: Neo-tree file explorer configuration
-- Combines Kickstart visibility and LazyVim integration
return {{
    "nvim-neo-tree/neo-tree.nvim",
    opts = function(_, opts)
        -- Window position & size
        opts.window = opts.window or {}
        opts.window.position = "left"
        opts.window.width = 40

        -- Make dotfiles & hidden visible like Kickstart
        opts.filesystem = opts.filesystem or {}
        opts.filesystem.filtered_items = opts.filesystem.filtered_items or {}
        opts.filesystem.filtered_items.hide_dotfiles = false
        opts.filesystem.filtered_items.hide_gitignored = false
        opts.filesystem.filtered_items.hide_hidden = false

        -- Additional names to hide if desired
        opts.filesystem.filtered_items.hide_by_name = vim.tbl_extend("force",
            opts.filesystem.filtered_items.hide_by_name or {}, {".DS_Store", "thumbs.db", "node_modules", "__pycache__",
                                                                ".virtual_documents", ".python-version", ".venv"})

        -- Components (icons, git symbols)
        opts.default_component_configs = opts.default_component_configs or {}
        opts.default_component_configs.git_status = opts.default_component_configs.git_status or {}
        opts.default_component_configs.git_status.symbols = vim.tbl_extend("force", opts.default_component_configs
            .git_status.symbols or {}, {
            added = "✚",
            modified = "",
            deleted = "✖",
            renamed = "➜",
            untracked = "",
            ignored = "",
            unstaged = "󰄱",
            staged = "",
            conflict = ""
        })

        opts.default_component_configs.indent = opts.default_component_configs.indent or {}
        opts.default_component_configs.indent.padding = 1

        opts.default_component_configs.icon = opts.default_component_configs.icon or {}
        opts.default_component_configs.icon.folder_closed = ""
        opts.default_component_configs.icon.folder_open = ""
        opts.default_component_configs.icon.folder_empty = ""
        opts.default_component_configs.icon.default = ""
        opts.default_component_configs.icon.symlink = ""
        opts.default_component_configs.icon.marked = "★"
    end,
    -- ShellForge: Neo-tree auto-open and enhancements
    vim.api.nvim_create_autocmd("VimEnter", {
        callback = function()
            -- Only open if nvim is started without a specific file
            if vim.fn.argc() == 0 then
                require("neo-tree.command").execute({
                    toggle = true,
                    dir = vim.loop.cwd()
                })
            end
        end
    }),

    vim.api.nvim_create_autocmd("BufEnter", {
        callback = function()
            require("neo-tree.command").execute({
                toggle = false,
                reveal = true
            })
        end
    })
}}
