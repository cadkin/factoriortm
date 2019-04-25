"""Convert a TAR file or directory of Factorio screenshots into Leaflet
map tiles.

Factorio Console Command to generate screenshots:
    /c game.player.surface.daytime = 0; for x=-1000,1000 do for y=-1000,1000 do if game.forces["player"].is_chunk_charted(1, {x, y}) then game.take_screenshot{show_entity_info=true, zoom=1, resolution={1024,1024}, position={x=32*x+16,y=32*y+16}, path="DIR/s_"..x.."_"..y..".jpg"}; end; end; end;

"""
import os
from glob import glob
import sys
import tarfile
import time
# local file
import log
from PIL import Image
from tqdm import tqdm
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from map_util import *
USAGE = '''
Usage: python3 factoriomap.py [source] [destination]
   source: directory, .tar file, or single .jpg
   destination: directory
'''
class EventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print("event with file {}, type {}".format(event.src_path, event.event_type))
            # Perform the modification to the changed file
            chunk_to_tiles(event.src_path)
            for zoom in range(9, 0, -1):
                x, y = chunk_coordinates(event.src_path)
                tile = '{}{}/{}/{}.jpg'.format(sys.argv[2], zoom+1, y, x)
                zoom_out(tile, zoom)

    def on_created(self, event):
        if not event.is_directory:
            print("event with file {}, type {}".format(event.src_path, event.event_type))
            # Perform the modification to the changed file
            chunk_to_tiles(event.src_path)
            for zoom in range(9, 0, -1):
                x, y = chunk_coordinates(event.src_path)
                tile = '{}{}/{}/{}.jpg'.format(sys.argv[2], zoom+1, y, x)
                zoom_out(tile, zoom)


def main():
    """Main executable function."""
    # Verify arguments; print usage on failure.
    if len(sys.argv) < 3:
        print(USAGE)

        sys.exit()
    if not os.path.isdir(sys.argv[2]):
        os.makedirs(sys.argv[2])

    if not os.path.exists(sys.argv[1]):
        os.makedirs(sys.argv[1])


    if os.path.isfile(sys.argv[1]):
        # If tar file
        if sys.argv[1].split('.')[-1] == 'tar':
            archive = tarfile.open(sys.argv[1])
            chunks = sorted(archive.getnames(), key=chunk_coordinates)
            for chunk in tqdm(chunks):
                chunk_to_tiles(archive.extractfile(chunk), chunk)

        else:        # singular file
            chunk_to_tiles(sys.argv[1])
            for zoom in range(9, 0, -1):
                x, y = chunk_coordinates(sys.argv[1])
                tile = '{}{}/{}/{}.jpg'.format(sys.argv[2], zoom+1, x, y)
                zoom_out(tile, zoom)

    else:
        if not os.path.exists(sys.argv[1]):
            os.makedirs(sys.argv[1])

        chunks = sorted(glob(sys.argv[1]+'c_*.jpg'), key=chunk_coordinates)
        for chunk in tqdm(chunks):
            chunk_to_tiles(chunk)

    for zoom in range(9, 0, -1):
        tiles = sorted(
            glob('{}{}/*/*.jpg'.format(sys.argv[2], zoom+1)),
            key=tile_coordinates)
        for tile in tqdm(tiles):
            zoom_out(tile, zoom)

    observer = Observer()
    event_handler = EventHandler()

    observer.schedule(event_handler, sys.argv[1], recursive=True)
    observer.start()

    while True:
        # time.sleep(0.0001)
        pass

if __name__ == '__main__':
    main()
