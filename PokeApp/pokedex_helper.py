from source.pokewrap import PokeMongo8
import yaml

pokemongo = PokeMongo8()

"""
dex_entries = pokemongo.pokedex.find({'transfer_only': True})
ids = []
for entry in dex_entries:
    ids.append(entry['_id'])

with open(f'transfer_only.txt', 'wt') as output:
    yaml.dump(ids, stream=output)

print(len(ids))
"""

move_entries = pokemongo.moves.find()
unique_keys = []
for entry in move_entries:
    for key in entry:
        if key not in unique_keys:
            unique_keys.append(key)

for key in unique_keys:
    print(key)