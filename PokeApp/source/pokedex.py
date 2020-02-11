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
                print(f'No hidden ability found for {species}.', file=print_to)
        else:
            print(f'Error: Unable to retrieve abilities for {species}, bzzzzrt!', file=print_to)

    def do_pokedex_function(self, pokemon, verbose, print_to):
        dex_entry = self.pokemongo.get_pokedex_entry(pokemon)
        if dex_entry is None:
            print(f'Error: No dex entry found for "{pokemon}", bzzzzrt!', file=print_to)
            return

        self.print_pokedex_data(dex_entry, verbose, print_to)

    def print_pokedex_data(self, dex_entry, verbose, print_to):
        species = dex_entry['species']
        types = dex_entry['types']
        stats = dex_entry['baseStats']
        abilities = dex_entry['abilities']
        raw_egg_groups = dex_entry['eggGroups']
        egg_groups = []
        for group in raw_egg_groups:
            egg_groups.append(group.capitalize())

        print(f'Pokedex entry for {species}:\n', file=print_to)

        types_string = '/'.join(types)
        print(f'Type: {types_string}', file=print_to)
        if verbose:
            self.do_types_damage_function(types, print_to, pokedex_format=True)
            print('', file=print_to)

        abilities_list = []
        ability_ids = []
        for key in abilities:
            ability_string = abilities[key]
            ability_ids.append(abilities[key].lower())
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
                    if ab['name'].replace(' ','') == abilities[list(abilities)[i]]:
                        entry = ab
                        break
                ability_name = entry['name']
                if 'H' in abilities:
                    if entry['name'].replace(' ','') == abilities['H']:
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
            print('', file=print_to)
        else:
            print(f'HP: {stats["hp"]} | Atk: {stats["atk"]} | Def: {stats["def"]} | SpA: {stats["spa"]} | SpD: {stats["spd"]} | Spe: {stats["spe"]}', file=print_to)

        if verbose:
            print('Egg Groups:', file=print_to)
            for group in egg_groups:
                print(f'  {group}', file=print_to)
            print('', file=print_to)
        else:
            egg_groups_string = ', '.join(egg_groups)
            print(f'Egg Groups: {egg_groups_string}', file=print_to)

    def get_stat_pipes(self, stat):
        return '|' * int(stat / 10)

    def do_pokemon_damage_function(self, pokemon, print_to):
        dex_entry = self.pokemongo.get_pokedex_entry(pokemon)
        if dex_entry is None:
            print(f'Error: Unable to retrieve pokedex listing for "{pokemon}", bzzzzrt!', file=print_to)
            return
        types = dex_entry['types']
        species = dex_entry['species']
        type_str = '[Undefined]'
        if len(types) == 1:
            type_str = types[0]
        if len(types) == 2:
            type_str = f'{types[0]}/{types[1]}'
        print(f'{species} is {type_str} type.', file=print_to)
        self.do_types_damage_function(types, print_to)

    def do_type_damage_function(self, elemental_type, print_to):
        self.print_types_damage(PokemonHelper().get_damage_modifiers([elemental_type]), print_to)

    def do_types_damage_function(self, types, print_to, pokedex_format=False):
        self.print_types_damage(PokemonHelper().get_damage_modifiers(types), print_to, pokedex_format)

    def print_types_damage(self, damage_dict, print_to, pokedex_format=False):
        double_weak = []
        weak = []
        neutral = []
        resist = []
        double_resist = []
        immune = []

        for t in damage_dict:
            if damage_dict[t] == 4:
                double_weak.append(t)
            elif damage_dict[t] == 2:
                weak.append(t)
            elif damage_dict[t] == 1:
                neutral.append(t)
            elif damage_dict[t] == 0.5:
                resist.append(t)
            elif damage_dict[t] == 0.25:
                double_resist.append(t)
            elif damage_dict[t] == 0:
                immune.append(t)
            else:
                print('Error: Invalid damage modifier!')
        
        heading_prefix = '  ' if pokedex_format else '\n'
        listing_prefix = '    ' if pokedex_format else '  '
        if len(double_weak) > 0:
            print(f'{heading_prefix}4x Weakness to:', file=print_to)
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
            print(f'{heading_prefix}4x Resists:', file=print_to)
            list_str = ', '.join(double_resist)
            print(f'{listing_prefix}{list_str}', file=print_to)
        if len(immune) > 0:
            print(f'{heading_prefix}Immunity to:', file=print_to)
            list_str = ', '.join(immune)
            print(f'{listing_prefix}{list_str}', file=print_to)
    
    def do_egg_group_function(self, group, print_to):
        egg_group_entries = self.pokemongo.get_minimum_egg_group(group)

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