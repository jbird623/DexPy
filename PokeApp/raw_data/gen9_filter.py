import yaml
import re

from pprint import pprint

source_dir = 'modified'
destination_dir = 'gen9'

def transform_entry(pokedex_entry, id, base_game_list, transfer_only_list, gen8_list):
    abilities = pokedex_entry['abilities']
    ability_list = []
    if '0' in abilities:
        ability_list.append(re.sub(r'\W+', '', abilities['0'].lower()))
    if '1' in abilities:
        ability_list.append(re.sub(r'\W+', '', abilities['1'].lower()))
    if 'H' in abilities:
        ability_list.append(re.sub(r'\W+', '', abilities['H'].lower()))
    pokedex_entry['ability_list'] = ability_list
    egg_groups = pokedex_entry['eggGroups']
    egg_group_list = []
    for group in egg_groups:
        egg_group_list.append(group.lower().replace(' ',''))
    bst = 0
    for stat in pokedex_entry['baseStats']:
        bst += pokedex_entry['baseStats'][stat]
    pokedex_entry['species'] = pokedex_entry.pop('name')
    if 'prevo' in pokedex_entry:
        pokedex_entry['prevo'] = re.sub(r'\W+', '', pokedex_entry['prevo'].lower())
    if 'evos' in pokedex_entry:
        evos = pokedex_entry['evos']
        evo_list = []
        for evo in evos:
            evo_list.append(re.sub(r'\W+', '', evo.lower()))
        pokedex_entry['evos'] = evo_list
    pokedex_entry['baseStats']['bst'] = bst
    pokedex_entry['eggGroups'] = egg_group_list
    pokedex_entry['base_game'] = (id in base_game_list)
    pokedex_entry['transfer_only'] = (id in transfer_only_list)
    pokedex_entry['gen8'] = (id in gen8_list)
    pokedex_entry['past_only'] = (id not in base_game_list and id not in transfer_only_list)
    return pokedex_entry

def transform_learnset(learnset):
    entry = dict()
    moves = learnset['learnset']
    machine_moves = []
    egg_moves = []
    level_up_moves = []
    move_levels = dict()
    tutor_moves = []
    all_moves = []
    transfer_moves = []
    transfer_dict = dict()
    for move in moves:
        learn_array = moves[move]
        for learn_method in learn_array:
            if learn_method[:1] == '9':
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
                    level = method[1:]
                    move_levels[move] = int(level)
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
    entry['movelevels'] = move_levels
    entry['tutor'] = tutor_moves
    entry['allmoves'] = all_moves
    entry['transfer'] = transfer_moves
    return entry

def transform_move(move, isPast):
    move['past_only'] = isPast
    return move

def transform_ability(ability, isPast):
    ability['past_only'] = isPast
    return ability

def main():
    gen9dex = filter_pokedex()
    gen9learnsets = filter_learnsets(gen9dex)
    gen9moves = filter_moves()
    gen9abilities = filter_abilities()
    print('Done!')

