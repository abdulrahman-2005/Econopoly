import json
import random
from collections import defaultdict
from pathlib import Path
import os
import numpy as np


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyEncoder, self).default(obj)

DATA_PATH = Path("./data")
DISPLAY_PATH = Path("./display")
RUNTIME_DATA_PATH = DATA_PATH / "runtime_data.json"
WORLD_DATA_PATH = DATA_PATH / "world_data.json"
DISPLAY_DATA_PATH = DISPLAY_PATH / "display_data.js"

UPDATE_DISPLAY_DELAY = 10

vnw = "Codarixa_land"
nw  = "Misty_dry"
n   = "Peakland"
ne  = "Misty_wet"
vne = "Chmugs_island"
w   = "West_ram"
mw  = "Crustia"
c   = "Capitolia"
me  = "Midway_dash"
e   = "East_ram"
vsw = "luxestan"
sw  = "comma_clan"
s   = "loid_island"
se  = "luxexis_island"
vse = "southern_luxestan"

coord_to_region_name = [
    [vnw, nw, n, ne, vne],
    [w, mw, c, me, e],
    [vsw, sw, s, se, vse]
]

regions_prefered_name_ranges = {
    vnw : {"pos": (0, 0), "name_range": (0, 66), "people": []},
    nw : {"pos": (0, 1), "name_range": (66, 132), "people": []},
    n : {"pos": (0, 2), "name_range": (132, 198), "people": []},
    ne : {"pos": (0, 3), "name_range": (198, 264), "people": []},
    vne : {"pos": (0, 4), "name_range": (264, 330), "people": []},
    w : {"pos": (1, 0), "name_range": (330, 396), "people": []},
    mw : {"pos": (1, 1), "name_range": (396, 462), "people": []},
    c : {"pos": (1, 2), "name_range": (462, 528), "people": []},
    me : {"pos": (1, 3), "name_range": (528, 594), "people": []},
    e : {"pos": (1, 4), "name_range": (594, 660), "people": []},
    vsw : {"pos": (2, 0), "name_range": (660, 726), "people": []},
    sw : {"pos": (2, 1), "name_range": (726, 792), "people": []},
    s : {"pos": (2, 2), "name_range": (792, 858), "people": []},
    se : {"pos": (2, 3), "name_range": (858, 924), "people": []},
    vse : {"pos": (2, 4), "name_range": (900, 999), "people": []},
}

gender_names = {}

def load_names(gender):
    with open(f"./assets/{gender}_names.txt", "r") as f:
        gender_names[gender] = set(f.read().split("\n"))
        
def get_person_name(gender: str, father_region: str = None, mother_region: str = None) -> str:
    if gender not in gender_names:
        load_names(gender)
    
    names = gender_names[gender]
    
    if father_region is None and mother_region is None:
        return random.choice(list(names))
    
    father_name_range = regions_prefered_name_ranges[father_region]["name_range"]
    mother_name_range = regions_prefered_name_ranges[mother_region]["name_range"]
    names_list = set(range(father_name_range[0], father_name_range[1])) | set(range(mother_name_range[0], mother_name_range[1]))
    return random.choices(list(names_list), k=1)[0]

birth_dates = defaultdict(lambda: defaultdict(int))

def load_json(file_path: str = str(WORLD_DATA_PATH)) -> dict:
    file_path = Path(file_path)
    with file_path.open("r") as f:
        return json.load(f)

def save_json(file_path: str = str(WORLD_DATA_PATH), new_data: dict = {}, indent=4) -> int:
    file_path = Path(file_path)
    with file_path.open("w") as f:
        if indent == 0:
            json.dump(new_data, f, indent=indent, ensure_ascii=False, cls=NumpyEncoder, separators=(",", ":"), allow_nan=False)
        else:
            json.dump(new_data, f, indent=indent, ensure_ascii=False, cls=NumpyEncoder)
    return 0

def save_display(data: dict):
    with open(DISPLAY_DATA_PATH, "w") as f:
        data_str = str(data)
        data_str = data_str.replace("\n", "").replace("\t", "").replace(" ", "").replace("None", "null")
        f.write(f"const data = {data_str}")
        
def reset_runtime():
    """
    resets the file 'runtime_data.json'
    """
    
    save_json(RUNTIME_DATA_PATH, {
        "created_ids": 0
    })
    

region_to_abbr = {
    vnw:  "VNW",
    nw:   "NW",
    n:    "N",
    ne:   "NE",
    vne:  "VNE",
    w:    "W",
    mw:   "MW",
    c:    "C",
    me:   "ME",
    e:    "E",
    vsw:  "VSW",
    sw:   "SW",
    s:    "S",
    se:   "SE",
    vse:  "VSE"
}

def get_person_id(gender, name, region):
    old = load_json(RUNTIME_DATA_PATH)
    create = f"{region_to_abbr[region]}-{gender[0]}-{name[0]}-{old['created_ids']+1}"
    old["created_ids"] += 1
    save_json(RUNTIME_DATA_PATH, old)
    return create

def clear():
    os.system('cls' if os.name=='nt' else 'clear')


def create_display_data():
    world_data_file = load_json() # that will load the world data : source defaults to world_data.json
    people_data = world_data_file["people"]
    world_population = len(people_data)
    regions = {}
    # sort people by their region
    for person in people_data.values():
        regions.setdefault(person["region"], []).append(person)
    
    # calculate averages for each region
    region_data = {}
    for region, people in regions.items():
        population = len(people)
        male_count = sum(person["genome"]["gender"] == "male" for person in people)
        female_count = population - male_count
        avg_population = 1 / population if population else 0
        region_data[region] = {
            "population": f"{population} - {population/world_population*100:.2f}%",
            "male_data": f"{male_count} - {male_count*avg_population*100:.2f}%",
            "female_data": f"{female_count} - {female_count*avg_population*100:.2f}%",
            "avg_money": round(sum(person["money"] for person in people) * avg_population, 2),
            "avg_health": round(sum(person["genome"]["health"] for person in people) * avg_population, 2),
            "avg_intelligence": round(sum(person["genome"]["intelligence"] for person in people) * avg_population, 2),
            "avg_charisma": round(sum(person["genome"]["charisma"] for person in people) * avg_population, 2),
            "avg_improve_rate": round(sum(person["genome"]["improve_rate"] for person in people) * avg_population, 2),
            "avg_age": round(sum(person["genome"]["age"] for person in people) * avg_population / 365, 2),
            "avg_ability_to_reproduce": round(sum(person["genome"]["ability_to_reproduce"] for person in people) * avg_population, 2),
            "avg_death_age": round(sum(person["genome"]["death_age"] for person in people) * avg_population / 365, 2),
            "avg_strength": round(sum(person["genome"]["strength"] for person in people) * avg_population, 2),
            "avg_beauty": round(sum(person["genome"]["beauty"] for person in people) * avg_population, 2),
        }
    
    save_json("./test.json", region_data)
    save_display(region_data)


if __name__ == "__main__":
    create_display_data()