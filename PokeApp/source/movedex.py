from .pokewrap import PokeMongo9
from .pokehelper import PokemonHelper
from pprint import pprint

import statistics
import random
import re

class MoveDex:
    def __init__(self, pokemongo):
        self.pokemongo = pokemongo

    def do_move_search_function(self, move, show_list, filters, print_to, full_desc=False):
        m_entry = self.pokemongo.get_move_entry(move)
        if m_entry is None:
            print(f'Error: Move "{move}" not found, bzzzzrt!', file=print_to)
            return

        if m_entry['past_only']:
            print('[NOTE: This move is not available in the Gen 9 games, bzzzzrt!]\n', file=print_to)

        print(f'Entry for {m_entry["name"]}:\n', file=print_to)

        print(f'Type: {m_entry["type"]}', file=print_to)

        category = m_entry['category']
        print(f'Category: {category}', file=print_to)

        power = m_entry['basePower']
        accuracy = m_entry['accuracy']

        if 'ohko' in m_entry:
            power = 'OHKO'
        elif power == 0:
            if category == 'Physical' or category == 'Special':
                power = 'Varies'
            else:
                power = '-'
        if accuracy == True:
            accuracy = '-'
        print(f'Base Power: {power}\nAccuracy: {accuracy}', file=print_to)

        print(f'Priority: {m_entry["priority"]}', file=print_to)

        print(f'Power Points: {m_entry["pp"]}', file=print_to)

        short_desc = 'No description available.'
        if 'shortDesc' in m_entry:
            short_desc = m_entry['shortDesc']
        desc = 'No description available.'
        if 'desc' in m_entry:
            desc = m_entry['desc']
        print(f'Description: {short_desc}', file=print_to)
        if full_desc:
            print(f'Full Description: {desc}', file=print_to)

        if not show_list:
            return

        move_name = move
        if 'name' in m_entry:
            move_name = m_entry['name']

        levelup_list = self.pokemongo.get_pokemon_with_move_levelup(move, print_to, filters=filters)
        machine_list = self.pokemongo.get_pokemon_with_move_machine(move, print_to, filters=filters)
        breeding_list = self.pokemongo.get_pokemon_with_move_breeding(move, print_to, filters=filters)
        tutor_list = self.pokemongo.get_pokemon_with_move_tutor(move, print_to, filters=filters)

        print('', file=print_to)

        past_pokemon = False
        if len(levelup_list) == 0 and len(machine_list) == 0 and len(breeding_list) == 0 and len(tutor_list) == 0:
            if len(filters) == 0:
                print(f'No pokemon can learn {move_name} in Gen 9 games, bzzzzrt!', file=print_to)
            else:
                print(f'No pokemon that fit the specified filters can learn {move_name} in Gen 9 games, bzzzzrt!', file=print_to)
            return
        if len(levelup_list) > 0:
            print(f'Pokemon that learn {move_name} by level up:', file=print_to)
            for pokemon in levelup_list:
                species = pokemon['species']
                if pokemon['past_only']:
                    species = f'*{species}'
                    past_pokemon = True
                print(f'  - {species}', file=print_to)
            print('', file=print_to)
        if len(machine_list) > 0:
            print(f'Pokemon that learn {move_name} by TM/TR:', file=print_to)
            for pokemon in machine_list:
                species = pokemon['species']
                if pokemon['past_only']:
                    species = f'*{species}'
                    past_pokemon = True
                print(f'  - {species}', file=print_to)
            print('', file=print_to)
        if len(breeding_list) > 0:
            print(f'Pokemon that learn {move_name} by breeding:', file=print_to)
            for pokemon in breeding_list:
                species = pokemon['species']
                if pokemon['past_only']:
                    species = f'*{species}'
                    past_pokemon = True
                print(f'  - {species}', file=print_to)
            print('', file=print_to)
        if len(tutor_list) > 0:
            print(f'Pokemon that learn {move_name} by tutor:', file=print_to)
            for pokemon in tutor_list:
                species = pokemon['species']
                if pokemon['past_only']:
                    species = f'*{species}'
                    past_pokemon = True
                print(f'  - {species}', file=print_to)
            print('', file=print_to)

        if past_pokemon:
            print('* Pokemon not available in Gen 9 games.', file=print_to)

    def do_moves_function(self, pokemon, filters, show_stab=False, max_stab=5, ignore_stats=False, show_coverage=False, max_coverage=3,
                          show_transfers=False, show_past=False, atk_override=None, spa_override=None, def_override=None, accuracy_check=False, ability=None, print_to=None):
        dex_entry = self.pokemongo.get_pokedex_entry(pokemon)
        if dex_entry is None:
            print(f'Error: No dex entry found for "{pokemon}", bzzzzrt!', file=print_to)
            return

        learnset = self.pokemongo.get_learnset(pokemon)
        if learnset is None:
            print(f'Error: No learnset found for "{pokemon}", bzzzzrt!', file=print_to)
            return

        if not show_past:
            filters['past'] = 'false'

        breeding_entries = self.pokemongo.get_move_entries(learnset['breeding'], print_to, filters)
        machine_entries = self.pokemongo.get_move_entries(learnset['machine'], print_to, filters)
        levelup_entries = self.pokemongo.get_move_entries(learnset['levelup'], print_to, filters)
        move_levels = learnset['movelevels']
        tutor_entries = self.pokemongo.get_move_entries(learnset['tutor'], print_to, filters)
        transfer_entries = []
        if show_transfers:
            transfer_entries = self.pokemongo.get_transfer_move_entries(learnset['transfer'], print_to, filters)

        all_moves = dict()
        for move in levelup_entries:
            level = move_levels[move['_id']]
            all_moves[move['_id']] = {'method':"Evolve" if level == "0" else f'Level {level}', 'move':move}
        for move in machine_entries:
            if move['_id'] not in all_moves:
                all_moves[move['_id']] = {'method':'TM/TR', 'move':move}
        for move in breeding_entries:
            if move['_id'] not in all_moves:
                all_moves[move['_id']] = {'method':'Breeding', 'move':move}
        for move in tutor_entries:
            if move['_id'] not in all_moves:
                all_moves[move['_id']] = {'method':'Tutor', 'move':move}
        if show_transfers:
            for move in transfer_entries:
                if move['_id'] not in all_moves:
                    all_moves[move['_id']] = {'method':'Transfer', 'move':move}

        if dex_entry['past_only']:
            print('[NOTE: This Pokemon is not transferrable to Gen 9 games, bzzzzrt!]\n', file=print_to)

        if show_stab:
            self.show_stab_moves(max_stab, ignore_stats, dex_entry, all_moves,
                                 atk_override, spa_override, def_override, accuracy_check, ability, print_to)

        if show_coverage:
            self.show_coverage_moves(max_coverage, ignore_stats, dex_entry, all_moves,
                                     atk_override, spa_override, def_override, accuracy_check, ability, print_to)

        offensive_abilities = PokemonHelper().get_offensive_ability_dict()
        if ability in offensive_abilities:
            print(f'\n* Moves calculated with the {offensive_abilities[ability]} ability.', file=print_to)
            if ability not in dex_entry['ability_list']:
                print(f'* This pokemon cannot naturally have this ability.', file=print_to)

        if show_coverage or show_stab:
            return
                    
        self.show_all_moves(breeding_entries, machine_entries, levelup_entries, move_levels, tutor_entries, transfer_entries, dex_entry, ability, ignore_stats, 'o' not in filters, print_to)

        if show_past:
            print('* Move not available in Gen 9 games.', file=print_to)

    def show_all_moves(self, breeding_entries, machine_entries, levelup_entries, move_levels, tutor_entries, transfer_entries, dex_entry, ability, ignore_stats, reorder, print_to):
        print('Level Up Moves:', file=print_to)
        if len(levelup_entries) == 0:
            print('  None', file=print_to)
        for move in self.format_moves(levelup_entries, dex_entry, ability=ability, ignore_stats=ignore_stats, move_levels=move_levels, reorder=reorder):
            self.print_move(move, ignore_stats, print_to)

        print('\nTM/TR Moves:', file=print_to)
        if len(machine_entries) == 0:
            print('  None', file=print_to)
        for move in self.format_moves(machine_entries, dex_entry, ability=ability, ignore_stats=ignore_stats):
            self.print_move(move, ignore_stats, print_to)

        if len(breeding_entries) > 0:
            print('\nEgg Moves:', file=print_to)
            for move in self.format_moves(breeding_entries, dex_entry, ability=ability, ignore_stats=ignore_stats):
                self.print_move(move, ignore_stats, print_to)

        if len(tutor_entries) > 0:
            print('\nMove Tutor Moves:', file=print_to)
            for move in self.format_moves(tutor_entries, dex_entry, ability=ability, ignore_stats=ignore_stats):
                self.print_move(move, ignore_stats, print_to)

        past_moves = False
        if len(transfer_entries) > 0:
            print('\nTransfer-Only Moves:', file=print_to)
            for move in self.format_moves(transfer_entries, dex_entry, ability=ability, ignore_stats=ignore_stats):
                if move['name'][0] == '*':
                    past_moves = True
                self.print_move(move, ignore_stats, print_to)

        if past_moves:
            print('\n* Move not available in Gen 9 games.', file=print_to)

    def show_stab_moves(self, max_stab, ignore_stats, dex_entry, all_moves, atk_override, spa_override, def_override, accuracy_check, ability, print_to):
        print(f'Top moves with STAB for {dex_entry["species"]}:', file=print_to)
        printed_moves = False
        for elemental_type in dex_entry['types']:
            top_moves = self.find_strongest_moves_of_type(all_moves, elemental_type, max_stab, dex_entry, atk_override, spa_override, def_override, accuracy_check, ability, ignore_stats)
            if len(top_moves) == 0:
                continue
            printed_moves = True
            num_moves = min(max_stab, len(top_moves))
            self.print_top_moves(top_moves, num_moves, elemental_type, ignore_stats, print_to)
        if not printed_moves:
            print('  None', file=print_to)
        print('', file=print_to)

    def show_coverage_moves(self, max_coverage, ignore_stats, dex_entry, all_moves, atk_override, spa_override, def_override, accuracy_check, ability, print_to):
        print(f'Top coverage moves for {dex_entry["species"]}:', file=print_to)
        printed_moves = False
        for elemental_type in PokemonHelper().get_types():
            if elemental_type in dex_entry['types']:
                continue
            top_moves = self.find_strongest_moves_of_type(all_moves, elemental_type, max_coverage, dex_entry, atk_override, spa_override, def_override, accuracy_check, ability, ignore_stats)
            if len(top_moves) == 0:
                continue
            printed_moves = True
            num_moves = min(max_coverage, len(top_moves))
            self.print_top_moves(top_moves, num_moves, elemental_type, ignore_stats, print_to)
        if not printed_moves:
            print('  None', file=print_to)
        print('', file=print_to)

    def find_strongest_moves_of_type(self, moves, elemental_type, num, dex_entry, atk_override, spa_override, def_override, accuracy_check, ability, ignore_stats):
        type_moves = self.filter_moves_by_type(moves, elemental_type, dex_entry, atk_override, spa_override, def_override, accuracy_check, ability, ignore_stats)
        type_moves.sort(key=self.acc_sort, reverse=True)
        type_moves.sort(key=self.pow_sort, reverse=True)
        return type_moves[:num]

    def filter_moves_by_type(self, moves, elemental_type, dex_entry, atk_override, spa_override, def_override, accuracy_check, ability, ignore_stats):
        type_moves = []
        for move in moves:
            if moves[move]['move']['type'] == 'Normal':
                if ability == 'aerilate':
                    moves[move]['move']['type'] = 'Flying'
                    moves[move]['move']['basePower'] = int(moves[move]['move']['basePower'] * 1.2)
                if ability == 'galvanize':
                    moves[move]['move']['type'] = 'Electric'
                    moves[move]['move']['basePower'] = int(moves[move]['move']['basePower'] * 1.2)
                if ability == 'normalize':
                    moves[move]['move']['basePower'] = int(moves[move]['move']['basePower'] * 1.2)
                if ability == 'pixilate':
                    moves[move]['move']['type'] = 'Fairy'
                    moves[move]['move']['basePower'] = int(moves[move]['move']['basePower'] * 1.2)
                if ability == 'refrigerate':
                    moves[move]['move']['type'] = 'Ice'
                    moves[move]['move']['basePower'] = int(moves[move]['move']['basePower'] * 1.2)
            if 'sound' in moves[move]['move']['flags']:
                if 'ability' == 'liquidvoice':
                    moves[move]['move']['type'] = 'Water'
            if moves[move]['move']['type'] == elemental_type:
                if moves[move]['move']['category'] == 'Status':
                    continue
                type_move = moves[move]['move']
                type_move['method'] = moves[move]['method']
                type_moves.append(type_move)
        return self.format_moves(type_moves, dex_entry, atk_override, spa_override, def_override, accuracy_check, ability, ignore_stats)

    def format_moves(self, moves, dex_entry, atk_override=None, spa_override=None, def_override=None, accuracy_check=False, ability=None, ignore_stats=False, orderby_key=None, move_levels=None, reorder=False):
        formatted_moves = []
        for move in moves:
            orderby_value = None
            if orderby_key is not None:
                orderby_value = move
                orderby_keys = orderby_key.split('.')
                for key in orderby_keys:
                    try:
                        orderby_value = orderby_value[key]
                    except:
                        orderby_value = 'N/A'
            method = ''
            level = ''
            if 'method' in move:
                method = move['method']
            elif move_levels is not None and move['_id'] in move_levels:
                level = move_levels[move['_id']]
                method = "Evolve" if level == "0" else f'Level {level}'
            modified_power = int(move['basePower'])
            move_type = move['category']
            base_power_str = str(modified_power)
            acc = int(move['accuracy'])
            if dex_entry:
                if 'overrideOffensiveStat' in move:
                    if def_override is None:
                        attack_mod = int(dex_entry['baseStats']['def'])
                    else:
                        attack_mod = def_override
                elif move_type == 'Special':
                    if spa_override is None:
                        attack_mod = int(dex_entry['baseStats']['spa'])
                    else:
                        attack_mod = spa_override
                elif move_type == 'Physical':
                    if atk_override is None:
                        attack_mod = int(dex_entry['baseStats']['atk'])
                    else:
                        attack_mod = atk_override
                else:
                    attack_mod = 0
                if move_type == 'Physical':
                    if ability == 'hustle':
                        move['basePower'] = int(int(move['basePower']) * 1.5)
                        if acc >= 20:
                            acc = acc - 20
                    if ability == 'hugepower' or ability == 'purepower':
                        move['basePower'] = int(move['basePower']) * 2
                if move['type'] == 'Normal':
                    if ability == 'aerilate':
                        move['type'] = 'Flying'
                    if ability == 'galvanize':
                        move['type'] = 'Electric'
                    if ability == 'pixilate':
                        move['type'] = 'Fairy'
                    if ability == 'refrigerate':
                        move['type'] = 'Ice'
                if move['type'] == 'Steel':
                    if ability == 'steelworker' or ability == 'steelyspirit':
                        move['basePower'] = int(int(move['basePower']) * 1.5)
                if move['type'] == 'Water' and ability == 'waterbubble':
                    move['basePower'] = int(move['basePower']) * 2
                if move['type'] == 'Dark' and ability == 'darkaura':
                    move['basePower'] = int(int(move['basePower']) * 1.33)
                if move['type'] == 'Dragon' and ability == 'dragonsmaw':
                    move['basePower'] = int(int(move['basePower']) * 1.5)
                if move['type'] == 'Electric' and ability == 'transistor':
                    move['basePower'] = int(int(move['basePower']) * 1.5)
                if move['type'] == 'Fairy' and ability == 'fairyaura':
                    move['basePower'] = int(int(move['basePower']) * 1.33)
                if ability == 'technician' and int(move['basePower']) <= 60:
                    move['basePower'] = int(int(move['basePower']) * 1.5)
                if ability == 'sheerforce' and 'secondary' in move:
                    if move['secondary'] is not None:
                        move['basePower'] = int(int(move['basePower']) * 1.3)
                if ability == 'reckless' and 'recoil' in move:
                    if move['recoil'] is not None:
                        move['basePower'] = int(int(move['basePower']) * 1.2)
                if 'flags' in move:
                    if ability == 'toughclaws' and 'contact' in move['flags']:
                        move['basePower'] = int(int(move['basePower']) * 1.3)
                    if ability == 'strongjaw' and 'bite' in move['flags']:
                        move['basePower'] = int(int(move['basePower']) * 1.3)
                    if 'sound' in move['flags']:
                        if ability == 'punkrock':
                            move['basePower'] = int(int(move['basePower']) * 1.3)
                        if ability == 'liquidvoice':
                            move['type'] = 'Water'
                    if ability == 'ironfist' and 'punch' in move['flags']:
                        move['basePower'] = int(int(move['basePower']) * 1.2)
                    if ability == 'megalauncher' and 'pulse' in move['flags']:
                        move['basePower'] = int(int(move['basePower']) * 1.5)

                modified_power = int(move['basePower'])
                base_power_str = str(modified_power)
                if move['type'] in dex_entry['types'] or ability == 'libero' or ability == 'protean':
                    if ability == 'adaptability':
                        modified_power = modified_power * 2
                    else:
                        modified_power = int(modified_power * 1.5)
            else:
                attack_mod = 0
            if not ignore_stats:
                if accuracy_check:
                    if acc == 1:
                        modified_power = modified_power * attack_mod
                    else:
                        modified_power = int(modified_power * attack_mod * (acc / 100))
                else:
                    modified_power = modified_power * attack_mod
            if 'multihit' in move:
                multihit = move['multihit']
                if isinstance(multihit, list):
                    if ability == 'skilllink':
                        times = multihit[1]
                    else:
                        times = statistics.mean(multihit)
                else:
                    times = multihit
                modified_power = int(modified_power * times)
                base_power_str = f'{base_power_str} x{int(times)}'
            elif 'ohko' in move:
                base_power_str = 'OHKO   '
            elif modified_power == 0:
                if move_type == 'Physical' or move_type == 'Special':
                    base_power_str = ' var   '
                else:
                    base_power_str = '   -   '
            else:
                base_power_str = f'{base_power_str}   '
            if acc == 1:
                acc_str = '-'
            else:
                acc_str = f'{acc}'
            move_name = move['name']
            if move['past_only']:
                move_name = f'*{move_name}'
            formatted_moves.append({'name':move_name,
                                    'type':move['type'],
                                    'pow':base_power_str,
                                    'acc':acc_str,
                                    'cat':move_type,
                                    'atk':attack_mod,
                                    'mpow':modified_power,
                                    'method':method,
                                    'level':level,
                                    'o':orderby_value})
        if move_levels is not None and reorder:
            formatted_moves.sort(key=lambda m : m['level'])
        return formatted_moves

    def acc_sort(self, move):
        return move['acc']

    def pow_sort(self, move):
        return move['mpow']

    def print_top_moves(self, top_moves, num_moves, elemental_type, ignore_stats, print_to):
        print(f'  {elemental_type}:', file=print_to)
        for move in top_moves:
            self.print_move(move, ignore_stats, print_to)

    def print_move(self, move, ignore_stats, print_to):
        orderby = f' ({move["o"]}) ' if move['o'] is not None else ''
        if orderby != '':
            orderby = f'{orderby:7s}'
        print(f'    - {move["name"]:28s} {orderby} {move["type"]:>8s} - {move["cat"]:12s} pow: {move["pow"]:>7s} acc: {move["acc"]:>3s}'
            + ('' if ignore_stats else f' (stat: {move["atk"]:3d})')
            + ('' if move['method'] == '' else f' [{move["method"]}]'), file=print_to)

    def find_egg_move_chain(self, pokemon, dex_entry, move, move_name, checked_mons, dex_name_map, print_to):
        pokemon = re.sub(r'\W+', '', pokemon.lower())
        move = re.sub(r'\W+', '', move.lower())

        if dex_entry is None:
            dex_entry = self.pokemongo.get_pokedex_entry(pokemon)
        if dex_entry is None:
            print(f'Error: No pokedex entry found for "{pokemon}, bzzzzrt!"', file=print_to)
            return False

        species = dex_entry['species']

        learnset = self.pokemongo.get_learnset(pokemon)
        if learnset is None:
            print(f'Error: No learnset entry found for {species}, bzzzzrt!', file=print_to)
            return False

        if move in learnset['levelup']:
            print(f'Note: {species} learns {move_name} by leveling up.', file=print_to)
            return False
        if move in learnset['machine']:
            print(f'Note: {species} learns {move_name} by TM/TR.', file=print_to)
            return False
        if move not in learnset['breeding']:
            if move != '[unspecified]':
                print(f'Error: {species} does not have {move_name} as an egg move, bzzzzrt!', file=print_to)
            if len(learnset['breeding']) > 0:
                print(f'Available egg moves for {species}:', file=print_to)
                all_moves = self.pokemongo.get_move_entries(learnset['breeding'], print_to)
                for egg_move in all_moves:
                    print(f'  - {egg_move["name"]}', file=print_to)
            else:
                print(f'No available egg moves for {species}.', file=print_to)
            return False

        egg_groups = dex_entry['eggGroups']
        potential_parents = []
        for egg_group in egg_groups:
            potential_parents = list(set().union(potential_parents, self.pokemongo.get_egg_group(egg_group, print_to, get_name=False)))

        parent_entries = self.pokemongo.get_pokedex_entries(potential_parents)
        for entry in parent_entries:
            dex_name_map[entry['_id']] = entry['species']
        full_parents_list = potential_parents[:]

        evo_family = self.pokemongo.get_full_evo_family(pokemon)
        for evo in evo_family:
            if evo in potential_parents:
                potential_parents.remove(evo)

        for mon in checked_mons:
            if mon in potential_parents:
                potential_parents.remove(mon)

        parent_learnsets = self.pokemongo.get_learnsets(potential_parents)
        parents_with_move = []
        for learnset in parent_learnsets:
            if move in learnset['levelup']:
                parents_with_move.append(learnset['_id'])
            elif move in learnset['machine']:
                parents_with_move.append(learnset['_id'])

        parent_entries = self.pokemongo.get_pokedex_entries(parents_with_move)
        valid_parents = []
        for entry in parent_entries:
            if 'prevo' in entry:
                if entry['prevo'] in parents_with_move:
                    continue
            if 'gender' in entry:
                if entry['gender'] == 'N' or entry['gender'] == 'F':
                    continue
            valid_parents.append(entry['_id'])

        potential_options = []
        if len(valid_parents) == 0:
            breeding_chain_parents = []
            for learnset in parent_learnsets:
                if move in learnset['breeding']:
                    breeding_chain_parents.append(learnset['_id'])
            breeding_chain_parent_entries = self.pokemongo.get_pokedex_entries(breeding_chain_parents)
            for entry in breeding_chain_parent_entries:
                parent = entry['_id']
                if 'prevo' in entry:
                    if entry['prevo'] in breeding_chain_parents:
                        continue
                options = self.find_egg_move_chain(parent, None, move, move_name, full_parents_list, dex_name_map, print_to)
                if len(options) > 0:
                    potential_options.append({'name': parent, 'chain': options})
        else:
            for parent in valid_parents:
                potential_options.append({'name': parent})

        return potential_options

    def print_parent_option(self, parent, tabs, dex_name_map, print_to):
        print(('    ' * tabs) +  f'  - ' + dex_name_map[parent['name']] + (', inheriting from:' if 'chain' in parent else ''), file=print_to)
        if 'chain' in parent:
            for option in parent['chain']:
                self.print_parent_option(option, tabs + 1, dex_name_map, print_to)

    def do_egg_moves_function(self, pokemon, move, print_to):
        if move is None:
            move = '[unspecified]'

        dex_entry = self.pokemongo.get_pokedex_entry(pokemon)
        if dex_entry is None:
            print(f'Error: No pokedex entry found for "{pokemon}", bzzzzrt!"', file=print_to)
            return
        species = dex_entry['species']

        move_entry = self.pokemongo.get_move_entry(move)
        if move_entry is None and move != '[unspecified]':
            print(f'Error: No entry found for "{move}", bzzzzrt!"', file=print_to)
            return
        if move != '[unspecified]':
            move_name = move_entry['name']
        else:
            move_name = '[unspecified]'

        dex_name_map = dict()

        possible_parents = self.find_egg_move_chain(pokemon, dex_entry, move, move_name, [], dex_name_map, print_to)
        if move != '[unspecified]':
            if possible_parents is not False and (possible_parents is None or len(possible_parents) == 0):
                print(f'No possible parents found for {species} with {move_name}. Mirror Herb required.', file=print_to)
            elif possible_parents is not False:
                print(f'Potential parents for {species} with {move_name}:', file=print_to)
                for parent in possible_parents:
                    self.print_parent_option(parent, 0, dex_name_map, print_to)

    def do_moves_query_function(self, filters, print_to, count=False, force_list=False):
        entries = self.pokemongo.get_move_entries_with_filters(print_to, filters)

        if count:
            print(f'Bzzzzrt! The number of entries that match that query is: {len(entries)}', file=print_to)
            return

        if len(entries) > 50 and not force_list:
            print(f'Bzzzzrt! A lot of moves matched your query! {len(entries)} entries, to be exact.', file=print_to)
            print(f'I didn\'t print the list, because it would be very large, but you can use the -f option to print it anyway if you want.', file=print_to)
            print(f'Or maybe you want to filter it further first? It\'s up to you, bzzzzrt!', file=print_to)
            return

        if len(entries) == 0:
            print('There are no moves that match your query, bzzzzrt.', file=print_to)
            return

        orderby = self.pokemongo.get_movedex_orderby_key(filters)
        formatted_moves = self.format_moves(entries, None, ignore_stats=True, orderby_key=orderby)

        past_moves = False
        format_str = f'There are {len(entries)} moves that match'
        if len(entries) == 1:
            format_str = f'There is 1 move that matches'
        print(f'{format_str} your query, bzzzzrt:', file=print_to)
        for move in formatted_moves:
            if move['name'][0] == '*':
                past_moves = True
            self.print_move(move, True, print_to)

        if past_moves:
            print('\n* Move not available in Gen 9 games.', file=print_to)

    def do_random_move_function(self, filters, print_to):
        entries = self.pokemongo.get_move_entries_with_filters(print_to, filters)

        if len(entries) == 0:
            print('There are no moves that match those filters, bzzzzrt!', file=print_to)
            return

        random_entry = entries[0]

        if len(entries) == 1:
            print(f'Oh, it looks like only one move matches those filters, bzzzzrt! This is an easy one.', file=print_to)
            name = f'{random_entry["name"]}'
            print(f'It\'s gotta be {name}, bzzzzrt!', file=print_to)
        else:
            if filters is not None and filters != {}:
                print(f'There are {len(entries)} moves that match those filters, bzzzzrt! Let me see...', file=print_to)
            else:
                print(f'Bzzzzrt, allow me to choose a random move out of all possible entries! Let me see...', file=print_to)
            random_entry = random.choice(entries)
            if random_entry is None:
                print(f'Bzzzzt, oh? Something appears to have gone wrong with my randomizer functions, my apologies!', file=print_to)
                return
            name = f'{random_entry["name"]}'
            random_response = PokemonHelper().get_random_response(name, additional_responses=[
                f'I\'ve been thinking about the move {name} lately, bzzzzrt! How about that one?',
                f'What about {name}, bzzzzrt? I was looking at its entry the other day!',
                f'I think {name} is a pretty interesting move, bzzzzrt! I think they\'re all interesting, though.',
                f'Perhaps {name} is a good move for whatever you\'re looking for, bzzzzrt?'
            ])
            print(random_response, file=print_to)
        print('Let me get you the entry for this move...\n', file=print_to)
        self.do_move_search_function(random_entry['_id'], False, filters, print_to)

    def do_wild_moveset_function(self, pokemon, level, print_to):
        dex_entry = self.pokemongo.get_pokedex_entry(pokemon)
        if dex_entry is None:
            print(f'Error: No dex entry found for "{pokemon}", bzzzzrt!', file=print_to)
            return

        learnset = self.pokemongo.get_learnset(pokemon)
        if learnset is None:
            print(f'Error: No learnset found for "{pokemon}", bzzzzrt!', file=print_to)
            return

        move_levels = learnset['movelevels']
        start_level = int(level)

        levelup_moves = []
        for move in move_levels:
            levelup_moves.append({'id':move, 'lvl':move_levels[move]})
        levelup_moves.sort(key=lambda e : e['lvl'])
        levelup_moves.reverse()

        wild_moves = []
        current_level = start_level
        while current_level > 0:
            for move in levelup_moves:
                if move['lvl'] == current_level:
                    wild_moves.append(move['id'])
            if len(wild_moves) >= 4:
                break
            current_level -= 1

        wild_move_entries = self.pokemongo.get_move_entries(wild_moves, print_to)
        print(f'Probable moves for a wild {dex_entry["species"]} at level {level}, bzzzzrt:', file=print_to)
        for move in self.format_moves(wild_move_entries, dex_entry, move_levels=move_levels, reorder=True):
            self.print_move(move, True, print_to)

        move_warnings = []
        for entry in wild_move_entries:
            if 'self-heal' not in move_warnings:
                if 'flags' in entry and 'heal' in entry['flags']:
                    move_warnings.append('self-heal')
            if 'recoil' not in move_warnings:
                if 'recoil' in entry:
                    move_warnings.append('recoil')
            if 'confuse' not in move_warnings:
                if 'self' in entry and 'volatileStatus' in entry['self'] and entry['self']['volatileStatus'] == 'lockedmove':
                    move_warnings.append('confuse')
            if 'self-destruct' not in move_warnings:
                if 'selfdestruct' in entry:
                    move_warnings.append('self-destruct')
            if 'force-switch' not in move_warnings:
                if 'forceSwitch' in entry:
                    move_warnings.append('force-switch')

        if len(move_warnings) > 0:
            print('', file=print_to)
            if 'self-heal' in move_warnings:
                print(f'* Pokemon has moves that allow it to heal itself. Sleep or paralysis recommended, bzzzzrt!', file=print_to)
            if 'recoil' in move_warnings or 'confuse' in move_warnings or 'self-destruct' in move_warnings:
                print(f'* Pokemon has moves that might cause it to hurt itself!', file=print_to)
            if 'force-switch' in move_warnings:
                print(f'* Pokemon has moves that allow it to flee from battle!', file=print_to)

