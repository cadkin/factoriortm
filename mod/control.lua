require("lib.screenshot")

g_seed = 0

-- On init, read the map seed and use it to store our map data.
script.on_init(
    function()
        g_seed = game["default_map_gen_settings"]["seed"]
    end
)

-- When a chunk is charted, save a screenshot of it.
script.on_event({defines.events.on_chunk_charted},
    function(e)
        game.write_file("mapdata/" .. g_seed .. "/socket/chunks.socket", "CHARTED " .. e.position.x .. " " .. e.position.y .. "\n", true)
        sshot_chunk(e.position)
    end
)

-- Handle the player position data.
script.on_nth_tick(60,
    function (e)
        -- For each player, update their position and write their positions to a file.
        for index, player in pairs(game.connected_players) do
            --player.print(player.position.x.." "..player.position.y);
            game.write_file("mapdata/" .. g_seed .. "/socket/player.socket", "PLAYER " .. player.name .. " "  .. player.position.x .. " " .. player.position.y .. "\n", true);
        end
    end
)
