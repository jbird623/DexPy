import yaml

with open('modified/pokedex.yaml', 'r') as input:
    pokedex = yaml.load(input.read())
    unique_keys = []
    skipped = []
    transfer = []
    for pokemon in pokedex:
        if pokemon == 'arcaninehisui':
            print(pokedex[pokemon])
        if 'battleOnly' in pokedex[pokemon]:
            skipped.append(pokemon)
            continue
        if 'isNonstandard' in pokedex[pokemon] and pokedex[pokemon]['isNonstandard'] == "Unobtainable":
            transfer.append(pokemon)
            continue
        if 'isNonstandard' in pokedex[pokemon] and (pokedex[pokemon]['isNonstandard'] == "CAP" or pokedex[pokemon]['isNonstandard'] == "Past" or pokedex[pokemon]['isNonstandard'] == "Unobtainable"or pokedex[pokemon]['isNonstandard'] == "Custom"):
            skipped.append(pokemon)
            continue
        if pokemon not in unique_keys:
            unique_keys.append(pokemon)

    with open(f'test.yaml', 'wt') as output:
        yaml.dump(unique_keys, stream=output)

    with open(f'skipped.yaml', 'wt') as output:
        yaml.dump(skipped, stream=output)

    with open(f'transfer.yaml', 'wt') as output:
        yaml.dump(transfer, stream=output)

