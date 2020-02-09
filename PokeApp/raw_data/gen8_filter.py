import yaml

from pprint import pprint

source_dir = 'modified'
destination_dir = 'gen8'

def transform_entry(pokedex_entry):
    abilities = pokedex_entry['abilities']
    ability_list = []
    if '0' in abilities:
        ability_list.append(abilities['0'].lower())
    if '1' in abilities:
        ability_list.append(abilities['1'].lower())
    if 'H' in abilities:
        ability_list.append(abilities['H'].lower())
    pokedex_entry['ability_list'] = ability_list
    return pokedex_entry

def transform_learnset(learnset):
    entry = dict()
    moves = learnset['learnset']
    machine_moves = []
    egg_moves = []
    level_up_moves = []
    for move in moves:
        learn_array = moves[move]
        for learn_method in learn_array:
            if learn_method[:1] == '8':
                method = learn_method[1:]
                if method == 'M':
                    machine_moves.append(move)
                if method == 'E':
                    egg_moves.append(move)
                if method[:1] == 'L':
                    level_up_moves.append(move)
    entry['machine'] = machine_moves
    entry['breeding'] = egg_moves
    entry['levelup'] = level_up_moves
    return entry

def transform_move(move):
    return move

def transform_ability(ability):
    return ability

def main():
    gen8dex = filter_pokedex()
    gen8learnsets = filter_learnsets(gen8dex)
    gen8moves = filter_moves()
    gen8abilities = filter_abilities()
    print('Done!')

def filter_pokedex():
    print('Filtering Pokedex...')
    gen8dex = dict()

    with open(f'{source_dir}/pokedex.txt', 'r') as input:
        pokedex = yaml.load(input.read(), Loader=yaml.SafeLoader)

        ignore_list = ['basculinbluestriped','keldeoresolute']
        
        for pokemon in pokedex:
            isGen8 = True
            for key in pokedex[pokemon]:
                if key == 'isNonstandard':
                    isGen8 = False
                    break
                if key == 'tier' and pokedex[pokemon]['tier'] == 'Unreleased':
                    isGen8 = False
                    break
                #if key == 'baseSpecies':
                #    if pokemon[-5:] != 'galar' and pokemon[-5:] != 'alola':
                #        isGen8 = False
                #        break
                if key == 'battleOnly' and pokedex[pokemon]['battleOnly'] == True:
                    isGen8 = False
                    break
            
            if pokemon[-4:] == 'gmax':
                isGen8 = False

            if pokemon[-4:] == 'mega':
                isGen8 = False

            if pokemon[:9] == 'pumpkaboo' and pokemon != 'pumpkaboo':
                isGen8 = False

            if pokemon[:9] == 'gourgeist' and pokemon != 'gourgeist':
                isGen8 = False

            if pokemon[:8] == 'silvally' and pokemon != 'silvally':
                isGen8 = False

            if pokemon in ignore_list:
                isGen8 = False

            if isGen8:
                gen8dex[pokemon] = transform_entry(pokedex[pokemon])
                #print(pokemon)

        with open(f'{destination_dir}/gen8_pokedex.txt', 'wt') as output:
            pprint(gen8dex, stream=output, compact=True)

    return gen8dex

def filter_learnsets(gen8dex):
    print('Filtering Learnsets...')
    gen8learnsets = dict()

    with open(f'{source_dir}/learnsets.txt', 'r') as input:
        learnsets = yaml.load(input.read(), Loader=yaml.SafeLoader)

        for pokemon in learnsets:
            if pokemon in gen8dex:
                gen8learnsets[pokemon] = transform_learnset(learnsets[pokemon])
        
        with open(f'{destination_dir}/gen8_learnsets.txt', 'wt') as output:
            pprint(gen8learnsets, stream=output, compact=True)
    
    return gen8learnsets

def filter_moves():
    print('Filtering Moves...')
    gen8moves = dict()

    with open(f'{source_dir}/moves.txt', 'r') as input:
        moves = yaml.load(input.read(), Loader=yaml.SafeLoader)

        for move in moves:
            isGen8 = True
            for key in moves[move]:
                if key == 'isNonstandard':
                    isGen8 = False
                    break
            if isGen8:
                gen8moves[move] = transform_move(moves[move])
        
        with open(f'{destination_dir}/gen8_moves.txt', 'wt') as output:
            print(gen8moves, file=output)
    
    return gen8moves

def filter_abilities():
    print('Filtering Abilities...')
    gen8abilities = dict()

    with open(f'{source_dir}/abilities.txt', 'r') as input:
        abilities = yaml.load(input.read(), Loader=yaml.BaseLoader)

        for ability in abilities:
            isGen8 = True
            for key in abilities[ability]:
                if key == 'isNonstandard':
                    isGen8 = False
                    break
            if isGen8:
                gen8abilities[ability] = transform_ability(abilities[ability])
        
        with open(f'{destination_dir}/gen8_abilities.txt', 'wt') as output:
            print(gen8abilities, file=output)
    
    return gen8abilities

main()