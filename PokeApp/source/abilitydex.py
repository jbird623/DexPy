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
        for entry in entries:
            if 'H' in entry['abilities'] and entry['abilities']['H'].lower() == ability:
                hidden_list.append(entry['species'])
            else:
                nonhidden_list.append(entry['species'])
        print(f'All pokemon with {ab_name} as a normal ability:', file=print_to)
        for p_name in nonhidden_list:
            print(f'  - {p_name}', file=print_to)
        print(f'\nAll pokemon with {ab_name} as a hidden ability:', file=print_to)
        for p_name in hidden_list:
            print(f'  - {p_name}', file=print_to)