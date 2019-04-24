local px_per_chunk = 32
local tiles_per_chunk = 32
local chunk_res = 1024

-- Produces a screenshot of a specified chunk. Takes a ChunkPosition class.
function sshot_chunk(chunk)
    local chunk_x = chunk.x * tiles_per_chunk
    local chunk_y = chunk.y * tiles_per_chunk

    -- Add 16 to get center of chunk for screenshot.
    game.take_screenshot({position = {chunk_x + 16, chunk_y + 16}, resolution = {chunk_res, chunk_res}, path = "mapdata/" .. global.g_seed .. "/raw/c_" .. chunk.x .. "_" ..chunk.y .. ".jpg", show_gui = false })
end

-- Function that screenshots all generated chunks.
function sshot_all()
    local time = game.surfaces["nauvis"].daytime
    game.surfaces["nauvis"].daytime = 0

    -- 'nauvis' is the default surface in the game (the one the player starts on)
    for chunk in game.surfaces["nauvis"].get_chunks() do
        if game.surfaces["nauvis"].is_chunk_generated(chunk) then
            game.write_file("mapdata/" .. global.g_seed .. "/socket/chunks.socket", "IMPORT " .. chunk.x .. " " .. chunk.y .. "\n")
            sshot_chunk(chunk)
        end
    end

    game.surfaces["nauvis"].daytime = time
end
