import yaml

from pprint import pprint

source_dir = 'modified'
destination_dir = 'modified'

with open(f'{source_dir}/raw_pokedex.txt', 'r') as input:
    raw_pokedex = input.read()
    pokedex = yaml.load(raw_pokedex)

    with open(f'{destination_dir}/pokedex.txt', 'wt') as output:
        pprint(pokedex, stream=output, compact=True)

with open(f'{source_dir}/raw_learnsets.txt', 'r') as input:
    raw_learnsets = input.read()
    learnsets = yaml.load(raw_learnsets)

    with open(f'{destination_dir}/learnsets.txt', 'wt') as out:
        pprint(learnsets, stream=out, compact=True)