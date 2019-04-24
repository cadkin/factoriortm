require("lib.screenshot")

-- On init, read the map seed and use it to store our map data.
script.on_init(
    function()
        global.g_seed = game["default_map_gen_settings"]["seed"]
        game.write_file("mapdata/" .. global.g_seed .. "/socket/chunks.socket", "WSEED " .. global.g_seed .. "\n", true)

        -- If the number of ticks in the game is greater than 600 (10 seconds), then this must be a pre-existing save. Screenshot everything.
        if game.tick > 600 then
            sshot_all()
        end
    end
)

-- When a chunk is charted, save a screenshot of it.
script.on_event({defines.events.on_chunk_charted},
    function(e)
        game.write_file("mapdata/" .. global.g_seed .. "/socket/chunks.socket", "CHUNK " .. e.position.x .. " " .. e.position.y .. "\n", true)

        -- Save the time of day so we can restore it later.
        local time = game.surfaces["nauvis"].daytime
        game.surfaces["nauvis"].daytime = 0

        sshot_chunk(e.position)

        game.surfaces["nauvis"].daytime = time
    end
)

-- Handle the player position data.
script.on_nth_tick(60,
    function (e)
        -- For each player, update their position and write their positions to a file.
        for index, player in pairs(game.connected_players) do
            if player.name ~= "" then
                --player.print(player.position.x.." "..player.position.y);
                game.write_file("mapdata/" .. global.g_seed .. "/socket/player.socket", "PLAYER " .. player.name .. " "  .. player.position.x .. " " .. player.position.y .. "\n");
            end
        end
    end
)
