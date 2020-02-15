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

    def add_filter(self, filters, new_filter):
        mod_filters = dict()
        for key in filters:
            mod_filters[key] = filters[key]
        for new_filter_key in new_filter:
            if new_filter_key in mod_filters:
                mod_filters[new_filter_key] = mod_filters[new_filter_key] + ',' + new_filter[new_filter_key]
            else:
                mod_filters[new_filter_key] = new_filter[new_filter_key]
        return mod_filters

    def string_bool(self, s):
        if s == 'true' or s == 'True':
            return True
        if s == 'false' or s == 'False':
            return False
        return None

    def get_stat_or_none(self, filter_key, filter_value, comparator):
        if filter_value == 'hp' or filter_value == 'atk' or filter_value == 'def' or filter_value == 'spa' or filter_value == 'spd' or filter_value == 'spe' or filter_value == 'bst':
            return {'$where': f'this.baseStats.{filter_key} {comparator} this.baseStats.{filter_value}'} 
        return None

    def get_simple_object_from_filter_value(self, filter_value):
        if ',' in filter_value:
            filters = []
            for v in filter_value.split(','):
                filters.append(self.get_simple_object_from_filter_value(v))
            return {'$and': filters}
        if filter_value[0] == '>':
            try:
                if filter_value[1] == '=':
                    return {'$gte':int(filter_value[2:])}
                else:
                    return {'$gt':int(filter_value[1:])}
            except:
                return None
        elif filter_value[0] == '<':
            try:
                if filter_value[1] == '=':
                    return {'$lte':int(filter_value[2:])}
                else:
                    return {'$lt':int(filter_value[1:])}
            except:
                return None
        else:
            try:
                return int(filter_value)
            except:
                return None

    def get_object_from_filter_value(self, filter_key, filter_value):
        if ',' in filter_value:
            filters = []
            for v in filter_value.split(','):
                filters.append(self.get_object_from_filter_value(filter_key, v))
            return {'$and': filters}
        if filter_value[0] == '>':
            try:
                if filter_value[1] == '=':
                    return {f'baseStats.{filter_key}':{'$gte':int(filter_value[2:])}}
                else:
                    return {f'baseStats.{filter_key}':{'$gt':int(filter_value[1:])}}
            except:
                if filter_value[1] == '=':
                    return self.get_stat_or_none(filter_key, filter_value[2:], '>=')
                else:
                    return self.get_stat_or_none(filter_key, filter_value[1:], '>')
        elif filter_value[0] == '<':
            try:
                if filter_value[1] == '=':
                    return {f'baseStats.{filter_key}':{'$lte':int(filter_value[2:])}}
                else:
                    return {f'baseStats.{filter_key}':{'$lt':int(filter_value[1:])}}
            except:
                if filter_value[1] == '=':
                    return self.get_stat_or_none(filter_key, filter_value[2:], '<=')
                else:
                    return self.get_stat_or_none(filter_key, filter_value[1:], '<')
        else:
            try:
                return {f'baseStats.{filter_key}':int(filter_value)}
            except:
                return self.get_stat_or_none(filter_key, filter_value, '==')

    def convert_pokedex_mongo_filters(self, filters, exclude=[]):
        and_list = []
        for f in filters:
            if f == 'a' and 'a' not in exclude:
                ab_ids = filters['a'].lower().replace(' ','').split(',')
                and_list.append({'ability_list':{'$in':ab_ids}})
            if f == 'a-force':
                ab_ids = filters['a-force'].lower().replace(' ','').split(',')
                and_list.append({'ability_list':{'$in':ab_ids}})
            if f == 'hp':
                hp = self.get_object_from_filter_value('hp', filters['hp'])
                and_list.append(hp)
            if f == 'atk':
                atk = self.get_object_from_filter_value('atk', filters['atk'])
                and_list.append(atk)
            if f == 'def':
                Def = self.get_object_from_filter_value('def', filters['def'])
                and_list.append(Def)
            if f == 'spa':
                spa = self.get_object_from_filter_value('spa', filters['spa'])
                and_list.append(spa)
            if f == 'spd':
                spd = self.get_object_from_filter_value('spd', filters['spd'])
                and_list.append(spd)
            if f == 'spe':
                spe = self.get_object_from_filter_value('spe', filters['spe'])
                and_list.append(spe)
            if f == 'bst':
                bst = self.get_object_from_filter_value('bst', filters['bst'])
                and_list.append(bst)
            if f == 'evo':
                evo = self.string_bool(filters['evo'])
                and_list.append({'evos':{'$exists':evo}})
            if f == 'prevo':
                prevo = self.string_bool(filters['prevo'])
                and_list.append({'prevo':{'$exists':prevo}})
            if f == 'eg' and 'eg' not in exclude:
                eg = filters['eg'].lower().replace(' ','')
                and_list.append({'eggGroups':eg})
            if f == 'eg-force':
                eg = filters['eg-force'].lower().replace(' ','')
                and_list.append({'eggGroups':eg})
            if f == 't':
                types = filters['t'].lower().replace(' ','').split(',')
                caps_types = []
                for t in types:
                    caps_types.append(t.capitalize())
                and_list.append({'types':{'$in':caps_types}})
            if f == 'ta':
                types = filters['ta'].lower().replace(' ','').split(',')
                caps_types = []
                for t in types:
                    caps_types.append(t.capitalize())
                and_list.append({'types':{'$all':caps_types}})
            if f == 'tr':
                tr = self.string_bool(filters['tr'])
                and_list.append({'transfer_only':tr})
        if len(and_list) > 0:
            return {'$and':and_list}
        else:
            return {}

    def convert_learnset_mongo_filters(self, filters, exclude=[]):
        and_list = []
        for f in filters:
            if f == 'm' and 'm' not in exclude:
                mv_ids = filters['m'].lower().replace(' ','').split(',')
                and_list.append({'allmoves':{'$all':mv_ids}})
            if f == 'ml' and 'ml' not in exclude:
                mv_ids = filters['ml'].lower().replace(' ','').split(',')
                and_list.append({'levelup':{'$all':mv_ids}})
            if f == 'mm' and 'mm' not in exclude:
                mv_ids = filters['mm'].lower().replace(' ','').split(',')
                and_list.append({'machine':{'$all':mv_ids}})
            if f == 'mb' and 'mb' not in exclude:
                mv_ids = filters['mb'].lower().replace(' ','').split(',')
                and_list.append({'breeding':{'$all':mv_ids}})
            if f == 'mt' and 'mt' not in exclude:
                mv_ids = filters['mt'].lower().replace(' ','').split(',')
                and_list.append({'tutor':{'$all':mv_ids}})
            if f == 'mtr' and 'mtr' not in exclude:
                mv_ids = filters['mtr'].lower().replace(' ','').split(',')
                elem_match_list = []
                for id in mv_ids:
                    elem_match_list.append({'$elemMatch':{'move':id}})
                and_list.append({'transfer':{'$all':elem_match_list}})
        if len(and_list) > 0:
            return {'$and':and_list}
        else:
            return {}

    def convert_moves_mongo_filters(self, filters, exclude=[]):
        and_list = []
        for f in filters:
            if f == 'pow':
                power = self.get_simple_object_from_filter_value(filters['pow'])
                and_list.append({'basePower':power})
            if f == 'acc':
                acc = self.get_simple_object_from_filter_value(filters['acc'])
                if acc is None:
                    acc = self.string_bool(filters['acc'])
                and_list.append({'accuracy':acc})
            if f == 'c':
                cats = filters['c'].lower().replace(' ','').split(',')
                caps_cats = []
                for c in cats:
                    caps_cats.append(c.capitalize())
                and_list.append({'category':{'$in':caps_cats}})
            if f == 't':
                types = filters['t'].lower().replace(' ','').split(',')
                caps_types = []
                for t in types:
                    caps_types.append(t.capitalize())
                and_list.append({'type':{'$in':caps_types}})
            if f == 'm':
                moves = filters['m'].lower().replace(' ','').split(',')
                and_list.append({'_id':{'$in':moves}})
        if len(and_list) > 0:
            return {'$and':and_list}
        else:
            return {}

    def get_pokedex_post_filters(self, filters):
        return {}

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

    def get_move_entries_with_filters(self, filters={}, exclude=[]):
        collection = []

        mongo_filters = self.convert_moves_mongo_filters(filters, exclude)
        entries = self.moves.find(mongo_filters)
            
        for entry in entries:
            collection.append(entry)
        return collection

    def get_transfer_move_entries(self, moves, filters={}, exclude=[]):
        ids = []
        methods = []
        for move in moves:
            ids.append(move['move'])
            methods.append(move['method'])

        collection = []

        mongo_filters = {'$and':[{'_id':{'$in':ids}}, self.convert_moves_mongo_filters(filters, exclude)]}
        entries = self.moves.find(mongo_filters)

        entries = list(entries)
            
        if len(entries) != len(ids):
            print(f'WARNING: Transfer Move Length Mismatch! {len(entries)} to {len(ids)}')

        offset = 0
        for i in range(len(entries)):
            entry = entries[i]
            while entry['_id'] != ids[i + offset]:
                offset += 1
            entry['method'] = methods[i + offset]
            collection.append(entry)
        return collection

    def get_move_entries(self, ids, filters={}, exclude=[]):
        collection = []

        mongo_filters = {'$and':[{'_id':{'$in':ids}}, self.convert_moves_mongo_filters(filters, exclude)]}
        entries = self.moves.find(mongo_filters)
            
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

    def get_learnset_entries_with_filters(self, full_entry=False, get_name=True, filters={}, exclude=[]):
        group = []

        projection = None if full_entry else {'_id':1, 'species':1}
        mongo_filters = self.convert_pokedex_mongo_filters(filters, exclude)
        dex_entries = self.pokedex.find(mongo_filters, projection)

        #TODO: ADD POST FILTERS

        ids = []
        for dex_entry in dex_entries:
            ids.append(dex_entry['_id'])

        mongo_filters = self.convert_learnset_mongo_filters(filters, exclude)
        entries = self.learnsets.find({'$and':[{'_id':{'$in':ids}},mongo_filters]}, projection)
            
        for pokemon in entries:
            group.append(pokemon if full_entry or get_name else pokemon['_id'])
        return group

    def get_pokedex_entries_with_filters(self, full_entry=False, get_name=True, filters={}, exclude=[]):
        group = []

        projection = None if full_entry else {'_id':1, 'species':1}
        mongo_filters = self.convert_learnset_mongo_filters(filters, exclude)
        entries = self.learnsets.find(mongo_filters, projection)

        ids = []
        for entry in entries:
            ids.append(entry['_id'])

        mongo_filters = self.convert_pokedex_mongo_filters(filters, exclude)
        dex_entries = self.pokedex.find({'$and':[{'_id':{'$in':ids}},mongo_filters]}, projection)

        #TODO: ADD POST FILTERS
            
        for pokemon in dex_entries:
            group.append(pokemon if full_entry or get_name else pokemon['_id'])
        return group

    def get_egg_group(self, egg_group, full_entry=False, get_name=True, filters={}):
        mod_filters = self.add_filter(filters, {'eg-force':egg_group})
        return self.get_pokedex_entries_with_filters(full_entry, get_name, mod_filters, ['eg'])

    def get_minimum_egg_group(self, egg_group, filters={}):
        group = []
        entries = self.get_egg_group(egg_group, full_entry=True, filters=filters)
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

    def get_pokemon_with_ability(self, ability_id, full_entry=False, get_name=True, filters={}):
        mod_filters = self.add_filter(filters, {'a-force':ability_id})
        return self.get_pokedex_entries_with_filters(full_entry, get_name, mod_filters, ['a'])

    def get_pokemon_with_move(self, learn_method, move, full_entry=False, get_name=True, filters={}):
        mod_filters = self.add_filter(filters, {('m'+learn_method[0]):move})
        return self.get_learnset_entries_with_filters(full_entry, get_name, mod_filters)

    def get_pokemon_with_move_levelup(self, move, full_entry=False, get_name=True, filters={}):
        return self.get_pokemon_with_move('levelup', move, full_entry, get_name, filters)

    def get_pokemon_with_move_machine(self, move, full_entry=False, get_name=True, filters={}):
        return self.get_pokemon_with_move('machine', move, full_entry, get_name, filters)

    def get_pokemon_with_move_breeding(self, move, full_entry=False, get_name=True, filters={}):
        return self.get_pokemon_with_move('breeding', move, full_entry, get_name, filters)

    def get_pokemon_with_move_tutor(self, move, full_entry=False, get_name=True, filters={}):
        return self.get_pokemon_with_move('tutor', move, full_entry, get_name, filters)

    def get_evo_line(self, pokemon, full_entry=False):
        dex_entry = self.get_pokedex_entry(pokemon)
        evo_line = [dex_entry if full_entry else pokemon]
        if 'prevo' in dex_entry:
            evo_line.extend(self.get_evo_line(dex_entry['prevo'], full_entry))
        return evo_line

    def get_evo_options(self, pokemon, full_entry=False):
        dex_entry = self.get_pokedex_entry(pokemon)
        evo_line = [dex_entry if full_entry else pokemon]
        if dex_entry is None:
            return []
        if 'evos' in dex_entry:
            for evo in dex_entry['evos']:
                evo_line.extend(self.get_evo_options(evo, full_entry))
        return evo_line

    def get_full_evo_family(self, pokemon, full_entry=False):
        dex_entry = self.get_pokedex_entry(pokemon)
        evo_line = [dex_entry if full_entry else pokemon]
        if dex_entry is None:
            print(f'Error: Cannot find pokedex entry for "{pokemon}".')
            return False
        if 'prevo' in dex_entry:
            evo_line.extend(self.get_evo_line(dex_entry['prevo'], full_entry))
        if 'evos' in dex_entry:
            for evo in dex_entry['evos']:
                evo_line.extend(self.get_evo_options(evo, full_entry))
        return evo_line