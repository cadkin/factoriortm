tiles_per_chunk = 32
px_per_tile = 32

-- Produces a screenshot of a specified chunk. Takes a ChunkPosition class.
function sshot_chunk(chunk)
    local chunk_x = chunk.x * tiles_per_chunk
    local chunk_y = chunk.y * tiles_per_chunk

    game.take_screenshot({position = {chunk_x, chunk_y}, resolution = {tiles_per_chunk * px_per_tile, tiles_per_chunk * px_per_tile}, path = "c" .. chunk.x .. "_" ..chunk.y .. ".png", show_gui = false })
end

