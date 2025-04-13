import subprocess
import re
from find_map import find_map
from parser import Parser

def get_map_name() -> str:
    while True:
        active_win_name = subprocess.run(["wmctrl", "-l"], capture_output=True, text=True).stdout
        if "osu!" in active_win_name:
            # split output by "osu!" and take everything after it
            active_map_name = active_win_name.split("osu!")[1].strip()
            # remove leading "- "
            active_map_name = active_map_name.lstrip("- ")
            if len(active_map_name) > 0:
                return active_map_name

map_full = get_map_name()

match = re.match(r"(.+?)\s*-\s*(.+?)\s*\[(.+)\]$", map_full)
if match:
    artist = match.group(1).strip()
    song_name = match.group(2).strip()
    difficulty = match.group(3).strip()
else:
    artist = ""
    song_name = map_full
    difficulty = ""

print("Artist:", artist)
print("Song Name:", song_name)
print("Difficulty:", difficulty)
print(map_path := find_map(artist, song_name, difficulty)[0])

print()

#
# TEST
#

with open(map_path, "r", encoding="utf-8") as f:
    mapdata = f.read()

parser = Parser()
parser.mapdata = mapdata
parser.HR = False
parser.EZ = False
parser.DT = False

circles = parser.load_circle_info()
print(circles)