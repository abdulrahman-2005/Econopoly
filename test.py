import random, json
from utils import load_json
from genome import genome


world_data_file = load_json() # that will load the world data : source defaults to world_data.json
people_data = world_data_file["people"]
length = len(people_data)

def get_gender():
    
    mother = False
    father = False

    lst_ = list(people_data.values())
    while not mother or not father:
        choice = random.choice(lst_)

        if choice["genome"]["gender"] == "female":
            mother = choice
        else:
            father = choice
    return genome(father["genome"], mother["genome"])["gender"]

#male = 0
#for i in range(1000):
#    male += 1 if get_gender() == "male" else 0
#print(f"male: {male},  female: {1000-male}, percentage: {round(male/1000*100, 2)}%")


# data = [father["genome"], mother["genome"], genome(father["genome"], mother["genome"])]
    
#[print(json.dumps(e, indent=4)) for e in data]

print(get_gender())