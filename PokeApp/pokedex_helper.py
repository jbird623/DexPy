from source.pokewrap import PokeMongo8

pokemongo = PokeMongo8()

abilities = pokemongo.abilities.find()
max_length = 0
longest_ids = []
for ability in abilities:
    if len(ability['shortDesc']) > 88:
        continue
    if len(ability['shortDesc']) > max_length:
        max_length = len(ability['shortDesc'])
        longest_ids = []
    if len(ability['shortDesc']) == max_length:
        longest_ids.append(ability['_id'])

for id in longest_ids:
    print(id)

print(max_length)
