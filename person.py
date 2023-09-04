import random
from utils import coord_to_region, get_person_name, clear_terminal_screen

created_people_count = 0

MUTATION_VALUE = .05
GENDER_RATIO = .6 # ]0, 1[ ::: higher means more female
YEAR_DAYS = 365
gender_effect_on_atrributes = {
    "strength"    : [.8, 1.2],
    "charisma"    : [.7, .86],
    "beauty"      : [1.1, .8],
    "intelligence": [.9, 1],
    "focus"       : [.8, .9]
}

atrributes_affected_by_gender = [
    "strength",
    "charisma",
    "beauty",
    "intelligence",
    "focus"
]

general_attributes = [
    "expectency",
]

def person_atrributes(gender):
    out = {}
    value = random.random()
    for attr in atrributes_affected_by_gender:
        out[attr] = round(value * gender_effect_on_atrributes[attr][gender], 2)
    
    for attr in general_attributes:
        out[attr] = round( value + (random.randint(-1, 1)/random.randint(3,6)) ,2)
    
    return out

def inherit_atrributes(gender: int, father: dict, mother: dict):
    out = {}
    value = (random.random() * MUTATION_VALUE) * random.randint(-1, 1)
    for attr in atrributes_affected_by_gender:
        initial = (father["attributes"][attr]+mother["attributes"][attr])/2
        initial += value
        out[attr] = round(initial * gender_effect_on_atrributes[attr][gender], 2)
    
    for attr in general_attributes:
        initial = (father["attributes"][attr]+mother["attributes"][attr])/2
        initial += value
        out[attr] = round(initial, 2)
    
    return out

def create_person(father: dict = None, mother: dict = None):
    global created_people_count
    
    gender = 1 if random.random() > GENDER_RATIO else 0 # 0 -> female
    
    out = {
        "ID": (id_:=f"person-{created_people_count}"),
        "name": id_ + " WORLD_" if father is None and mother is None else get_person_name(gender, father, mother) + " " + father["name"],
        "partner": None,
        "children": None,
        "companies": None,
        "gender": ["female", "male"][gender],
        "attributes": person_atrributes(gender),
        "health": 100,
        "status": "born",
        "location": (loc:=[random.randint(0,2), random.randint(0, 4)]),
        "region": coord_to_region(loc)["name"],
        "age": (age:=round(random.randint(36, 100) * (random.randint(5, 10)/10), 2)),
        "death_age": age + random.randint(1, random.randint(5, 70)),
        "work": {
            "current_company": None,
            "last_company": None,
        }
    }
    
    if father and mother:
        out["attributes"] = inherit_atrributes(gender, father, mother)
        out["age"] = 0
        out["death_age"] = round(((father["death_age"]+mother["death_age"])/2)*(1/random.randint(1, 10)), 2)
        
    if gender == 0:
        out["pregnancy"] = None
    
    created_people_count += 1
    
    return out

def person_die(world: dict, person: dict) -> bool:    
    partner = person["partner"]
    children = person["children"]
    balance = world["bank"]["people"][person["ID"]]
    if partner:
        partner_inheritance = balance*.2
        balance -= partner_inheritance
        world["bank"]["people"][partner["ID"]]["balance"] += partner_inheritance
    
    if children:
        child_inheritance = balance/len(children)
        for child in children:
            world["bank"]["people"][child["ID"]]["balance"] += child_inheritance
    
    del world["bank"]["people"][person["ID"]]
    world["dead_people"].append(person["ID"])
    del world["people"][person["ID"]]
    
    #! still needs to inherit the companies stocks and stuff
    
    return True

def create_person_bank_account(world: dict, person: dict, starting_balance: int | float = 100000) -> None:
    if person["ID"] in world["bank"]["people"]:
        return False
    
    world["bank"]["people"][person["ID"]] = {
        "balance": starting_balance,
        "stocks": {},
        "loans": [],
        "points": 0
    }

def get_option(source: dict, desc: str):
    if "/" not in desc:
        return source[desc]
    
    desc = desc.split("/")
    data = ""
    for i in desc:
        data = data[i]
    return data

default_display = {
    "display": ["name","gender","region", "age"]
}

from tabulate import tabulate
from statistics import median, mean

def sort_by_age(person_id, person):
    return person["age"]

def sort_by_region(person_id, person):
    reg = person["region"]
    return sum(ord(reg[i]) * (i + 1) for i in range(len(reg)))

def sort_by_name(person_id, person):
    name = person["name"]
    return sum(ord(name[i]) * (i + 1) for i in range(len(name)))

def display_person(persons: dict, options: dict = default_display, sort_by="age"):
    headers = options["display"]

    sort_key = {
        "name": sort_by_name,
        "age": sort_by_age,
        "region": sort_by_region
    }[sort_by]

    sorted_persons = sorted(persons.items(), key=lambda x: sort_key(x[0], x[1]), reverse=True)

    data = [[person[thing] for thing in headers] for _, person in sorted_persons]
    clear_terminal_screen()
    print(tabulate(data, headers), end="\r")

default_average_numeric = [
    "age",
    "attributes/strength",
    "attributes/charisma",
    "attributes/beauty",
    "attributes/intelligence",
    "attributes/focus",
    "attributes/expectancy"
]


def calculate_averages_data(persons: list[dict], options: list=default_average_numeric):
    avgs = {}
    medians = {}
    minimums = {}
    maximums = {}
    for person in persons:
        for option in options:
            avgs[option].append(get_option(person, option))
    
    for k, v in avgs:
        medians[k] = median(v)
        minimums[k] = min(v)
        maximums[k] = max(v)
        avgs[k] = mean(v)
    
    return {
        "avgs": avgs,
        "medians": medians,
        "maximums": maximums,
        "minimums": minimums
    }