def filter_pokedex():
    print('Filtering Pokedex...')
    gen9dex = dict()

    with open(f'{source_dir}/base_game.yaml', 'r') as input:
        base_game_list = yaml.load(input.read(), Loader=yaml.SafeLoader)

    with open(f'{source_dir}/transfer_only.yaml', 'r') as input:
        transfer_only_list = yaml.load(input.read(), Loader=yaml.SafeLoader)

    with open(f'{source_dir}/gen8/base_game.yaml', 'r') as input:
        gen8_base = yaml.load(input.read(), Loader=yaml.SafeLoader)
    with open(f'{source_dir}/gen8/transfer_only.yaml', 'r') as input:
        gen8_transfer = yaml.load(input.read(), Loader=yaml.SafeLoader)
    with open(f'{source_dir}/gen8/isle_of_armor.yaml', 'r') as input:
        gen8_ioa = yaml.load(input.read(), Loader=yaml.SafeLoader)
    with open(f'{source_dir}/gen8/crown_tundra.yaml', 'r') as input:
        gen8_ct = yaml.load(input.read(), Loader=yaml.SafeLoader)
    
    gen8_list = gen8_base + gen8_transfer + gen8_ioa + gen8_ct

    with open(f'{source_dir}/pokedex.yaml', 'r') as input:
        pokedex = yaml.load(input.read(), Loader=yaml.SafeLoader)

        ignore_list = ['basculinbluestriped','keldeoresolute','polteageistantique','sinisteaantique', 'floetteeternal',
                       'giratinaorigin', 'hoopaunbound', 'pichuspikyeared', 'shayminsky', 'vivillonpokeball', 'zygarde10']
        outputList = []

        for pokemon in pokedex:
            isGen9 = True
            isPast = False
            for key in pokedex[pokemon]:
                if key == 'isNonstandard':
                    if pokedex[pokemon]['isNonstandard'].lower() == 'past' or pokedex[pokemon]['isNonstandard'].lower() == 'unobtainable':
                        isPast = True
                    else:
                        isGen9 = False
                    break
                if key == 'tier' and pokedex[pokemon]['tier'].lower() == 'unreleased':
                    isPast = True
                    break
                #if key == 'baseSpecies':
                if key == 'battleOnly':
                    isGen9 = False
                    break
            
            if pokemon[-4:] == 'gmax':
                isGen9 = False

            if pokemon[-4:] == 'mega' or pokemon[-5:] == 'megay' or pokemon[-5:] == 'megax':
                isGen9 = False

            if pokemon[-5:] == 'totem':
                isGen9 = False

            if pokemon[-6:] == 'primal':
                isGen9 = False

            if pokemon[-7:] == 'therian':
                isGen9 = False

            if pokemon[:9] == 'pumpkaboo' and pokemon != 'pumpkaboo':
                isGen9 = False

            if pokemon[:9] == 'gourgeist' and pokemon != 'gourgeist':
                isGen9 = False

            if pokemon[:8] == 'silvally' and pokemon != 'silvally':
                isGen9 = False

            if pokemon[:6] == 'arceus' and pokemon != 'arceus':
                isGen9 = False

            if pokemon[:6] == 'deoxys' and pokemon != 'deoxys':
                isGen9 = False

            if pokemon[:8] == 'genesect' and pokemon != 'genesect':
                isGen9 = False

            if pokemon[:8] == 'oricorio' and pokemon != 'oricorio':
                isGen9 = False

            if pokemon[:7] == 'pikachu' and pokemon != 'pikachu':
                isGen9 = False

            if pokemon in ignore_list:
                isGen9 = False

            if isGen9:
                gen9dex[pokemon] = transform_entry(pokedex[pokemon], pokemon, base_game_list, transfer_only_list, gen8_list)
                #print(pokemon)

        #for id in outputList:
        #    print(id)

        with open(f'{destination_dir}/gen9_pokedex.yaml', 'wt') as output:
            yaml.dump(gen9dex, stream=output)

    return gen9dex

def filter_learnsets(gen9dex):
    print('Filtering Learnsets...')
    gen9learnsets = dict()

    with open(f'{source_dir}/learnsets.yaml', 'r') as input:
        learnsets = yaml.load(input.read(), Loader=yaml.SafeLoader)

        for pokemon in learnsets:
            if pokemon in gen9dex:
                try:
                    gen9learnsets[pokemon] = transform_learnset(learnsets[pokemon])
                except:
                    print(f'Skipping learnset for {pokemon}')
        
        with open(f'{destination_dir}/gen9_learnsets.yaml', 'wt') as output:
            yaml.dump(gen9learnsets, stream=output)
    
    return gen9learnsets

def filter_moves():
    print('Filtering Moves...')
    gen9moves = dict()

    with open(f'{source_dir}/moves.yaml', 'r') as input:
        moves = yaml.load(input.read(), Loader=yaml.SafeLoader)

        for move in moves:
            isGen9 = True
            isPast = False
            for key in moves[move]:
                if key == 'isNonstandard':
                    if moves[move]['isNonstandard'].lower() == 'past':
                        isPast = True
                    else:
                        isGen9 = False
                    break
            if isGen9:
                gen9moves[move] = transform_move(moves[move], isPast)
        
        with open(f'{destination_dir}/gen9_moves.yaml', 'wt') as output:
            yaml.dump(gen9moves, stream=output)
    
    return gen9moves

def filter_abilities():
    print('Filtering Abilities...')
    gen9abilities = dict()

    with open(f'{source_dir}/abilities.yaml', 'r') as input:
        abilities = yaml.load(input.read(), Loader=yaml.SafeLoader)

        for ability in abilities:
            isGen9 = True
            isPast = False
            for key in abilities[ability]:
                if key == 'isNonstandard':
                    if abilities[ability]['isNonstandard'].lower() == 'past':
                        isPast = True
                    else:
                        isGen9 = False
                    break
            if isGen9:
                gen9abilities[ability] = transform_ability(abilities[ability], isPast)
        
        with open(f'{destination_dir}/gen9_abilities.yaml', 'wt') as output:
            yaml.dump(gen9abilities, stream=output)
    
    return gen9abilities

main()