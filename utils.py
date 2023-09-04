import json
import random
from pathlib import Path
import os

DATA_PATH = Path("./data")
DISPLAY_PATH = Path("./display")
RUNTIME_DATA_PATH = DATA_PATH / "runtime_data.json"
WORLD_DATA_PATH = DATA_PATH / "world_data.json"
DISPLAY_DATA_PATH = DISPLAY_PATH / "display_data.js"

vnw  = {"name": "Aurorise", "pos": (0, 0), "name_range": (0, 66)},
nw   = {"name": "Mystique", "pos": (0, 1), "name_range": (66, 132)},
n    = {"name": "Summitia", "pos": (0, 2), "name_range": (132, 198)},
ne   = {"name": "Lumisong", "pos": (0, 3), "name_range": (198, 264)},
vne  = {"name": "Celestia", "pos": (0, 4), "name_range": (264, 330)},
w    = {"name": "Veridian", "pos": (1, 0), "name_range": (330, 396)},
mw   = {"name": "Emberias", "pos": (1, 1), "name_range": (396, 462)},
c    = {"name": "Jubilant", "pos": (1, 2), "name_range": (462, 528)},
me   = {"name": "Solstice", "pos": (1, 3), "name_range": (528, 594)},
e    = {"name": "Echowind", "pos": (1, 4), "name_range": (594, 660)},
vsw  = {"name": "Vividora", "pos": (2, 0), "name_range": (660, 726)},
sw   = {"name": "Serenade", "pos": (2, 1), "name_range": (726, 792)},
s    = {"name": "Harmonia", "pos": (2, 2), "name_range": (792, 858)},
se   = {"name": "Eupheres", "pos": (2, 3), "name_range": (858, 924)},
vse  = {"name": "Radiance", "pos": (2, 4), "name_range": (900, 999)},


def coord_to_region(coord: list[int, int]):
    return [
        [vnw, nw, n, ne, vne],
        [w, mw, c, me, e],
        [vsw, sw, s, se, vse]
    ][coord[0]][coord[1]][0]


gender_names = {}
def load_names(gender):
    global gender_names
    with open(f"./assets/{gender}_names.txt", "r") as f:
        gender_names[gender] = f.read().split("\n")


def get_person_name(gender: int, father: str = None, mother: str = None) -> str:
    
    gender = ["female", "male"][gender]
    
    if gender not in gender_names:
        load_names(gender)
    
    names = gender_names[gender]
    
    if father is None and father is None:
        return random.choice(names)
    
    father_region = father["region"], father["location"]
    mother_region = mother["region"], mother["location"]
    
    if father_region[0] == mother_region[0]:
        name_range = coord_to_region(father_region[1])["name_range"]
        name_list  = names[name_range[0]:name_range[1]]
        return random.choice(name_list)
    
    father_name_range = coord_to_region(father_region[1])["name_range"]
    mother_name_range = coord_to_region(mother_region[1])["name_range"]
        
    father_name_list = names[father_name_range[0]:father_name_range[1]]
    mother_name_list = names[mother_name_range[0]:mother_name_range[1]]
    
    combined_name_list = father_name_list + mother_name_list
    return random.choice(combined_name_list)


def load_json(file_path: str = str(WORLD_DATA_PATH)) -> dict:
    file_path = Path(file_path)
    with file_path.open("r") as f:
        return json.load(f)

def save_json(file_path: str = str(WORLD_DATA_PATH), new_data: dict = {}, indent=4) -> int:
    file_path = Path(file_path)
    with file_path.open("w") as f:
        if indent == 0:
            json.dump(new_data, f, indent=indent, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
        else:
            json.dump(new_data, f, indent=indent, ensure_ascii=False)
    return 0


def clear_terminal_screen():
    os.system('cls' if os.name=='nt' else 'clear')
