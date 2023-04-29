from person import create_person
from utils import coord_to_region_name, regions_prefered_name_ranges, load_json, save_json, save_display, reset_runtime
from bank import bank_, bank_account

world_template = {
	"NAME": "WORLD_0_1",
	"ID": "001",
	"date": 0,
	"bank": bank_.copy(),
	"regions_coord": coord_to_region_name.copy()
}


def world(starting_population: int = 1000):
    reset_runtime()
    w_ = world_template
    
    people = [create_person() for i in range(starting_population)]
    w_["people"] = people
        
    temp = {p["id"]: p for p in w_["people"]}
    w_["people"] = temp
    
    w_["dead_people"] = []
    w_["map"] = regions_prefered_name_ranges.copy()
    
    w_["companies"] = {}
    
    for p_id, person in w_["people"].items():
        w_["map"][person["region"]]["people"].append(p_id)
        
    save_json(new_data=w_)
    return w_

#THE ACTUAL HELL (WHAT RUNS THE SIMULATION)
def male__(person: dict, world):
	pass

def female__(person: dict, world):
	pass

def company__(company: dict, world):
	pass

bank_ = {
	"name": "WORLD_BANK",
	"owner": "WORLD",
	"accounts": {
		"world": bank_account(1_000_000_000_000, 9999),
		"company": {},
		"person": {}
	},
	"loans": {
		"company": {},
		"person": {}
	}
}


def bank__(world):
	bank_data = world["bank"]
	mod_data = bank_data.copy()
	#people loop
	for acc in bank_data:
		pass
	#account
	#tax

	#companies loop
	#account
	#tax

	#tax loop

def market__(world):
	pass

#MAIN LOOP

def main(new=False, years_to_simulate=10):
	if new:
		world_ = world(starting_population = int(input("[int] (population): ")))
	else:
		world_ = load_json()

	for i in range(years_to_simulate*365):
		world_["date"] += 1
		for p in world_["people"]:
			p = world_["people"][p]
			if p["genome"]["gender"] == "male":
				male__(p, world_)
			else:
				female__(p, world_)

		for c in world_["companies"]:
			c = world_["companies"][c]
			company__(c, world_)
    
		bank__(world_)
		market__(world_)

		

	save_json(new_data=world_)
	save_display(world_)

main(new=True)