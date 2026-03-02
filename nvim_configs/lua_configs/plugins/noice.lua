return {{
    "folke/noice.nvim",
    opts = function(_, opts)
        -- disable bottom search so we use popupstyle
        opts.presets = opts.presets or {}
        opts.presets.bottom_search = false
        opts.presets.command_palette = true

        -- ensure views table exists
        opts.views = opts.views or {}

        -- center cmdline popup
        opts.views.cmdline_popup = {
            position = {
                row = "35%",
                col = "50%"
            },
            size = {
                width = 60,
                height = "auto"
            },
            border = {
                style = "rounded"
            }
        }

        -- center popup menu (search results / interactive search)
        opts.views.popupmenu = {
            relative = "editor",
            position = {
                row = "45%",
                col = "50%"
            },
            size = {
                width = 60,
                height = 10
            },
            border = {
                style = "rounded",
                padding = {0, 1}
            }
        }

        return opts
    end
}}
