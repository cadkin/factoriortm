Factorio Real-Time Map
===============================

Description: A modification for Factorio that allows display of map elements in a browser. Partially based on [Factorio to Leaflet Maps].

[Factorio to Leaflet Maps]: https://github.com/SenorPez/factorio-leaflet-maps

Installation and usage info
-------------------------------

Setup requires a number of steps.

##### Mod Installation

Installation of the mod is fairly simple:
1. Locate your installation of Factorio. If the game was installed by Steam, this will be in `$HOME/.factorio/` on Linux. Otherwise, this will be the location where you extracted the game.
2. Create the directory `mods/factoriortm_0.1.0/` inside the Factorio root.
3. Copy the contents of `mod` from the repository to `mods/factoriortm_0.1.0/` inside the Factorio root.

##### Leaflet Setup

Leaflet is used to render the map in game. However, it must know where to source the data from:
1. Inside the repository, navigate to `web/js`.
2. In `main.js` modify the two strings at the top of the file. `mapSeed` must be the seed used by the game to generate the map that will be displayed. `gamePath` is the location of your Factorio installation.

##### Python Setup and Execution

The python watcher script requires the follow modules:
- dev-python/pillow
- dev-python/tqdm
- dev-python/watchdog

The watcher script can now be started using the follow command:
```
$ python3 factoriomap.py [path_to_raw_data] [path_to_output]
```
- `[path_to_raw_data]` specifies where the script will pickup raw images for conversion to Leaflet tiles. The mod outputs raw tiles to `script-output/mapdata/<map_seed>/raw/`. Therefore, this parameter should look something like `/home/user/factorio/script-output/mapdata/1234567890/raw`.
- `[path_to_output]` specifies where the script will write the output. By default, the webpage looks for files in `script-output/mapdata/<map_seed>/leaflet` Therefore, this parameter should look something like `/home/user/factorio/script-output/mapdata/1234567890/leaflet`.

##### Running

With the mod installed and the script running, the map can now be viewed:
1. Open up Factorio and either load up the world corresponding to your seed or create a new world using your seed.
2. Allow the game to generate the screenshots and the script to process them. On a new world, this does not take overly long but on older worlds this can take a while.
3. In your web browser, open up `file://` and navigate to the repository. Open up `web/index.html` and the map should appear.

-------------------------------
##### Known Issues

- Script does not render tiles consistently at any zoom greater than the closest.
- Webpage does not refresh quickly due to caching by the browser. Currently, this can be worked around by refreshing the page.
- Generated images follow the time of day in game. As such, this can create a jarring difference between tiles taken at night and tiles taken during the day.
- Setup is NOT elegant at all.
