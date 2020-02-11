from .pokewrap import PokeMongo8
from .pokehelper import PokemonHelper
from pprint import pprint

class MoveDex:
    def __init__(self):
        self.pokemongo = PokeMongo8()

    def do_move_search_function(self, move, show_list, filters, print_to, full_desc=False):
        m_entry = self.pokemongo.get_move_entry(move)
        if m_entry is None:
            print(f'Error: Move "{move}" not found, bzzzzrt!', file=print_to)
            return

        category = m_entry['category']
        print(f'Category: {category}', file=print_to)

        power = m_entry['basePower']
        accuracy = m_entry['accuracy'] 
        print(f'Base Power: {power}\nAccuracy: {accuracy}', file=print_to)

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

        levelup_list = self.pokemongo.get_pokemon_with_move_levelup(move, filters=filters)
        machine_list = self.pokemongo.get_pokemon_with_move_machine(move, filters=filters)
        breeding_list = self.pokemongo.get_pokemon_with_move_breeding(move, filters=filters)

        if len(levelup_list) > 0:
            print(f'\nPokemon that learn {move_name} by level up:', file=print_to)
            for pokemon in levelup_list:
                print(f'  - {pokemon["species"]}', file=print_to)
        if len(machine_list) > 0:
            print(f'\nPokemon that learn {move_name} by TM/TR:', file=print_to)
            for pokemon in machine_list:
                print(f'  - {pokemon["species"]}', file=print_to)
        if len(breeding_list) > 0:
            print(f'\nPokemon that learn {move_name} by breeding:', file=print_to)
            for pokemon in breeding_list:
                print(f'  - {pokemon["species"]}', file=print_to)

    def do_moves_function(self, pokemon, filters, show_stab=False, max_stab=5, ignore_stats=False, show_coverage=False, max_coverage=3, print_to=None):
        dex_entry = self.pokemongo.get_pokedex_entry(pokemon)
        if dex_entry is None:
            print(f'Error: No dex entry found for "{pokemon}", bzzzzrt!', file=print_to)
            return

        learnset = self.pokemongo.get_learnset(pokemon)
        if learnset is None:
            print(f'Error: No learnset found for "{pokemon}", bzzzzrt!', file=print_to)
            return

        breeding_entries = self.pokemongo.get_move_entries(learnset['breeding'], filters)
        machine_entries = self.pokemongo.get_move_entries(learnset['machine'], filters)
        levelup_entries = self.pokemongo.get_move_entries(learnset['levelup'], filters)

        all_moves = dict()
        for move in levelup_entries:
            all_moves[move['_id']] = {'method':'levelup', 'move':move}
        for move in machine_entries:
            if move['_id'] not in all_moves:
                all_moves[move['_id']] = {'method':'machine', 'move':move}
        for move in breeding_entries:
            if move['_id'] not in all_moves:
                all_moves[move['_id']] = {'method':'breeding', 'move':move}

        if show_stab:
            self.show_stab_moves(max_stab, ignore_stats, dex_entry, all_moves, print_to)
            return

        if show_coverage:
            self.show_coverage_moves(max_coverage, ignore_stats, dex_entry, all_moves, print_to)
            return
                    
        self.show_all_moves(breeding_entries, machine_entries, levelup_entries, dex_entry, ignore_stats, print_to)

    def show_all_moves(self, breeding_entries, machine_entries, levelup_entries, dex_entry, ignore_stats, print_to):
        print('Level Up Moves:', file=print_to)
        for move in self.format_moves(levelup_entries, dex_entry, ignore_stats):
            self.print_move(move, ignore_stats, print_to)
        print('\nTM/TR Moves:', file=print_to)
        for move in self.format_moves(machine_entries, dex_entry, ignore_stats):
            self.print_move(move, ignore_stats, print_to)
        print('\nEgg Moves:', file=print_to)
        for move in self.format_moves(breeding_entries, dex_entry, ignore_stats):
            self.print_move(move, ignore_stats, print_to)

    def show_stab_moves(self, max_stab, ignore_stats, dex_entry, all_moves, print_to):
        for elemental_type in dex_entry['types']:
            top_moves = self.find_strongest_moves_of_type(all_moves, elemental_type, max_stab, dex_entry, ignore_stats)
            num_moves = min(max_stab, len(top_moves))
            self.print_top_moves(top_moves, num_moves, elemental_type, ignore_stats, print_to)

    def show_coverage_moves(self, max_coverage, ignore_stats, dex_entry, all_moves, print_to):
        for elemental_type in PokemonHelper().get_types():
            if elemental_type in dex_entry['types']:
                continue
            top_moves = self.find_strongest_moves_of_type(all_moves, elemental_type, max_coverage, dex_entry, ignore_stats)
            if len(top_moves) == 0:
                continue
            num_moves = min(max_coverage, len(top_moves))
            self.print_top_moves(top_moves, num_moves, elemental_type, ignore_stats, print_to)

    def find_strongest_moves_of_type(self, moves, elemental_type, num, dex_entry, ignore_stats):
        type_moves = self.filter_moves_by_type(moves, elemental_type, dex_entry, ignore_stats)
        type_moves.sort(key=self.acc_sort, reverse=True)
        type_moves.sort(key=self.pow_sort, reverse=True)
        return type_moves[:num]

    def filter_moves_by_type(self, moves, elemental_type, dex_entry, ignore_stats):
        type_moves = []
        for move in moves:
            if moves[move]['move']['type'] == elemental_type:
                if moves[move]['move']['category'] == 'Status':
                    continue
                type_moves.append(moves[move]['move'])
        return self.format_moves(type_moves, dex_entry, ignore_stats)

    def format_moves(self, moves, dex_entry, ignore_stats):
        formatted_moves = []
        for move in moves:
            modified_power = int(move['basePower'])
            move_type = move['category']
            if dex_entry:
                if move_type == 'Special':
                    attack_mod = int(dex_entry['baseStats']['spa'])
                elif move_type == 'Physical':
                    attack_mod = int(dex_entry['baseStats']['atk'])
                else:
                    attack_mod = 0
            else:
                attack_mod = 0
            if not ignore_stats:
                modified_power = modified_power * attack_mod
            formatted_moves.append({'name':move['name'],
                                    'pow':move['basePower'],
                                    'acc':move['accuracy'],
                                    'cat':move_type,
                                    'atk':attack_mod,
                                    'mpow':modified_power})
        return formatted_moves

    def acc_sort(self, move):
        return move['acc']

    def pow_sort(self, move):
        return move['mpow']

    def print_top_moves(self, top_moves, num_moves, elemental_type, ignore_stats, print_to):
        print(f'\n{elemental_type}:', file=print_to)
        for move in top_moves:
            self.print_move(move, ignore_stats, print_to)

    def print_move(self, move, ignore_stats, print_to):
        print(f'  - {move["name"]:20s} category: {move["cat"]:12s} pow: {move["pow"]:3d}    acc: {move["acc"]:3d}'
            + ('' if ignore_stats else f'    ( mod: {move["mpow"]:5d}  stat: {move["atk"]:3d} )'), file=print_to)

    def find_egg_move_chain(self, pokemon, dex_entry, move, move_name, checked_mons, dex_name_map, print_to):
        pokemon = pokemon.lower().replace(' ','')
        move = move.lower().replace(' ','')

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
                all_moves = self.pokemongo.get_move_entries(learnset['breeding'])
                for egg_move in all_moves:
                    print(f'  - {egg_move["name"]}', file=print_to)
            else:
                print(f'No available egg moves for {species}.', file=print_to)
            return False

        egg_groups = dex_entry['eggGroups']
        potential_parents = []
        for egg_group in egg_groups:
            potential_parents = list(set().union(potential_parents, self.pokemongo.get_egg_group(egg_group)))

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
                print(f'No possible parents found for {species} with {move_name}.', file=print_to)
            elif possible_parents is not False:
                print(f'Potential parents for {species} with {move_name}:', file=print_to)
                for parent in possible_parents:
                    self.print_parent_option(parent, 0, dex_name_map, print_to)

    def do_moves_query_function(self, filters, print_to):
        entries = self.pokemongo.get_move_entries_with_filters(filters)

        if len(entries) == 0:
            print('There are no moves that match your query, bzzzzrt.', file=print_to)
            return

        formatted_moves = self.format_moves(entries, None, True)

        print('Here are the moves that match your query, bzzzzrt:', file=print_to)
        for move in formatted_moves:
            self.print_move(move, True, print_to)