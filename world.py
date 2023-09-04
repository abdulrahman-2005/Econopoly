import random
from person import create_person, person_die
from utils import load_json, save_json

default_world = {
    "starting_population": 100,
    "min_starting_money": 10_000,
    "max_starting_money": 300_000,
    "luck": .2222213,
    "company_required_bank_points": 12,
    "company_required_starting_cost": 100_000,
    "company_starting_min_person_balance": 200_000,
    "company_yearly_total_tax": .09,
    "person_yearly_total_tax": .3,
}


def new_world(initial_data: dict = default_world):
    people = [create_person() for _ in range(initial_data["starting_population"])]
    people_ = {}
    for person in people:
        people_[person["ID"]] = person
    people = people_
    del people_
    
    bank = {
        "world": {},
        "people": {},
        "companies": {}
    }
    for _, person in people.items():
        bank["people"][person["ID"]] = {
            "balance": random.randint(initial_data["min_starting_money"], initial_data["max_starting_money"])*(1+initial_data["luck"]),
            "stocks": {},
            "loans": [],
            "points": 0
        }
    
    bank["world"] = {
        "user_balance": (s:=sum([v["balance"] for k,v in bank["people"].items()])),
        "balance": 99999999*initial_data["starting_population"]-s,
    }
    
    
    return {
        "name": "WORLD",
        "initial_data": initial_data,
        "people": people,
        "dead_people": [],
        "bank": bank,
    }


def load_world(path: str) -> dict | ValueError:
    return load_json(path)

def save_world(path: str, world: dict) -> None:
    save_json(path, world)



def create_company_bank_account(world: dict, company: dict, person: dict) -> bool:
    min_balance = world["initial_data"]["company_required_starting_cost"]

    company_ID = company["ID"]
    
    if company_ID in world["bank"]["companies"]:
        company["ID"] = company_ID + "_"
    
    company_ID = company["ID"]
    
    world["bank"]["companies"][company_ID] = {
        "balance": min_balance,
        "stocks": {},
        "loans": [],
        "points": 0
    }
    
    world["bank"]["people"][person["ID"]]["balance"] -= min_balance
    
    return True

def person_(world: dict, person: dict) -> None:
    person["age"] += 1/365
    if person["age"] >= person["death_age"]:
        person_die(world, person)

def male_(world: dict, person: dict) -> None:
    person_(world, person)

def female_(world: dict, person: dict) -> None:
    person_(world, person)

def bank_(world) -> None:
    bank = world["bank"]
    pass


if __name__ == "__main__":
    world_bank = new_world()["bank"]
    print(world_bank["world"]["user_balance"])
    print(world_bank["world"]["balance"])