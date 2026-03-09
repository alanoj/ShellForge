return {{
    "folke/flash.nvim",
    event = "VeryLazy",
    opts = {
        jump = {
            autojump = true
        },
        modes = {
            char = {
                jump_labels = true,
                multi_line = false
            }
        }
    }
}}
