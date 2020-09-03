from .pokewrap import PokeMongo8
from pprint import pprint

class AbilityDex:
    def __init__(self):
        self.pokemongo = PokeMongo8()

    def do_ability_search_function(self, ability, show_list, filters, print_to):
        ab = self.pokemongo.get_ability(ability)
        if ab is None:
            print(f'Error: Ability "{ability}" not found, bzzzzrt!', file=print_to)
            return

        if ab['past_only']:
            print('\n[NOTE: This ability is not available in the Gen 8 games, bzzzzrt!]\n', file=print_to)

        desc = 'No description available.'
        if 'shortDesc' in ab:
            desc = ab['shortDesc']
        print(f'Description: {desc}\n', file=print_to)

        if not show_list:
            return

        ab_name = ability
        if 'name' in ab:
            ab_name = ab['name']

        entries = self.pokemongo.get_pokemon_with_ability(ability, full_entry=True, filters=filters)
        hidden_list = []
        nonhidden_list = []
        past_pokemon = False
        for entry in entries:
            if 'H' in entry['abilities'] and entry['abilities']['H'].lower().replace(' ','') == ability:
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
        print(f'All pokemon with {ab_name} as a normal ability:', file=print_to)
        for p_name in nonhidden_list:
            print(f'  - {p_name}', file=print_to)
        print(f'\nAll pokemon with {ab_name} as a hidden ability:', file=print_to)
        for p_name in hidden_list:
            print(f'  - {p_name}', file=print_to)

        if past_pokemon:
            print('\n* Pokemon not available in Gen 8 games.', file=print_to)