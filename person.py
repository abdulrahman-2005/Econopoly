from genome import genome
import numpy as np
from utils import get_person_name, coord_to_region_name, get_person_id, clear


person_ = {
	"id": "",
	"name": "",
	"money": 0,
	"region": "",
	"full_name": "WORLD ",
	"targets": {
		"love": 1,
		"money": 50,
		"strength": 80,
		"beauty": 80,
	},
	"family": {
		"children": [],
		"partners": [],
		"current_partner": "partner_id",
		"family_rate": 0,
	},
	"work_status": {
		"experience": 0,
		"jobs": 0,
		"last_job": {},
		"current_job": {},
		"work_happiness": 0
	}
}

def get_targets(gender):
    if gender == "male":
        targets = {
            "love": np.random.choice([1, 1, 1, 0]),
            "money": np.random.randint(40, 101),
            "strength": np.random.randint(40, 101),
            "beauty": np.random.randint(30, 91)
        }
    else:
        targets = {
            "love": np.random.choice([1, 1, 0, 0]),
            "money": np.random.randint(50, 101),
            "strength": np.random.randint(20, 61),
            "beauty": np.random.randint(50, 101)
        }
        
    targets["money"] += np.random.randint(-10, 11)
    targets["strength"] += np.random.randint(-10, 11)
    targets["beauty"] += np.random.randint(-10, 11)
    
    return targets

def create_person(father=None, mother=None, date=None):
    p = person_.copy()
    p["needs"] = 50
    p["type"] = "person"
    
    if father is None and mother is None:
        p["genome"] = genome()
        p["name"] = get_person_name(p["genome"]["gender"])
        p["money"] = np.random.randint(10000, 1000001)
        p["full_name"] = f"{p['name']} {p['full_name']}"
        p["birth"] = {
            "date": date,
            "place": (coord:=(np.random.randint(0, 3), np.random.randint(0, 5))),
            "region": coord_to_region_name[coord[0]][coord[1]]
        }
    else:
        p["genome"] = genome(father["genome"], mother["genome"])
        p["name"] = get_person_name(p["genome"]["gender"], father["birth"]["region"], mother["birth"]["region"])
        p["full_name"] = f"{p['name']} {father['full_name']}"
        p["birth"] = {
            "date": date,
            "place": mother["birth"]["place"],
            "region": mother["birth"]["region"]
        }

    p["position"] = p["birth"]["place"]
    p["region"] = p["birth"]["region"]
    
    targets = get_targets(p["genome"]["gender"])
    p["targets"] = {k: v for k, v in targets.items()}
    p["targets"]["money"] = round(targets["money"] * (1 + (np.random.randint(-10, 11) / 100)), 2)
    p["targets"]["strength"] = round(targets["strength"] * (1 + (np.random.randint(-10, 11) / 100)), 2)
    p["targets"]["beauty"] = round(targets["beauty"] * (1 + (np.random.randint(-10, 11) / 100)), 2)
    
    p["id"] = get_person_id(gender=p["genome"]["gender"], name=p["name"], region=p["region"])
    
    return p