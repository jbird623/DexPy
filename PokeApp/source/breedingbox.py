from .pokewrap import PokeMongo9

class BreedingBox:
    def __init__(self, pokemongo):
        self.pokemongo = pokemongo

    def register_ha_mon(self, user, username, pokemon, print_to):
        bb_entry = self.pokemongo.get_or_register_bb(user, username)
        dex_entry = self.pokemongo.get_pokedex_entry(pokemon)
        if dex_entry is None:
            print(f'Error: No dex entry found for "{pokemon}", bzzzzrt!', file=print_to)
            return False
        if pokemon in bb_entry['ha_list']:
            print(f'You have already registered {dex_entry["species"]}, bzzzzrt!', file=print_to)
            return
        bb_entry['ha_list'].append(pokemon)
        registered = self.pokemongo.update_bb_entry(user, bb_entry)
        if registered:
            print(f'Successfully registered HA {dex_entry["species"]}, bzzzzrt!', file=print_to)
        else:
            print(f'Error: There was a problem registering {dex_entry["species"]}, bzzzzrt!', file=print_to)

    def unregister_ha_mon(self, user, username, pokemon, print_to):
        bb_entry = self.pokemongo.get_or_register_bb(user, username)
        dex_entry = self.pokemongo.get_pokedex_entry(pokemon)
        if dex_entry is None:
            print(f'Error: No dex entry found for "{pokemon}", bzzzzrt!', file=print_to)
            return False
        if pokemon not in bb_entry['ha_list']:
            print(f'Error: {dex_entry["species"]} has not been registered, bzzzzrt!', file=print_to)
            return False
        bb_entry['ha_list'].remove(pokemon)
        unregistered = self.pokemongo.update_bb_entry(user, bb_entry)
        if unregistered:
            print(f'Successfully unregistered {dex_entry["species"]}, bzzzzrt!', file=print_to)
        else:
            print(f'Error: There was a problem unregistering {dex_entry["species"]}, bzzzzrt!', file=print_to)

    def query_ha_mon(self, user, pokemon, print_to):
        full_evo_line = self.pokemongo.get_full_evo_family(pokemon)
        if not full_evo_line:
            print(f'Unable to find a pokedex entry for "{pokemon}", bzzzzrt!\n', file=print_to)
            return
        entries = self.pokemongo.get_bb_entries(full_evo_line)
        species_map = self.pokemongo.get_pokemon_species_map(full_evo_line)
        if len(entries) == 0:
            print(f'No one has registered any pokemon in the same evolutionary line as {species_map[pokemon]}, bzzzzrt!\n', file=print_to)
            return
        print(f'The following users have registered a pokemon in the same evolutionary line as {species_map[pokemon]}:', file=print_to)
        user_pokemon_map = dict()
        for entry in entries:
            if entry['name'] not in user_pokemon_map:
                user_pokemon_map[entry['name']] = []
            user_pokemon_map[entry['name']].append(species_map[entry['pokemon']])
        for user in user_pokemon_map:
            list_string = ', '.join(user_pokemon_map[user])
            print(f' - {user} ({list_string})', file=print_to)
        print('', file=print_to)