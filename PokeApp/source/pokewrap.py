import pymongo

from pymongo import MongoClient

class PokeMongo8:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['gen8']
        self.pokedex = self.db.pokedex
        self.learnsets = self.db.learnsets
        self.moves = self.db.moves
        self.abilities = self.db.abilities

    def insert_pokedex_entry(self, pokedex_entry):
        try:
            pokemon_id = self.pokedex.insert_one(pokedex_entry).inserted_id
        except:
            pass

    def insert_learnset(self, learnset):
        try:
            learnset_id = self.learnsets.insert_one(learnset).inserted_id
        except:
            pass

    def insert_move(self, move):
        try:
            move_id = self.moves.insert_one(move).inserted_id
        except:
            pass

    def insert_ability(self, ability):
        try:
            ability_id = self.abilities.insert_one(ability).inserted_id
        except:
            pass

    def get_pokedex_entry(self, id):
        return self.pokedex.find_one({'_id':id})

    def get_pokedex_entries(self, ids):
        collection = []
        entries = self.pokedex.find({'_id': {'$in': ids}})
        for entry in entries:
            collection.append(entry)
        return collection

    def get_all_pokedex_ids(self):
        collection = []
        entries = self.pokedex.find({}, {'_id':1})
        for entry in entries:
            collection.append(entry)
        return collection

    def get_learnset(self, id):
        return self.learnsets.find_one({'_id':id})

    def get_learnsets(self, ids):
        collection = []
        entries = self.learnsets.find({'_id': {'$in': ids}})
        for entry in entries:
            collection.append(entry)
        return collection

    def get_all_learnsets(self):
        collection = []
        entries = self.learnsets.find()
        for entry in entries:
            collection.append(entry)
        return collection

    def get_move_entry(self, id):
        return self.moves.find_one({'_id':id})

    def get_move_entries(self, ids):
        collection = []
        entries = self.moves.find({'_id': {'$in': ids}})
        for entry in entries:
            collection.append(entry)
        return collection

    def get_ability(self, id):
        return self.abilities.find_one({'_id':id})

    def update_egg_moves(self, id, egg_moves):
        learnset = self.learnsets.find_one({'_id':id})
        if learnset is None:
            print(f'Unable to find learnset for {id}')
            return
        learnset['breeding'] = egg_moves
        self.learnsets.update_one({'_id':id}, {'$set': learnset})

    def update_learnset_species(self, id):
        dex_entry = self.get_pokedex_entry(id)
        learnset = self.get_learnset(id)
        if dex_entry is None:
            print(f'Unable to find dex entry for {id}')
            return
        if learnset is None:
            print(f'Unable to find learnset for {id}')
            return
        species = dex_entry['species']
        learnset['species'] = species
        self.learnsets.update_one({'_id':id}, {'$set': learnset})

    def get_egg_group(self, egg_group, full_entry=False):
        group = []
        filter = None if full_entry else {'_id':1}
        entries = self.pokedex.find({'eggGroups':egg_group}, filter)
        for pokemon in entries:
            group.append(pokemon if full_entry else pokemon['_id'])
        return group

    def get_pokemon_with_ability(self, ability_id, full_entry=False):
        group = []
        filter = None if full_entry else {'_id':1}
        entries = self.pokedex.find({'ability_list':ability_id}, filter)
        for pokemon in entries:
            group.append(pokemon if full_entry else pokemon['_id'])
        return group

    def get_pokemon_with_move_levelup(self, move, full_entry=False, get_name=True):
        group = []
        filter = None if full_entry else {'_id':1, 'species':1}
        entries = self.learnsets.find({'levelup':move}, filter)
        for pokemon in entries:
            group.append(pokemon if full_entry or get_name else pokemon['_id'])
        return group

    def get_pokemon_with_move_machine(self, move, full_entry=False, get_name=True):
        group = []
        filter = None if full_entry else {'_id':1, 'species':1}
        entries = self.learnsets.find({'machine':move}, filter)
        for pokemon in entries:
            group.append(pokemon if full_entry or get_name else pokemon['_id'])
        return group

    def get_pokemon_with_move_breeding(self, move, full_entry=False, get_name=True):
        group = []
        filter = None if full_entry else {'_id':1, 'species':1}
        entries = self.learnsets.find({'breeding':move}, filter)
        for pokemon in entries:
            group.append(pokemon if full_entry or get_name else pokemon['_id'])
        return group

    def get_evo_line(self, pokemon):
        evo_line = [pokemon]
        dex_entry = self.get_pokedex_entry(pokemon)
        if 'prevo' in dex_entry:
            evo_line.extend(self.get_evo_line(dex_entry['prevo']))
        return evo_line

    def get_evo_options(self, pokemon):
        evo_line = [pokemon]
        dex_entry = self.get_pokedex_entry(pokemon)
        if dex_entry is None:
            return []
        if 'evos' in dex_entry:
            for evo in dex_entry['evos']:
                evo_line.extend(self.get_evo_options(evo))
        return evo_line

    def get_full_evo_family(self, pokemon):
        evo_line = [pokemon]
        dex_entry = self.get_pokedex_entry(pokemon)
        if 'prevo' in dex_entry:
            evo_line.extend(self.get_evo_line(dex_entry['prevo']))
        if 'evos' in dex_entry:
            for evo in dex_entry['evos']:
                evo_line.extend(self.get_evo_options(evo))
        return evo_line