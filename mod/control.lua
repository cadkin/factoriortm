require("lib.screenshot")

-- On world creation, save the currently generated chunks.
script.on_init(
    function()
        --[[
        for chunk in game.surfaces["nauvis"].get_chunks() do
            if game.surfaces["nauvis"].is_chunk_generated(chunk) then
                game.write_file("chunks.log", "LOADED " .. chunk.x .. " " .. chunk.y .. "\n", true)
                sshot_chunk(chunk)
            end
        end

        --game.set_wait_for_screenshots_to_finish()
        --]]
    end
)

-- When a chunk is charted, save a screenshot of it.
script.on_event({defines.events.on_chunk_charted},
    function(e)
        game.write_file("chunks.log", "CHARTED " .. e.position.x .. " " .. e.position.y .. "\n", true)
        sshot_chunk(e.position)
    end
)

-- Handle the player position data.
script.on_nth_tick(60,
    function (e)
        -- For each player, update their position and write their positions to a file.
        for index, player in pairs(game.connected_players) do
            --player.print(player.position.x.." "..player.position.y);
            game.write_file("test.log", "PLAYER " .. player.position.x .. " " .. player.position.y .. "\n", true);
        end
    end
)
