import yaml

from pprint import pprint

source_dir = 'modified'
destination_dir = 'gen8'

def transform_entry(pokedex_entry, id, transfer_only_list):
    abilities = pokedex_entry['abilities']
    ability_list = []
    if '0' in abilities:
        ability_list.append(abilities['0'].lower().replace(' ',''))
    if '1' in abilities:
        ability_list.append(abilities['1'].lower().replace(' ',''))
    if 'H' in abilities:
        ability_list.append(abilities['H'].lower().replace(' ',''))
    pokedex_entry['ability_list'] = ability_list
    egg_groups = pokedex_entry['eggGroups']
    egg_group_list = []
    for group in egg_groups:
        egg_group_list.append(group.lower().replace(' ',''))
    bst = 0
    for stat in pokedex_entry['baseStats']:
        bst += pokedex_entry['baseStats'][stat]
    pokedex_entry['baseStats']['bst'] = bst
    pokedex_entry['eggGroups'] = egg_group_list
    pokedex_entry['transfer_only'] = (id in transfer_only_list)
    return pokedex_entry

def transform_learnset(learnset):
    entry = dict()
    moves = learnset['learnset']
    machine_moves = []
    egg_moves = []
    level_up_moves = []
    tutor_moves = []
    all_moves = []
    transfer_moves = []
    transfer_dict = dict()
    for move in moves:
        learn_array = moves[move]
        for learn_method in learn_array:
            if learn_method[:1] == '8':
                method = learn_method[1:]
                if method == 'M':
                    machine_moves.append(move)
                    if move not in all_moves:
                        all_moves.append(move)
                elif method == 'E':
                    egg_moves.append(move)
                    if move not in all_moves:
                        all_moves.append(move)
                elif method[:1] == 'L':
                    level_up_moves.append(move)
                    if move not in all_moves:
                        all_moves.append(move)
                elif method[:1] == 'T':
                    tutor_moves.append(move)
                    if move not in all_moves:
                        all_moves.append(move)
            elif move not in all_moves:
                method = learn_method[1:]
                if method == 'M':
                    method = 'TM/TR'
                elif method == 'E':
                    method = 'Breeding'
                elif method[:1] == 'L':
                    method = 'Level Up'
                elif method[:1] == 'T':
                    method = 'Tutor'
                elif method == 'V':
                    method = 'Virtual Console'
                elif method[:1] == 'S':
                    method = 'Special'
                if move in transfer_dict:
                    if method not in transfer_dict[move]:
                        transfer_dict[move].append(method)
                else:
                    transfer_dict[move] = [method]
    for move in transfer_dict:
        transfer_moves.append({'move':move, 'method':', '.join(transfer_dict[move])})
    entry['machine'] = machine_moves
    entry['breeding'] = egg_moves
    entry['levelup'] = level_up_moves
    entry['tutor'] = tutor_moves
    entry['allmoves'] = all_moves
    entry['transfer'] = transfer_moves
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

    with open(f'{source_dir}/transfer_only.txt', 'r') as input:
        transfer_only_list = yaml.load(input.read(), Loader=yaml.SafeLoader)

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
                gen8dex[pokemon] = transform_entry(pokedex[pokemon], pokemon, transfer_only_list)
                #print(pokemon)

        with open(f'{destination_dir}/gen8_pokedex.txt', 'wt') as output:
            yaml.dump(gen8dex, stream=output)

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
            yaml.dump(gen8learnsets, stream=output)
    
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
            yaml.dump(gen8moves, stream=output)
    
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
            yaml.dump(gen8abilities, stream=output)
    
    return gen8abilities

main()