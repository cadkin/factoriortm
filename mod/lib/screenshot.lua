local px_per_chunk = 32
local tiles_per_chunk = 32
local chunk_res = 1024

-- Produces a screenshot of a specified chunk. Takes a ChunkPosition class.
function sshot_chunk(chunk)
    local chunk_x = chunk.x * tiles_per_chunk
    local chunk_y = chunk.y * tiles_per_chunk

    -- Add 16 to get center of chunk for screenshot.
    game.take_screenshot({position = {chunk_x + 16, chunk_y + 16}, resolution = {chunk_res, chunk_res}, path = "mapdata/" .. g_seed .. "/c" .. chunk.x .. "_" ..chunk.y .. ".jpg", show_gui = false })
end

function sshot_all()
    for chunk in game.surfaces["nauvis"].get_chunks() do
        if game.surfaces["nauvis"].is_chunk_generated(chunk) then
            game.write_file("chunks.log", "LOADED " .. chunk.x .. " " .. chunk.y .. "\n", true)
            sshot_chunk(chunk)
        end
    end

    game.set_wait_for_screenshots_to_finish()
end
