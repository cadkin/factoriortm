local hfile = require "xavante.filehandler"
--local hcgi = require "xavante.cgiluahandler"
local hredir = require "xavante.redirecthandler"

local xavante = require "xavante"

-- Define here where Xavante HTTP documents scripts are located
local webDir = "./html/"

local simplerules = {
    { -- URI remapping example
      match = "^[^%./]*/$",
      with = hredir,
      params = {"index.html"}
    },
    --[[

    { -- cgiluahandler example
      match = {"%.lp$", "%.lp/.*$", "%.lua$", "%.lua/.*$" },
      with = hcgi.makeHandler (webDir)
    },
    --]]

    { -- filehandler example
      match = ".",
      with = hfile,
      params = {baseDir = webDir}
    },
}

xavante.HTTP{
    server = {host = "*", port = 8080},

    defaultHost = {
    	rules = simplerules
    },
}

xavante.start();
