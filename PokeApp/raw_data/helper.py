import yaml

with open('abilities.txt', 'r') as input:
    pokedex = yaml.load(input.read())
    unique_keys = []
    for pokemon in pokedex:
        for key in pokedex[pokemon]:
            if key not in unique_keys:
                unique_keys.append(key)

    for key in unique_keys:
        print(key)