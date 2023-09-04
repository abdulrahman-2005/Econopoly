from world import new_world, save_world, default_world
from person import display_person, create_person, person_die, create_person_bank_account
from company import create_company

# default_world["starting_population"] = 100000

world = new_world()

test_person = create_person()


test_person["name"] = "-------------------------------------------------"
test_person["age"] = 10000
world["people"][test_person["ID"]] = test_person

create_person_bank_account(world, person=test_person, starting_balance=200000)
world["bank"]["people"]

create_company(world, person=test_person)
create_company(world, person=test_person)
create_company(world, person=test_person)
create_company(world, person=test_person)

#person_die(world, test_person)
display_person(world["people"])

save_world("./world.json", world)

