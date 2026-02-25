return {
  {
    "hrsh7th/nvim-cmp",
    opts = function(_, opts)
      -- Show kind icons + short source labels
      local kind_icons = {
        Text = "󰉿",
        Method = "m",
        Function = "󰊕",
        Constructor = "",
        Field = "",
        Variable = "󰆧",
        Class = "󰌗",
        Interface = "",
        Module = "",
        Property = "",
        Unit = "",
        Value = "󰎠",
        Enum = "",
        Keyword = "󰌋",
        Snippet = "",
        Color = "󰏘",
        File = "󰈙",
        Reference = "",
        Folder = "󰉋",
        EnumMember = "",
        Constant = "󰇽",
        Struct = "",
        Event = "",
        Operator = "󰆕",
        TypeParameter = "󰊄",
      }

      opts.formatting = opts.formatting or {}
      opts.formatting.fields = { "kind", "abbr", "menu" }
      opts.formatting.format = function(entry, item)
        item.kind = string.format("%s", kind_icons[item.kind] or item.kind)
        item.menu = ({
          nvim_lsp = "[LSP]",
          luasnip = "[Snip]",
          buffer = "[Buf]",
          path = "[Path]",
        })[entry.source.name] or ("[" .. entry.source.name .. "]")
        return item
      end
    end,
  },
}