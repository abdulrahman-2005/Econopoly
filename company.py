import random
from world import create_company_bank_account

COMPANY = {
    "name": "",
    "ID": "",
    "owner": "",
    "market_data": {
        "evaluation": 0,
        "stock_price": 0,
    },
    "employees_ids": [],
    "employees_data": {},
    "products": [],
    "is_hiring": False
}

created_company_count = 0

slogs = ["CO", "LIMITED", "UNITED", "CENTRAL", "IO", "GIGA", "CORP", "INTERNATIONAL", "LTD", "NATIONAL"]
def generate_company_name_and_ID(person):
    
    global created_company_count
    
    generated_name = person["name"] + person["region"] + " " + random.choice(slogs)
    generated_ID = "".join([i.upper() for i in generated_name]) + str(created_company_count)
    
    created_company_count += 1
    
    return generated_name, generated_ID

def is_elegible_to_create_company(world: dict, person: dict) -> bool:
    person_bank_account = world["bank"]["people"][person["ID"]]
    
    print(person_bank_account)
    
    elegible = person_bank_account["points"] >= world["initial_data"]["company_required_bank_points"] and person_bank_account["balance"] >= world["initial_data"]["company_starting_min_person_balance"]
    return elegible

def create_company(world: dict, person: dict) -> bool:
    
    if not is_elegible_to_create_company(world, person):
        return False
    
    name, ID = generate_company_name_and_ID(person)
    
    created_company = COMPANY.copy()
    
    created_company["owner"] = person["ID"]
    created_company["name"] = name
    created_company["ID"] = ID
    
    create_company_bank_account(world, created_company, person)
    
    if person["companies"]:
        person["companies"].append(ID)
    
    return True

