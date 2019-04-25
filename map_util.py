import os
from os import sys
from glob import glob
import tarfile

from PIL import Image
from tqdm import tqdm

print(os.sys.argv[2])
def zoom_out(filename, zoom):
    """Shrink and combine tiles to zoom view out."""
    source_x, source_y = tile_coordinates(filename)
    tile_x = source_x // 2
    tile_y = source_y // 2
    origin_x = tile_x * 2
    origin_y = tile_y * 2

    # if not os.path.isfile(
    #         '{}{}/{}/{}.jpg'.format(sys.argv[2], zoom, tile_y, tile_x)):
    os.makedirs('{}{}/{}'.format(sys.argv[2], zoom, tile_y), exist_ok=True)

    tile_image = Image.new('RGB', (512, 512))
    for x_adj in range(2):
        for y_adj in range(2):
            try:
                paste_image = Image.open('{}{}/{}/{}.jpg'.format(
                    sys.argv[2], zoom+1, origin_y+y_adj, origin_x+x_adj))
            except FileNotFoundError:
                paste_image = Image.new('RGB', (256, 256))

            tile_image.paste(
                paste_image,
                (x_adj*256, y_adj*256))

    tile_image.resize((256, 256)).save('{}{}/{}/{}.jpg'.format(
        sys.argv[2], zoom, tile_y, tile_x))

    print("Saved tile image to {}{}/{}/{}.jpg".format(
        sys.argv[2], zoom, tile_y, tile_x))

def chunk_coordinates(filename):
    """Extract chunk coordinates         for x_adj in range(4):
            for y_adj in range(4):
                os.makedirs(
                    '{}{}/{}'.format(
                        sys.argv[2], 10, tile_y+y_adj),
                    exist_ok=True)

                chunk_image.crop(
                    (
                        x_adj*256,
                        y_adj*256,
                        (x_adj+1)*256,
                        (y_adj+1)*256)
                    ).save('{}{}/{}/{}.jpg'.format(
                        sys.argv[2], 10, tile_y+y_adj, tile_x+x_adj))
from filename."""
    _, chunk_x, chunk_y = os.path.splitext(filename)[0].split('_')
    return (int(chunk_x), int(chunk_y))

def tile_coordinates(path):
    """Compute tile coordinates."""
    explosion = os.path.splitext(path)[0].split('/')
    return (int(explosion[-1]), int(explosion[-2]))

def chunk_to_tiles(chunk, chunkname=None):
    """Convert the chunk screenshot to Leaflet tiles at maximum zoom."""
    chunk_image = Image.open(chunk)
    if chunkname is None:
        chunk_x, chunk_y = chunk_coordinates(chunk)
    else:
        chunk_x, chunk_y = chunk_coordinates(chunkname)
    tile_x = chunk_x*4
    tile_y = chunk_y*4

    # if not os.path.isfile(
    #         '{}{}/{}/{}.jpg'.format(sys.argv[2], 10, tile_y, tile_x)):
    for x_adj in range(4):
        for y_adj in range(4):
            os.makedirs(
                '{}{}/{}'.format(
                    sys.argv[2], 10, tile_y+y_adj),
                exist_ok=True)

            chunk_image.crop(
                (
                    x_adj*256,
                    y_adj*256,
                    (x_adj+1)*256,
                    (y_adj+1)*256)
                ).save('{}{}/{}/{}.jpg'.format(
                    sys.argv[2], 10, tile_y+y_adj, tile_x+x_adj))
            
            print("Saved tile image to {}{}/{}/{}.jpg".format(sys.argv[2], 10, tile_y, tile_x))

