"""
Usage: dexpy_cli.py moves (POKEMON) [--stab|-s=NUM_MOVES] [--ignore-stats]
       dexpy_cli.py moves (POKEMON) [--coverage|-c=NUM_MOVES] [--ignore-stats]
       dexpy_cli.py eggmove (POKEMON) [MOVE]
       dexpy_cli.py pokedex (POKEMON)
       dexpy_cli.py ha (POKEMON)
       dexpy_cli.py ability (ABILITY)

Arguments:
  POKEMON       The pokemon to check the moves for.
  MOVE          The move to check for.
  ABILITY       The ability to check for.

Options:        
  --stab            Get the top 5 moves with STAB for each type.
  -s=NUM_MOVES      Get the top NUM_MOVES moves with STAB for each type.
  --ignore-stats    Ignore stats when calculating move damage.
  -c=NUM_MOVES      Get the top NUM_MOVES coverage moves per type available.
  --coverage        Get the top coverage move per type available.
"""
import sys

from docopt import docopt
from source.abilitydex import AbilityDex
from source.movedex import MoveDex
from source.pokedex import PokeDex

def main():
    arguments = docopt(__doc__)
    if arguments['moves']:
        moves_func(arguments)
    if arguments['eggmove']:
        eggmove_func(arguments)
    if arguments['pokedex']:
        pokedex_func(arguments)
    if arguments['ha']:
        ha_func(arguments)
    if arguments['ability']:
        ability_func(arguments)

def eggmove_func(arguments):
    print('')
    pokemon = arguments['POKEMON']
    move = arguments['MOVE']

    MoveDex().do_egg_moves_function(pokemon, move, sys.stdout)
    print('')

def moves_func(arguments):
    print('')
    pokemon = arguments['POKEMON'].lower().replace(' ','')

    show_stab = False
    max_stab = 5
    ignore_stats = False
    show_coverage = False
    max_coverage = 3

    if '-s' in arguments:
        if arguments['-s']:
            show_stab = True
            max_stab = int(arguments['-s'][1:])
    if '--stab' in arguments:
        if arguments['--stab']:
            show_stab = True
    if '-c' in arguments:
        if arguments['-c']:
            show_coverage = True
            max_coverage = int(arguments['-c'][1:])
    if '--coverage' in arguments:
        if arguments['--coverage']:
            show_coverage = True
    if '--ignore-stats' in arguments:
        ignore_stats = arguments['--ignore-stats']
        if not show_stab and not show_coverage:
            ignore_stats = True

    MoveDex().do_moves_function(pokemon, show_stab, max_stab, ignore_stats, show_coverage, max_coverage, print_to=sys.stdout)
    print('')

def pokedex_func(arguments):
    print('')
    pokemon = arguments['POKEMON'].lower().replace(' ','')

    PokeDex().do_pokedex_function(pokemon, sys.stdout)
    print('')

def ha_func(arguments):
    print('')
    pokemon = arguments['POKEMON'].lower().replace(' ','')

    PokeDex().do_hidden_ability_function(pokemon, sys.stdout)
    print('')

def ability_func(arguments):
    print('')
    ability = arguments['ABILITY'].lower().replace(' ','')

    AbilityDex().do_ability_search_function(ability, sys.stdout)
    print('')

if __name__ == '__main__':
    main()