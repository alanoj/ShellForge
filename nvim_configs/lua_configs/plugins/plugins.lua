-- ShellForge: Plugin import order (LazyVim → Extras → Custom)

return {
  
  { import = "lazyvim.plugins.extras.lang.clangd"   }, -- C/C++
  { import = "lazyvim.plugins.extras.lang.json"     }, -- JSON + schemas
  { import = "lazyvim.plugins.extras.lang.markdown" }, -- Markdown preview/lint
  { import = "lazyvim.plugins.extras.lang.go"       }, -- Go support
  { import = "lazyvim.plugins.extras.lang.python"   }, -- Python support
  { import = "lazyvim.plugins.extras.lang.rust"     }, -- Rust support
}