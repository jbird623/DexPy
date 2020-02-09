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

    def do_pokedex_function(self, pokemon, print_to):
        dex_entry = self.pokemongo.get_pokedex_entry(pokemon)
        if dex_entry is None:
            print(f'Error: No dex entry found for "{pokemon}", bzzzzrt!', file=print_to)
            return

        pprint(dex_entry, stream=print_to)

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

    def do_types_damage_function(self, types, print_to):
        self.print_types_damage(PokemonHelper().get_damage_modifiers(types), print_to)

    def print_types_damage(self, damage_dict, print_to):
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
        
        if len(double_weak) > 0:
            print('\n4x Weakness to:', file=print_to)
            print(*double_weak, sep=', ', file=print_to)
        if len(weak) > 0:
            print('\nWeakness to:', file=print_to)
            print(*weak, sep=', ', file=print_to)
        if len(neutral) > 0:
            print('\nNormal damage from:', file=print_to)
            print(*neutral, sep=', ', file=print_to)
        if len(resist) > 0:
            print('\nResists:', file=print_to)
            print(*resist, sep=', ', file=print_to)
        if len(double_resist) > 0:
            print('\n4x Resists:', file=print_to)
            print(*double_resist, sep=', ', file=print_to)
        if len(immune) > 0:
            print('\nImmunity to:', file=print_to)
            print(*immune, sep=', ', file=print_to)
