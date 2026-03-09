return {
  {
    "nvim-lualine/lualine.nvim",
    opts = function(_, opts)

        -- ensure base tables exist
      opts.sections = opts.sections or {}
      opts.sections.lualine_a = opts.sections.lualine_a or {}
      opts.sections.lualine_b = opts.sections.lualine_b or {}
      opts.sections.lualine_c = opts.sections.lualine_c or {}
      opts.sections.lualine_x = opts.sections.lualine_x or {}
      opts.sections.lualine_y = opts.sections.lualine_y or {}
      opts.sections.lualine_z = opts.sections.lualine_z or {}

      opts.inactive_sections = opts.inactive_sections or {}
      opts.inactive_sections.lualine_a = opts.inactive_sections.lualine_a or {}
      opts.inactive_sections.lualine_b = opts.inactive_sections.lualine_b or {}
      opts.inactive_sections.lualine_c = opts.inactive_sections.lualine_c or {}
      opts.inactive_sections.lualine_x = opts.inactive_sections.lualine_x or {}
      opts.inactive_sections.lualine_y = opts.inactive_sections.lualine_y or {}
      opts.inactive_sections.lualine_z = opts.inactive_sections.lualine_z or {}

      -- Custom mode component
      local mode = {
        "mode",
        fmt = function(str)
          return " " .. str
        end,
      }

      -- Custom filename component
      local filename = {
        "filename",
        file_status = true,
        path = 0,
      }

      local hide_in_width = function()
        return vim.fn.winwidth(0) > 100
      end

      local diagnostics = {
        "diagnostics",
        sources = { "nvim_diagnostic" },
        sections = { "error", "warn" },
        symbols = { error = " ", warn = " ", info = " ", hint = " " },
        colored = false,
        update_in_insert = false,
        always_visible = false,
        cond = hide_in_width,
      }

      local diff = {
        "diff",
        colored = false,
        symbols = { added = " ", modified = " ", removed = " " },
        cond = hide_in_width,
      }

      table.insert(opts.sections.lualine_x, {
        require("noice").api.statusline.mode.get,
        cond = require("noice").api.statusline.mode.has,
        color = { fg = "#ff9e64" },
      })

      -- Override existing sections
      opts.options.theme = "nord"
      opts.options.section_separators = { left = "", right = "" }
      opts.options.component_separators = { left = "", right = "" }
      opts.options.disabled_filetypes = { "alpha", "neo-tree" }

      opts.sections.lualine_a = { mode }
      opts.sections.lualine_b = { "branch" }
      opts.sections.lualine_c = { filename }
      opts.sections.lualine_x = {
        diagnostics,
        diff,
        { "encoding", cond = hide_in_width },
        { "filetype", cond = hide_in_width },
      }
      opts.sections.lualine_y = { "location" }
      opts.sections.lualine_z = { "progress" }

      opts.inactive_sections.lualine_c = { { "filename", path = 1 } }
      opts.inactive_sections.lualine_x = { { "location", padding = 0 } }

      return opts
    end,
  },
}
