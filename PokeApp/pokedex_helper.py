from source.pokewrap import PokeMongo8

pokemongo = PokeMongo8()

pokemon_names = pokemongo.get_all_pokedex_ids()
max_length = 0
longest_ids = []
for name in pokemon_names:
    if len(name['_id']) > max_length:
        max_length = len(name['_id'])
        longest_ids = []
    if len(name['_id']) == max_length:
        longest_ids.append(name['_id'])

for id in longest_ids:
    print(id)

print(max_length)
