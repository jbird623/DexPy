import pymongo

from pymongo import MongoClient
from pprint import pprint

class PokeMongo8:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['gen8']
        self.pokedex = self.db.pokedex
        self.learnsets = self.db.learnsets
        self.moves = self.db.moves
        self.abilities = self.db.abilities
        self.breedingboxes = self.db.breedingboxes

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

    def get_or_register_bb(self, user, username):
        bb_entry = self.breedingboxes.find_one({'_id':user})
        if bb_entry is None:
            bb_entry = dict()
            bb_entry['_id'] = user
            bb_entry['username'] = username
            bb_entry['ha_list'] = []
            try:
                id = self.breedingboxes.insert_one(bb_entry).inserted_id
            except:
                print(f'Hit exception trying to register breeding box for user {user}')
                return None
        if bb_entry['username'] != username:
            bb_entry['username'] = username
            self.update_bb_entry(user, bb_entry)
        return bb_entry

    def update_bb_entry(self, user, bb_entry):
        try:
            self.breedingboxes.update_one({'_id':user}, {'$set': bb_entry})
            return True
        except:
            print(f'Hit exception trying to update breeding box for user {user}')
            return False

    def get_bb_entries(self, ids):
        collection = []
        for id in ids:
            entries = self.breedingboxes.find({'ha_list': id}, {'_id':1, 'username':1})
            for entry in entries:
                collection.append({'name':entry['username'], 'pokemon':id})
        return collection

    def get_pokedex_entry(self, id):
        return self.pokedex.find_one({'_id':id})

    def get_pokedex_entries(self, ids):
        collection = []
        entries = self.pokedex.find({'_id': {'$in': ids}})
        for entry in entries:
            collection.append(entry)
        return collection

    def get_pokemon_species_map(self, ids):
        names = dict()
        entries = self.pokedex.find({'_id': {'$in': ids}}, {'_id':1, 'species':1})
        for entry in entries:
            names[entry['_id']] = entry['species']
        return names

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

    #TODO: ADD FILTERS
    def get_move_entries(self, ids, filters={}):
        collection = []
        entries = self.moves.find({'_id': {'$in': ids}})
        for entry in entries:
            collection.append(entry)
        return collection

    def get_ability(self, id):
        return self.abilities.find_one({'_id':id})

    def get_abilities(self, ids):
        collection = []
        entries = self.abilities.find({'_id': {'$in': ids}})
        for entry in entries:
            collection.append(entry)
        return collection

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

    #TODO: ADD FILTERS
    def get_egg_group(self, egg_group, full_entry=False, filters={}):
        group = []
        filter = None if full_entry else {'_id':1}
        entries = self.pokedex.find({'eggGroups':egg_group}, filter)
        for pokemon in entries:
            group.append(pokemon if full_entry else pokemon['_id'])
        return group

    #TODO: ADD FILTERS
    def get_minimum_egg_group(self, egg_group, filters={}):
        group = []
        entries = self.get_egg_group(egg_group, full_entry=True)
        for pokemon in entries:
            is_prevo = True
            if 'prevo' in pokemon:
                for entry in entries:
                    if entry['_id'] == pokemon['prevo']:
                        is_prevo = False
                        break
            if is_prevo:
                group.append(pokemon)
        return group

    #TODO: ADD FILTERS
    def get_pokemon_with_ability(self, ability_id, full_entry=False, filters={}):
        group = []
        filter = None if full_entry else {'_id':1}
        entries = self.pokedex.find({'ability_list':ability_id}, filter)
        for pokemon in entries:
            group.append(pokemon if full_entry else pokemon['_id'])
        return group

    #TODO: ADD FILTERS
    def get_pokemon_with_move(self, learn_method, move, full_entry=False, get_name=True, filters={}):
        group = []
        filter = None if full_entry else {'_id':1, 'species':1}
        entries = self.learnsets.find({learn_method:move}, filter)
        for pokemon in entries:
            group.append(pokemon if full_entry or get_name else pokemon['_id'])
        return group

    def get_pokemon_with_move_levelup(self, move, full_entry=False, get_name=True, filters={}):
        return self.get_pokemon_with_move('levelup', move, full_entry, get_name, filters)

    def get_pokemon_with_move_machine(self, move, full_entry=False, get_name=True, filters={}):
        return self.get_pokemon_with_move('machine', move, full_entry, get_name, filters)

    def get_pokemon_with_move_breeding(self, move, full_entry=False, get_name=True, filters={}):
        return self.get_pokemon_with_move('breeding', move, full_entry, get_name, filters)

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
        if dex_entry is None:
            print(f'Error: Cannot find pokedex entry for "{pokemon}".')
            return False
        if 'prevo' in dex_entry:
            evo_line.extend(self.get_evo_line(dex_entry['prevo']))
        if 'evos' in dex_entry:
            for evo in dex_entry['evos']:
                evo_line.extend(self.get_evo_options(evo))
        return evo_line