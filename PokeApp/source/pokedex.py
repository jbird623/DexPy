import math
import random

from .pokewrap import PokeMongo8
from .pokehelper import PokemonHelper
from pprint import pprint

class PokeDex:
    def __init__(self):
        self.pokemongo = PokeMongo8()

    def do_hidden_ability_function(self, pokemon, print_to):
        dex_entry = self.pokemongo.get_pokedex_entry(pokemon)
        if dex_entry is None:
            print(f'Error: No dex entry found for "{pokemon}", bzzzzrt!', file=print_to)
            return

        species = dex_entry['species']

        if 'abilities' in dex_entry:
            if 'H' in dex_entry['abilities']:
                print(f'The hidden ability for {species} is ' + dex_entry['abilities']['H'] + '.', file=print_to)
            else:
                print(f'{species} does not have a hidden ability.', file=print_to)
        else:
            print(f'Error: Unable to retrieve abilities for {species}, bzzzzrt!', file=print_to)

    def do_pokedex_function(self, pokemon, verbose, print_to):
        dex_entry = self.pokemongo.get_pokedex_entry(pokemon)
        if dex_entry is None:
            print(f'Error: No dex entry found for "{pokemon}", bzzzzrt!', file=print_to)
            return

        self.print_pokedex_data(dex_entry, verbose, print_to)

    def get_hp_range(self, value):
        if value == 1:
            return '  1-  1'
        min = math.floor(2 * value) + 110
        max = math.floor(2 * value + 94) + 110
        return f'{min:3d}-{max:3d}'

    def get_stat_range(self, value, nature):
        min = math.floor((math.floor(2 * value) + 5) * (1 + 0.1 * nature))
        max = math.floor((math.floor(2 * value + 94) + 5) * (1 + 0.1 * nature))
        return f'{min:3d}-{max:3d}'

    def format_stat_ranges(self, HP, Atk, Def, SpA, SpD, Spe, nature):
        stat_ranges = ''
        stat_ranges += f' {self.get_hp_range(HP)} '
        stat_ranges += f' {self.get_stat_range(Atk, nature)} '
        stat_ranges += f' {self.get_stat_range(Def, nature)} '
        stat_ranges += f' {self.get_stat_range(SpA, nature)} '
        stat_ranges += f' {self.get_stat_range(SpD, nature)} '
        stat_ranges += f' {self.get_stat_range(Spe, nature)} '
        return stat_ranges

    def print_pokedex_data(self, dex_entry, verbose, print_to):
        p_id = dex_entry['_id']
        species = dex_entry['species']
        types = dex_entry['types']
        stats = dex_entry['baseStats']
        abilities = dex_entry['abilities']
        ability_list = dex_entry['ability_list']
        raw_egg_groups = dex_entry['eggGroups']
        egg_groups = []
        for group in raw_egg_groups:
            egg_groups.append(group.capitalize())

        if dex_entry['past_only']:
            print('[NOTE: Bzzzzrt! This Pokemon is not transferrable to Gen 8 games!]\n', file=print_to)

        print(f'{"Full" if verbose else "Abbreviated"} Pokedex entry for {species}, bzzzzrt:\n', file=print_to)

        types_string = '/'.join(types)
        print(f'Type: {types_string}', file=print_to)
        if verbose:
            self.do_types_damage_function(types, print_to, True, ability_list)
            print('', file=print_to)

        abilities_list = []
        ability_ids = []
        for key in abilities:
            ability_string = abilities[key]
            ability_ids.append(abilities[key].lower().replace(' ',''))
            if key == 'H':
                ability_string += ' (hidden)'
            abilities_list.append(ability_string)
        abilities_string = ', '.join(abilities_list)
        if verbose:
            print('Abilities:', file=print_to)
            ab_entries = self.pokemongo.get_abilities(ability_ids)
            for i in range(len(list(abilities))):
                entry = None
                for ab in ab_entries:
                    if ab['name'] == abilities[list(abilities)[i]]:
                        entry = ab
                        break
                ability_name = entry['name']
                if 'H' in abilities:
                    if entry['name'] == abilities['H']:
                        ability_name += ' (hidden)'
                print(f'  {ability_name}: {entry["shortDesc"]}', file=print_to)
            print('', file=print_to)
        else:
            print(f'Abilities: {abilities_string}', file=print_to)

        if verbose:
            print(f'Base Stats:', file=print_to)
            print(f'       HP: {stats["hp"]:3d} {self.get_stat_pipes(stats["hp"])}', file=print_to)
            print(f'   Attack: {stats["atk"]:3d} {self.get_stat_pipes(stats["atk"])}', file=print_to)
            print(f'  Defense: {stats["def"]:3d} {self.get_stat_pipes(stats["def"])}', file=print_to)
            print(f'  Sp. Atk: {stats["spa"]:3d} {self.get_stat_pipes(stats["spa"])}', file=print_to)
            print(f'  Sp. Def: {stats["spd"]:3d} {self.get_stat_pipes(stats["spd"])}', file=print_to)
            print(f'    Speed: {stats["spe"]:3d} {self.get_stat_pipes(stats["spe"])}', file=print_to)
            print(f'--- Total: {stats["bst"]:3d} ------------------------', file=print_to)
            print(f'  Average: {int(stats["bst"]/6):3d} {self.get_stat_pipes(int(stats["bst"]/6))}', file=print_to)
            print('', file=print_to)
            print(f'Stat Ranges (Level 100):', file=print_to)
            print(f'   Nature     HP       Atk      Def      SpA      SpD      Spe', file=print_to)
            print(f' Hindering:{self.format_stat_ranges(stats["hp"], stats["atk"], stats["def"], stats["spa"], stats["spd"], stats["spe"], -1)}', file=print_to)
            print(f'   Neutral:{self.format_stat_ranges(stats["hp"], stats["atk"], stats["def"], stats["spa"], stats["spd"], stats["spe"], 0)}', file=print_to)
            print(f'Beneficial:{self.format_stat_ranges(stats["hp"], stats["atk"], stats["def"], stats["spa"], stats["spd"], stats["spe"], 1)}', file=print_to)
            print('', file=print_to)
        else:
            print(f'HP: {stats["hp"]} | Atk: {stats["atk"]} | Def: {stats["def"]} | SpA: {stats["spa"]} | SpD: {stats["spd"]} | Spe: {stats["spe"]} | BST: {stats["bst"]}', file=print_to)

        if verbose:
            print('Other Stats:', file=print_to)
            print(f'  Height: {dex_entry["heightm"]}m', file=print_to)
            print(f'  Weight: {dex_entry["weightkg"]}kg', file=print_to)
            print(f'  Color: {dex_entry["color"]}', file=print_to)
            availability = 'not transferrable'
            if dex_entry['base_game']:
                availability = 'obtainable in base game'
            elif dex_entry['transfer_only']:
                availability = 'only obtainable via transfer'
            elif dex_entry['isle_of_armor']:
                availability = 'added in Isle of Armor DLC'
            elif dex_entry['crown_tundra']:
                availability = 'added in Crown Tundra DLC'
            print(f'  Availability: {availability}', file=print_to)
            print('', file=print_to)
            print('Egg Groups:', file=print_to)
            for group in egg_groups:
                print(f'  {group}', file=print_to)
            print('', file=print_to)
        else:
            egg_groups_string = ', '.join(egg_groups)
            print(f'Egg Groups: {egg_groups_string}', file=print_to)

        if verbose:
            print('Evolution:', file=print_to)
            evo_options = self.pokemongo.get_evo_options(p_id, full_entry=True)
            longest_name = 1
            for opt in evo_options:
                if opt['_id'] == p_id:
                    continue
                if len(opt['species']) > longest_name:
                    longest_name = len(opt['species'])
            if len(evo_options) > 1:
                print('  Evolves Into:', file=print_to)
            for opt in evo_options:
                if opt['_id'] == p_id:
                    continue
                evo_type_str = ''
                if 'evoType' in opt:
                    if opt['evoType'] == 'trade':
                        evo_type_str = 'trade'
                    elif opt['evoType'] == 'levelFriendship':
                        evo_type_str = 'level up with friendship'
                    elif opt['evoType'] == 'levelExtra':
                        evo_type_str = 'level up'
                    elif opt['evoType'] == 'levelHold':
                        evo_type_str = 'level up while holding'
                evo_gender_str = ''
                if 'gender' in opt:
                    if opt['gender'] == 'M':
                        evo_gender_str = ' (male only)'
                    if opt['gender'] == 'F':
                        evo_gender_str = ' (female only)'
                if 'evoCondition' in opt:
                    if evo_type_str == '':
                        print(f'    {opt["species"]:{longest_name}s}   [{opt["evoCondition"]}{evo_gender_str}]', file=print_to)
                    else:
                        print(f'    {opt["species"]:{longest_name}s}   [{evo_type_str} {opt["evoCondition"]}{evo_gender_str}]', file=print_to)
                elif 'evoLevel' in opt:
                    print(f'    {opt["species"]:{longest_name}s}   [level {opt["evoLevel"]}{evo_gender_str}]', file=print_to)
                elif 'evoMove' in opt:
                    print(f'    {opt["species"]:{longest_name}s}   [level up while knowing {opt["evoMove"]}{evo_gender_str}]', file=print_to)
                elif 'evoItem' in opt:
                    if evo_type_str == 'trade':
                        print(f'    {opt["species"]:{longest_name}s}   [trade while holding {opt["evoItem"]}{evo_gender_str}]', file=print_to)
                    elif evo_type_str == 'level up while holding':
                        print(f'    {opt["species"]:{longest_name}s}   [level up while holding {opt["evoItem"]}{evo_gender_str}]', file=print_to)
                    else:
                        print(f'    {opt["species"]:{longest_name}s}   [use {opt["evoItem"]}{evo_gender_str}]', file=print_to)
                else:
                    print(f'    {opt["species"]:{longest_name}s}   [{evo_type_str}{evo_gender_str}]', file=print_to)
            print('  Tree:', file=print_to)
            evo_line = self.pokemongo.get_evo_line(p_id, full_entry=True)
            child = None
            for evo in evo_line:
                if 'prevo' not in evo:
                    child = evo
                    break
            if child is None:
                print('ERROR: Unable to find child of evolutionary line.')
                return
            evo_family = self.pokemongo.get_full_evo_family(child['_id'], full_entry=True)
            if child['_id'] == p_id:
                child['species'] = f'*{child["species"]}*'
            stages = []
            current_stage = [child]
            while len(current_stage) > 0:
                next_stage = []
                for evo in current_stage:
                    if 'evos' not in evo:
                        continue
                    for name in evo['evos']:
                        for entry in evo_family:
                            if entry['_id'] == p_id and entry['species'][0] != '*':
                                entry['species'] = f'*{entry["species"]}*'
                            if entry['_id'] == name:
                                next_stage.append(entry)
                stages.append(current_stage[:])
                current_stage = next_stage[:]
            max_evos = 1
            max_name_lens = []
            for stage in stages:
                max_name_lens.append(1)
                i = len(max_name_lens) - 1
                if len(stage) > max_evos:
                    max_evos = len(stage)
                for evo in stage:
                    if len(evo['species']) > max_name_lens[i]:
                        max_name_lens[i] = len(evo['species'])
            lines = []
            for i in range(max_evos):
                line = ''
                for j in range(len(stages)):
                    if len(stages[j]) > i:
                        if line != '':
                            line += ' ---> '
                        line += f'{stages[j][i]["species"]:{max_name_lens[j]}s}'
                    else:
                        if line != '':
                            line += '      '
                        line += (' ' * max_name_lens[j])
                lines.append(line)
            for line in lines:
                print(f'    {line}', file=print_to)
        else:
            print(f'Quick Assessment: {PokemonHelper().get_stat_evaluation(stats)}', file=print_to)

    def get_stat_pipes(self, stat):
        return '|' * max(int(stat / 10), 1)

    def do_pokemon_damage_function(self, pokemon, print_to, abilities=None):
        dex_entry = self.pokemongo.get_pokedex_entry(pokemon)
        if dex_entry is None:
            print(f'Error: Unable to retrieve pokedex listing for "{pokemon}", bzzzzrt!', file=print_to)
            return
        types = dex_entry['types']
        species = dex_entry['species']
        override_ability = False
        ability_list = []
        if abilities is None:
            abilities = dex_entry['ability_list']
        else:
            override_ability = True
            ability_list = dex_entry['ability_list']
        type_str = '[Undefined]'
        if len(types) == 1:
            type_str = types[0]
        if len(types) == 2:
            type_str = f'{types[0]}/{types[1]}'
        print(f'{species} is {type_str} type.', file=print_to)
        self.do_types_damage_function(types, print_to, False, abilities)
        defensive_abilities = PokemonHelper().get_defensive_ability_dict()
        type_effectiveness_abilities = PokemonHelper().get_type_effectiveness_ability_dict()
        verb_str = 'might have'
        if len(abilities) == 1:
            verb_str = 'always has'
        defensive_ability = False
        for ability in abilities:
            if ability in defensive_abilities:
                if not defensive_ability:
                    print('', file=print_to)
                    defensive_ability = True
                if not override_ability:
                    print(f'* It {verb_str} the {defensive_abilities[ability]} ability.', file=print_to)
                elif ability in type_effectiveness_abilities:
                    print(f'* Calculated with the {type_effectiveness_abilities[ability]} ability.', file=print_to)
                    if ability not in ability_list:
                        print(f'* This pokemon cannot naturally have this ability.', file=print_to)

    def do_type_damage_function(self, elemental_type, print_to, abilities=None):
        self.do_types_damage_function([elemental_type], print_to, False, abilities)

    def do_types_damage_function(self, types, print_to, pokedex_format=False, abilities=None):
        self.print_types_damage(PokemonHelper().get_damage_modifiers(types, abilities), print_to, pokedex_format, abilities)

    def do_coverage_calculator_function(self, check_types, filters, print_to):
        pHelp = PokemonHelper()
        all_types = pHelp.get_types()
        for t in check_types:
            if t not in all_types:
                print(f'Error: Invalid type "{t}", bzzzzrt!', file=print_to)
                return
        pokedex_entries = PokeMongo8().get_all_pokemon_type_info(filters)
        super_effective = []
        effective = []
        resistant = []
        immune = []
        for entry in pokedex_entries:
            types = entry['types']
            abilities = entry['ability_list']
            damage_dict = pHelp.get_damage_modifiers(types, abilities)
            super_effective_hit = False
            for t in check_types:
                if damage_dict[t] > 1:
                    super_effective_hit = True
                    break
            if super_effective_hit:
                super_effective.append(entry)
                continue
            effective_hit = False
            for t in check_types:
                if damage_dict[t] == 1:
                    effective_hit = True
                    break
            if effective_hit:
                effective.append(entry)
                continue
            resistant_hit = False
            for t in check_types:
                if damage_dict[t] < 1 and damage_dict[t] > 0:
                    resistant_hit = True
                    break
            if resistant_hit:
                resistant.append(entry)
                continue
            immune_hit = False
            for t in check_types:
                if damage_dict[t] == 0:
                    immune_hit = True
                    break
            if immune_hit:
                immune.append(entry)
                continue
            print(f'This message should never be printed. Pokedex Entry: {entry}')
        self.print_type_coverage_results(super_effective, effective, resistant, immune, print_to)
        
    def print_type_coverage_results(self, super_effective, effective, resistant, immune, print_to):
        print('Here are the results for the types you specified, bzzzzrt:\n', file=print_to)

        print(f'Super Effective against {len(super_effective)} Pokemon.', file=print_to)
        print(f'Effective against {len(effective)} Pokemon.', file=print_to)
        print(f'Not Very Effective against {len(resistant)} Pokemon.', file=print_to)
        print(f'No Effect against {len(immune)} Pokemon.', file=print_to)

        if len(immune) > 0:
            immune_sorted = sorted(immune, key = lambda p: p['baseStats']['bst'])
            immune_sorted.reverse()
            print('\nNotable Pokemon with Immunity:', file=print_to)
            for i in range(min(len(immune_sorted), 5)):
                print(f'  - {immune_sorted[i]["species"]}', file=print_to)

        if len(resistant) > 0:
            resistant_sorted = sorted(resistant, key = lambda p: p['baseStats']['bst'])
            resistant_sorted.reverse()
            print('\nNotable Pokemon with Resistance:', file=print_to)
            for i in range(min(len(resistant_sorted), 5)):
                print(f'  - {resistant_sorted[i]["species"]}', file=print_to)
        

    def print_types_damage(self, damage_dict, print_to, pokedex_format=False, abilities=None):
        if abilities is None or len(abilities) > 1:
            abilities = []
        
        double_weak = []
        weak = []
        neutral = []
        resist = []
        double_resist = []
        immune = []

        for t in damage_dict:
            if damage_dict[t] >= 4:
                double_weak.append(t)
            elif damage_dict[t] == 2:
                weak.append(t)
            elif damage_dict[t] == 1:
                neutral.append(t)
            elif damage_dict[t] == 0.5:
                resist.append(t)
            elif damage_dict[t] <= 0.25 and damage_dict[t] > 0:
                double_resist.append(t)
            elif damage_dict[t] == 0:
                immune.append(t)
            else:
                print('Error: Invalid damage modifier!')
        
        heading_prefix = '  ' if pokedex_format else '\n'
        listing_prefix = '    ' if pokedex_format else '  '
        if len(double_weak) > 0:
            print(f'{heading_prefix}Great Weakness to:', file=print_to)
            list_str = ', '.join(double_weak)
            print(f'{listing_prefix}{list_str}', file=print_to)
        if len(weak) > 0:
            print(f'{heading_prefix}Weakness to:', file=print_to)
            list_str = ', '.join(weak)
            print(f'{listing_prefix}{list_str}', file=print_to)
        if len(neutral) > 0:
            print(f'{heading_prefix}Normal damage from:', file=print_to)
            list_str = ', '.join(neutral)
            print(f'{listing_prefix}{list_str}', file=print_to)
        if len(resist) > 0:
            print(f'{heading_prefix}Resists:', file=print_to)
            list_str = ', '.join(resist)
            print(f'{listing_prefix}{list_str}', file=print_to)
        if len(double_resist) > 0:
            print(f'{heading_prefix}Greatly Resists:', file=print_to)
            list_str = ', '.join(double_resist)
            print(f'{listing_prefix}{list_str}', file=print_to)
        if len(immune) > 0:
            print(f'{heading_prefix}Immunity to:', file=print_to)
            list_str = ', '.join(immune)
            print(f'{listing_prefix}{list_str}', file=print_to)

        if len(abilities) == 1:
            type_effectiveness_abilities = PokemonHelper().get_type_effectiveness_ability_dict()
            if abilities[0] in type_effectiveness_abilities:
                print(f'\n* Calculated with the {type_effectiveness_abilities[abilities[0]]} ability.', file=print_to)
    
    def do_egg_group_function(self, group, filters, print_to):
        egg_group_entries = self.pokemongo.get_minimum_egg_group(group, filters)

        one_group_list = []
        two_group_list = []
        for entry in egg_group_entries:
            species_string = entry['species']
            if 'gender' in entry:
                if entry['gender'] == 'N':
                    species_string += ' (genderless)'
                if entry['gender'] == 'F':
                    species_string += ' (female only)'
            if len(entry['eggGroups']) == 2:
                alt_group = entry['eggGroups'][0] if entry['eggGroups'][1] == group else entry['eggGroups'][1]
                two_group_list.append({'pokemon':species_string, 'alt_group':alt_group})
            if len(entry['eggGroups']) == 1:
                one_group_list.append({'pokemon':species_string})

        print(f'These Pokemon are just in the {group.capitalize()} egg group:', file=print_to)
        for elem in one_group_list:
            print(f'  - {elem["pokemon"]}', file=print_to)

        print(f'\nThese Pokemon are in both the {group.capitalize()} egg group and another egg group:', file=print_to)
        for elem in two_group_list:
            print(f'  - {elem["pokemon"]:25s} [{elem["alt_group"].capitalize()}]', file=print_to)

    def do_pokedex_query_function(self, filters, print_to, count=False, force_list=False):
        dex_entries = self.pokemongo.get_pokedex_entries_with_filters(full_entry=True, filters=filters)

        if count:
            print(f'Bzzzzrt! The number of entries that match that query are: {len(dex_entries)}', file=print_to)
            return

        if len(dex_entries) > 50 and not force_list:
            print(f'Bzzzzrt! A lot of pokemon matched your query! {len(dex_entries)} entries, to be exact.', file=print_to)
            print(f'I didn\'t print the list, because it would be very large, but you can use the -f option to print it anyway if you want.', file=print_to)
            print(f'Or maybe you want to filter it further first? It\'s up to you, bzzzzrt!', file=print_to)
            return

        if len(dex_entries) == 0:
            print('There are no pokemon that match your query, bzzzzrt.', file=print_to)
            return

        print(f'There are {len(dex_entries)} pokemon that match your query, bzzzzrt:', file=print_to)
        orderby_key = self.pokemongo.get_pokedex_orderby_key(filters)
        past_pokemon = False
        for entry in dex_entries:
            species = entry['species']
            if entry['past_only']:
                species = f'*{species}'
                past_pokemon = True
            if orderby_key is not None:
                orderby_value = entry
                orderby_keys = orderby_key.split('.')
                for key in orderby_keys:
                    try:
                        orderby_value = orderby_value[key]
                    except:
                        orderby_value = 'N/A'
                species = f'{species:21s} ({orderby_value})'
            print(f'  - {species}', file=print_to)

        if past_pokemon:
            print('\n* Pokemon not available in Gen 8 games.', file=print_to)
    
    def do_random_pokemon_function(self, filters, print_to):
        dex_entries = self.pokemongo.get_pokedex_entries_with_filters(full_entry=True, filters=filters)

        if len(dex_entries) == 0:
            print('There are no pokemon that match those filters, bzzzzrt!', file=print_to)
            return

        random_entry = dex_entries[0]

        if len(dex_entries) == 1:
            print(f'Oh, it looks like only one pokemon matches those filters, bzzzzrt! This is an easy one.', file=print_to)
            species = f'{random_entry["species"]}'
            if 'rotom' in species.lower():
                if species.lower() == 'rotom':
                    print(f'It\'s gotta be {species}, bzzzzrt! Oh hey, that\'s me! Thank you so much, bzzzzt!', file=print_to)
                else:
                    print(f'It\'s gotta be {species}, bzzzzrt! Oh, they\'re a good friend of mine, bzzzzt!', file=print_to)
            else:
                print(f'It\'s gotta be {species}, bzzzzrt!', file=print_to)
        else:
            if filters is not None and filters != {}:
                print(f'There are {len(dex_entries)} pokemon that match those filters, bzzzzrt! Let me see...', file=print_to)
            else:
                print(f'Bzzzzrt, allow me to choose a random pokemon out of all possible entries! Let me see...', file=print_to)
            random_entry = random.choice(dex_entries)
            if random_entry is None:
                print(f'Bzzzzt, oh? Something appears to have gone wrong with my randomizer functions, my apologies!', file=print_to)
                return
            species = f'{random_entry["species"]}'
            random_response = PokemonHelper().get_random_response(species, additional_responses=[
                f'I\'ve been thinking about {species} lately, bzzzzrt! How about that one?',
                f'What about {species}, bzzzzrt? I was looking at its dex entry the other day!',
                f'I think {species} is a pretty interesting pokemon, bzzzzrt! I like all pokemon, though.',
                f'Perhaps {species} is a good pokemon for whatever you\'re looking for, bzzzzrt?'
            ])
            if 'rotom' in species.lower():
                random_response = f'Oh, what about {species}? (I promise this was selected randomly and is not at all biased, bzzzzrt!)'
            print(random_response, file=print_to)
        print('Let me get you the dex entry...\n', file=print_to)
        self.print_pokedex_data(random_entry, False, print_to)