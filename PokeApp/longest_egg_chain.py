"""
Usage: longest_egg_chain.py [MAX_DEPTH]

Find the longest egg move breeding chains.

Arguments:
  MAX_DEPTH     Forced max depth.
"""
import sys

from docopt import docopt
from source.movedex import MoveDex

from source.pokewrap import PokeMongo8
from pprint import pprint

pokemongo = PokeMongo8()

def get_chain_depth(option, depth):
    if 'chain' in option:
        max_depth = depth
        for opt in option['chain']:
            d = get_chain_depth(opt, depth + 1)
            if d > max_depth:
                max_depth = d
        return max_depth
    else:
        return depth

def main():
    arguments = docopt(__doc__)
    force_max_depth = 100 if not arguments['MAX_DEPTH'] else int(arguments['MAX_DEPTH'])
    all_learnsets = pokemongo.get_all_learnsets()
    longest_chain = 0
    longest_chains = []
    for learnset in all_learnsets:
        pokemon = learnset['_id']
        eggmoves = learnset['breeding']
        print(f'Checking {pokemon}...')
        for move in eggmoves:
            options = MoveDex().find_egg_move_chain(pokemon, move, [], sys.stdout)
            if options == False:
                continue
            max_depth = 1
            for option in options:
                depth = get_chain_depth(option, 1)
                if depth > force_max_depth:
                    continue
                if depth > max_depth:
                    max_depth = depth
                if depth > longest_chain:
                    longest_chain = depth
                    longest_chains = []
            if max_depth == longest_chain:
                longest_chains.append({'pokemon':pokemon, 'move':move})
    print(f'\nLongest Chain: {longest_chain}')
    pprint(longest_chains)
    

main()