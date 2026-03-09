local M = {}

M.apply = function(name)
    if name == "kanagawa" then
        require("kanagawa").setup({
            theme = "dragon"
        })
        vim.cmd("colorscheme kanagawa")
    elseif name == "rose-pine" then
        require("rose-pine").setup({
            variant = "main"
        })
        vim.cmd("colorscheme rose-pine")
    elseif name == "catppuccin" then
        require("catppuccin").setup({
            flavour = "mocha"
        })
        vim.cmd("colorscheme catppuccin")
    else
        print("Theme not found:", name)
    end
end

return M
