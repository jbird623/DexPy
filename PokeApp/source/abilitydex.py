from .pokewrap import PokeMongo9
from .pokehelper import PokemonHelper
from pprint import pprint

import random
import re

class AbilityDex:
    def __init__(self, pokemongo):
        self.pokemongo = pokemongo

    def do_ability_search_function(self, ability, show_list, filters, print_to):
        ab = self.pokemongo.get_ability(ability)
        if ab is None:
            print(f'Error: Ability "{ability}" not found, bzzzzrt!', file=print_to)
            return

        if ab['past_only']:
            print('\n[NOTE: This ability is not available in the Gen 9 games, bzzzzrt!]\n', file=print_to)

        desc = 'No description available.'
        if 'shortDesc' in ab:
            desc = ab['shortDesc']
        print(f'Description: {desc}\n', file=print_to)

        if not show_list:
            return

        ab_name = ability
        if 'name' in ab:
            ab_name = ab['name']

        entries = self.pokemongo.get_pokemon_with_ability(ability, print_to, full_entry=True, filters=filters)
        hidden_list = []
        nonhidden_list = []
        past_pokemon = False
        for entry in entries:
            if 'H' in entry['abilities'] and re.sub(r'\W+', '', entry['abilities']['H'].lower()) == ability:
                species = entry['species']
                if entry['past_only']:
                    species = f'*{species}'
                    past_pokemon = True
                hidden_list.append(species)
            else:
                species = entry['species']
                if entry['past_only']:
                    species = f'*{species}'
                    past_pokemon = True
                nonhidden_list.append(species)
        if len(filters) > 0 and len(hidden_list) == 0 and len(nonhidden_list) == 0:
            print(f'No pokemon that fit the specified filters can have {ab_name} as an ability, bzzzzrt!', file=print_to)
            return
        print(f'All pokemon with {ab_name} as a normal ability:', file=print_to)
        for p_name in nonhidden_list:
            print(f'  - {p_name}', file=print_to)
        print(f'\nAll pokemon with {ab_name} as a hidden ability:', file=print_to)
        for p_name in hidden_list:
            print(f'  - {p_name}', file=print_to)

        if past_pokemon:
            print('\n* Pokemon not available in Gen 9 games.', file=print_to)

    def do_random_ability_function(self, print_to):
        # TODO: Maybe filter support here?
        entries = self.pokemongo.get_all_abilities()
        filters = {}

        if len(entries) == 0:
            print('There are no abilities that match those filters, bzzzzrt!', file=print_to)
            return

        random_entry = entries[0]

        if len(entries) == 1:
            print(f'Oh, it looks like only one ability matches those filters, bzzzzrt! This is an easy one.', file=print_to)
            name = f'{random_entry["name"]}'
            print(f'It\'s gotta be {name}, bzzzzrt!', file=print_to)
        else:
            if filters is not None and filters != {}:
                print(f'There are {len(entries)} abilities that match those filters, bzzzzrt! Let me see...', file=print_to)
            else:
                print(f'Bzzzzrt, allow me to choose a random ability out of all possible entries! Let me see...', file=print_to)
            random_entry = random.choice(entries)
            if random_entry is None:
                print(f'Bzzzzt, oh? Something appears to have gone wrong with my randomizer functions, my apologies!', file=print_to)
                return
            name = f'{random_entry["name"]}'
            random_response = PokemonHelper().get_random_response(name, additional_responses=[
                f'I\'ve been thinking about the ability {name} lately, bzzzzrt! How about that one?',
                f'I think {name} is a pretty interesting ability, bzzzzrt! I think they\'re all interesting, though.',
                f'Perhaps {name} is a good ability for whatever you\'re looking for, bzzzzrt?'
            ])
            print(random_response, file=print_to)
        print('Let me get you the description for this ability, bzzzzrt:\n', file=print_to)
        self.do_ability_search_function(random_entry['_id'], False, filters, print_to)