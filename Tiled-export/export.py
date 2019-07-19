#!/usr/bin/env python3

"""
Script exports map, tilesets
Debuggs map in Tiled program by swapping tilesets

Directory layout of Tiled and Game asset folder
must exactly match to not break referance links
"""

import os
from shutil import copy
from sys import argv

# map_dir: where the game map asset resides
map_dir = "/home/rubsz/Documents/programming/game_dev/Tides_of_war/asset/img/map"
# character_dir: where the game character sprite assets reside
character_dir = "/home/rubsz/Tides_of_war/asset/img/character"

tileset_dir = "tilesets"
dtileset_dir = "debug_tilesets"

# debug_name: placeholder name in res dir for program to know if it's currently using debugging tilesets or not
debug_name = "DEBUG-"

img_ext = ".png"
map_ext = ".tmx"
tileset_ext = ".tsx"

if len(argv) > 1:
    arg = argv[1]
    if os.path.isfile(arg) and not arg.endswith(map_ext) or os.path.isdir(arg) and arg.endswith(tileset_dir):
        print("\n--> EXECUTE IN MAP SCENE\n--> ABORTING OPERATION")
    elif os.path.isdir(arg) and len(argv) == 3:
        # This is for swapping tilesets
        arg = os.path.join(arg, tileset_dir)
        if argv[2] == "DEBUG":
            dtileset_dir = os.path.join(arg, dtileset_dir)
            debug = True
            for thing in os.listdir(arg):
                if thing.startswith(debug_name):
                    debug = False
                    break
            if not debug:
                for tileset in os.listdir(arg):
                    if tileset.endswith(img_ext) and tileset.startswith(debug_name):
                        os.rename(os.path.join(arg, tileset), os.path.join(arg, tileset[len(debug_name):]))
            else:
                for tileset in os.listdir(arg):
                    if tileset.endswith(img_ext):
                        os.rename(os.path.join(arg, tileset), os.path.join(arg, debug_name + tileset))
                for dtileset in os.listdir(dtileset_dir):
                    if os.path.isfile(os.path.join(dtileset_dir, dtileset)):
                        copy(os.path.join(dtileset_dir, dtileset), os.path.join(arg, dtileset))
            print("\n--> DEBUG MAP: %s\n--> PRESS (CTRL-T) TO REFRESH IF HASN'T" % debug)

        elif os.path.isdir(argv[2]):
            # This is for exporting tilesets
            map_dir = os.path.join(map_dir, tileset_dir)
            if not os.path.isdir(map_dir):
                os.mkdir(map_dir)
            for tileset in os.listdir(arg):
                if os.path.isfile(os.path.join(arg, tileset)):
                    copy(os.path.join(arg, tileset), map_dir)
            arg = argv[2]
            for race in os.listdir(arg):
                if os.path.isdir(os.path.join(arg, race)):
                    for thing in os.listdir(os.path.join(arg, race)):
                        if thing.endswith(tileset_ext):
                            copy(os.path.join(arg, race, thing), os.path.join(character_dir, race, thing))
            print("\n--> TILESETS EXPORTED TO: %s" % map_dir)

    else:
        # This is for exporting map
        copy(arg, map_dir)
        print("\n--> MAP EXPORTED TO: %s" % map_dir)
else:
    print("\n--> NEED ARGS FROM TILED TO RUN")
