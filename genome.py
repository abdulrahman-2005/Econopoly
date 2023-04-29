import numpy as np

YEAR_DAYS = 365

def genome(father_genome=None, mother_genome=None):
    gen = {}

    if father_genome is None and mother_genome is None:
        gen['gender'] = 'male' if np.random.randint(0, 5) < 2 else 'female'
        gen_values = {
            'health': (50, 100),
            'intelligence': (50, 100),
            'charisma': (50, 100),
            'ability_to_reproduce': (0, 100),
            'improve_rate': (0.01, 0.5),
            'age': (18 * YEAR_DAYS, 50 * YEAR_DAYS),
            'death_age': (68 * YEAR_DAYS, 100 * YEAR_DAYS), # assuming average lifespan of 68-100 years
            'strength': (70, 100) if gen['gender'] == 'male' else (30, 70),
            'beauty': (30, 70) if gen['gender'] == 'male' else (70, 100)
        }
    else:
        random_factor = 10
        
        # Calculate parents' combined ability to reproduce
        combined_ability_to_reproduce = (father_genome["ability_to_reproduce"] + mother_genome["ability_to_reproduce"]) / 2

        # Add random factor to combined ability to reproduce
        combined_ability_to_reproduce += np.random.randint(-random_factor, random_factor)

        # Generate random integer to determine sex of child
        gen["gender"] = "male" if np.random.randint(0, 99) < combined_ability_to_reproduce*.8 else "female"
        
        gen_values = {
            'health': ((father_genome['health'] + mother_genome['health']) / 2 - 10, (father_genome['health'] + mother_genome['health']) / 2 + 10),
            'intelligence': ((father_genome['intelligence'] + mother_genome['intelligence']) / 2 - 10, (father_genome['intelligence'] + mother_genome['intelligence']) / 2 + 10),
            'charisma': ((father_genome['charisma'] + mother_genome['charisma']) / 2 - 10, (father_genome['charisma'] + mother_genome['charisma']) / 2 + 10),
            'ability_to_reproduce': ((father_genome['ability_to_reproduce'] + mother_genome['ability_to_reproduce']) / 2 - 10, (father_genome['ability_to_reproduce'] + mother_genome['ability_to_reproduce']) / 2 + 10),
            'improve_rate': ((father_genome['improve_rate'] + mother_genome['improve_rate']) / 2 - 0.1, (father_genome['improve_rate'] + mother_genome['improve_rate']) / 2 + 0.1),
            'age': (0, 0),
            'death_age': ((father_genome['death_age'] + mother_genome['death_age']) / 2 - 10, (father_genome['death_age'] + mother_genome['death_age']) / 2 + 10),
            'strength': ((father_genome['strength'] + mother_genome['strength']) / 2 - 5, (father_genome['strength'] + mother_genome['strength']) / 2 + 15) if gen['gender'] == 'male' else ((father_genome['strength'] + mother_genome['strength']) / 2 - 15, (father_genome['strength'] + mother_genome['strength']) / 2 + 5),
            'beauty': ((father_genome['beauty'] + mother_genome['beauty']) / 2 - 15, (father_genome['beauty'] + mother_genome['beauty']) / 2 + 5) if gen['gender'] == 'male' else ((father_genome['beauty'] + mother_genome['beauty']) / 2 - 5, (father_genome['beauty'] + mother_genome['beauty']) / 2 + 15)
        }

    for key, value in gen_values.items():
        gen[key] = int(np.random.randint(value[0], value[1]+1))

    return gen

