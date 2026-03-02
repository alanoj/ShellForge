return {
    "rebelot/kanagawa.nvim",
    lazy = false, -- Load during startup so the theme is available immediately
    priority = 1000, -- Load this before other plugins
    opts = {
        -- Add any specific Kanagawa options here (e.g., dimming, transparency)
        compile = true,
        undercurl = true
    },
    config = function(_, opts)
        require("kanagawa").setup(opts)
        vim.cmd("colorscheme kanagawa-wave") -- Actually activates the theme
    end
}
