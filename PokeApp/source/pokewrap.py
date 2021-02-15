import pymongo

from pymongo import MongoClient
from .pokehelper import PokemonHelper
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

    def get_pokedex_order_filters(self):
        types = PokemonHelper().get_types()
        lowercase_types = []
        for t in types:
            lowercase_types.append(t.lower())
        lowercase_types.extend([
            'hp', 'atk', 'def', 'spa', 'spd', 'spe', 'bst',
            'num',
            'weight', 'w', 'weightkg',
            'height', 'h', 'heightm'
        ])
        return lowercase_types

    def get_pokedex_orderby(self, filter_value, negate):
        filter_value = filter_value.lower()
        if filter_value not in self.get_pokedex_order_filters():
            return None
        if filter_value == 'hp' or filter_value == 'atk' or filter_value == 'def' or filter_value == 'spa' or filter_value == 'spd' or filter_value == 'spe' or filter_value == 'bst':
            return [(f'baseStats.{filter_value}', 1 if negate else -1)]
        types = PokemonHelper().get_types()
        lowercase_types = []
        for t in types:
            lowercase_types.append(t.lower())
        if filter_value in lowercase_types:
            return [(f'coverage.{filter_value.capitalize()}', 1 if negate else -1)]
        if filter_value == 'num':
            negate = not negate
        if filter_value == 'weight' or filter_value == 'w':
            filter_value = 'weightkg'
        if filter_value == 'height' or filter_value == 'h':
            filter_value = 'heightm'
        return [(f'{filter_value}', 1 if negate else -1)]

    def update_pokedex_projection_from_filters(self, projection, filters):
        if 'o' not in filters or projection is None:
            return projection
        orderby = self.get_pokedex_orderby(filters['o'], False)
        if orderby is not None:
            projection[orderby[0][0]] = 1
        return projection
    
    def get_pokedex_orderby_key(self, filters):
        if 'o' not in filters:
            return None
        orderby = self.get_pokedex_orderby(filters['o'], False)
        if orderby is not None:
            return orderby[0][0]
        return None

    def get_move_order_filters(self):
        return [
            'num', 'name',
            'accuracy', 'acc', 'a',
            'basePower', 'power', 'pow',
            'category', 'cat', 'c',
            'priority', 'prio', 'p'
        ]

    def get_movedex_orderby(self, filter_value, negate):
        filter_value = filter_value.lower()
        if filter_value not in self.get_move_order_filters():
            return None
        if filter_value == 'num' or filter_value == 'name':
            negate = not negate
        if filter_value == 'acc' or filter_value == 'a':
            filter_value = 'accuracy'
        if filter_value == 'pow' or filter_value == 'power':
            filter_value = 'basePower'
        if filter_value == 'cat' or filter_value == 'c':
            filter_value = 'category'
        if filter_value == 'category':
            negate = not negate
        if filter_value == 'prio' or filter_value == 'p':
            filter_value = 'priority'
        return [(f'{filter_value}', 1 if negate else -1)]

    def get_movedex_orderby_key(self, filters):
        if 'o' not in filters:
            return None
        orderby = self.get_movedex_orderby(filters['o'], False)
        if orderby is not None:
            return orderby[0][0]
        return None

    def get_simple_object_from_filter_value(self, filter_value, negate=False):
        if ',' in filter_value:
            filters = []
            for v in filter_value.split(','):
                filters.append(self.get_simple_object_from_filter_value(v, negate))
            return {'$and': filters}
        if negate:
            if '>' in filter_value:
                if '=' in filter_value:
                    filter_value = filter_value.replace('>=', '<')
                else:
                    filter_value = filter_value.replace('>', '<=')
            elif '<' in filter_value:
                if '=' in filter_value:
                    filter_value = filter_value.replace('<=', '>')
                else:
                    filter_value = filter_value.replace('<', '>=')
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
                if negate:
                    return {'$ne':int(filter_value)}
                else:
                    return int(filter_value)
            except:
                return None

    def get_object_from_filter_value(self, filter_key, filter_value, negate=False):
        if ',' in filter_value:
            filters = []
            for v in filter_value.split(','):
                filters.append(self.get_object_from_filter_value(filter_key, v, negate))
            return {'$and': filters}
        if negate:
            if '>' in filter_value:
                if '=' in filter_value:
                    filter_value = filter_value.replace('>=', '<')
                else:
                    filter_value = filter_value.replace('>', '<=')
            elif '<' in filter_value:
                if '=' in filter_value:
                    filter_value = filter_value.replace('<=', '>')
                else:
                    filter_value = filter_value.replace('<', '>=')
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
                if negate:
                    return {f'baseStats.{filter_key}':{'$ne':int(filter_value)}}
                else:
                    return {f'baseStats.{filter_key}':int(filter_value)}
            except:
                if negate:
                    return self.get_stat_or_none(filter_key, filter_value, '!=')
                else:
                    return self.get_stat_or_none(filter_key, filter_value, '==')

    def convert_pokedex_mongo_filters(self, filters, exclude=[]):
        and_list = []
        orderby = None
        for f in filters:
            negate = False
            ft = f[:]
            new_key = None
            new_filter = None
            if f[0] == '~':
                negate = True
                ft = f[1:]
            if (ft == 'a' and 'a' not in exclude) or ft == 'a-force':
                ab_ids = filters[f].lower().replace(' ','').split(',')
                new_key = 'ability_list'
                if negate:
                    new_filter = {'$nin':ab_ids}
                else:
                    new_filter = {'$in':ab_ids}
            if ft == 'hp':
                hp = self.get_object_from_filter_value('hp', filters[f], negate)
                and_list.append(hp)
            if ft == 'atk':
                atk = self.get_object_from_filter_value('atk', filters[f], negate)
                and_list.append(atk)
            if ft == 'def':
                Def = self.get_object_from_filter_value('def', filters[f], negate)
                and_list.append(Def)
            if ft == 'spa':
                spa = self.get_object_from_filter_value('spa', filters[f], negate)
                and_list.append(spa)
            if ft == 'spd':
                spd = self.get_object_from_filter_value('spd', filters[f], negate)
                and_list.append(spd)
            if ft == 'spe':
                spe = self.get_object_from_filter_value('spe', filters[f], negate)
                and_list.append(spe)
            if ft == 'bst':
                bst = self.get_object_from_filter_value('bst', filters[f], negate)
                and_list.append(bst)
            if ft == 'o':
                orderby = self.get_pokedex_orderby(filters[f], negate)
            if ft == 'evo':
                evo = self.string_bool(filters[f])
                new_key = 'evos'
                if negate:
                    evo = not evo
                new_filter = {'$exists':evo}
            if ft == 'prevo':
                prevo = self.string_bool(filters[f])
                new_key = 'prevo'
                if negate:
                    prevo = not prevo
                new_filter = {'$exists':prevo}
            if (ft == 'eg' and 'eg' not in exclude) or ft == 'eg-force':
                eg = filters[f].lower().replace(' ','').split(',')
                new_key = 'eggGroups'
                if negate:
                    new_filter = {'$nin':eg}
                else:
                    new_filter = {'$in':eg}
            if ft == 'ega':
                eg = filters[f].lower().replace(' ','').split(',')
                if negate:
                    and_list.append({'eggGroups':{'$nin':eg}})
                else:
                    and_list.append({'$or':[{'eggGroups':{'$eq':eg}},{'eggGroups':{'$eq':eg[::-1]}}]})
            if ft == 'c':
                colors = filters[f].lower().replace(' ','').split(',')
                caps_colors = []
                for c in colors:
                    caps_colors.append(c.capitalize())
                new_key = 'color'
                if negate:
                    new_filter = {'$nin':caps_colors}
                else:
                    new_filter = {'$in':caps_colors}
            if ft == 't':
                types = filters[f].lower().replace(' ','').split(',')
                caps_types = []
                for t in types:
                    caps_types.append(t.capitalize())
                new_key = 'types'
                if negate:
                    new_filter = {'$nin':caps_types}
                else:
                    new_filter = {'$in':caps_types}
            if ft == 'ta':
                types = filters[f].lower().replace(' ','').split(',')
                caps_types = []
                for t in types:
                    caps_types.append(t.capitalize())
                if negate:
                    and_list.append({'types':{'$nin':caps_types}})
                else:
                    and_list.append({'$or':[{'types':{'$eq':caps_types}},{'types':{'$eq':caps_types[::-1]}}]})
            if ft == 'tr':
                tr = self.string_bool(filters[f])
                new_key = 'transfer_only'
                if negate:
                    tr = not tr
                new_filter = tr
            if ft == 'base':
                base = self.string_bool(filters[f])
                new_key = 'base_game'
                if negate:
                    base = not base
                new_filter = base
            if ft == 'ioa':
                ioa = self.string_bool(filters[f])
                new_key = 'isle_of_armor'
                if negate:
                    ioa = not ioa
                new_filter = ioa
            if ft == 'ct':
                ct = self.string_bool(filters[f])
                new_key = 'crown_tundra'
                if negate:
                    ct = not ct
                new_filter = ct
            if ft == 'past':
                past = self.string_bool(filters[f])
                new_key = 'past_only'
                if negate:
                    past = not past
                new_filter = past
            if new_key is not None:
                and_list.append({new_key:new_filter})
        query = {}
        if len(and_list) > 0:
            query = {'$and':and_list}
        if orderby is not None:
            return {'$query':query,'$orderby':orderby}
        else:
            return query

    def convert_learnset_mongo_filters(self, filters, exclude=[]):
        and_list = []
        for f in filters:
            negate = False
            ft = f[:]
            new_key = None
            new_filter = None
            if f[0] == '~':
                negate = True
                ft = f[1:]
            if ft == 'm' and 'm' not in exclude:
                mv_ids = filters[f].lower().replace(' ','').split(',')
                new_key = 'allmoves'
                if negate:
                    new_filter = {'$nin':mv_ids}
                else:
                    new_filter = {'$all':mv_ids}
            if ft == 'ml' and 'ml' not in exclude:
                mv_ids = filters[f].lower().replace(' ','').split(',')
                new_key = 'levelup'
                if negate:
                    new_filter = {'$nin':mv_ids}
                else:
                    new_filter = {'$all':mv_ids}
            if ft == 'mm' and 'mm' not in exclude:
                mv_ids = filters[f].lower().replace(' ','').split(',')
                new_key = 'machine'
                if negate:
                    new_filter = {'$nin':mv_ids}
                else:
                    new_filter = {'$all':mv_ids}
            if ft == 'mb' and 'mb' not in exclude:
                mv_ids = filters[f].lower().replace(' ','').split(',')
                new_key = 'breeding'
                if negate:
                    new_filter = {'$nin':mv_ids}
                else:
                    new_filter = {'$all':mv_ids}
            if ft == 'mt' and 'mt' not in exclude:
                mv_ids = filters[f].lower().replace(' ','').split(',')
                new_key = 'tutor'
                if negate:
                    new_filter = {'$nin':mv_ids}
                else:
                    new_filter = {'$all':mv_ids}
            if ft == 'mtr' and 'mtr' not in exclude:
                mv_ids = filters[f].lower().replace(' ','').split(',')
                elem_match_list = []
                if negate:
                    for id in mv_ids:
                        elem_match_list.append({'transfer':{'$elemMatch':{'move':id}}})
                    and_list.append({'$nor':elem_match_list})
                else:
                    for id in mv_ids:
                        elem_match_list.append({'$elemMatch':{'move':id}})
                    and_list.append({'transfer':{'$all':elem_match_list}})
            if ft == 'mc' and 'mc' not in exclude:
                types = filters[f].lower().replace(' ','').split(',')
                caps_types = []
                for t in types:
                    caps_types.append(t.capitalize())
                for t in caps_types:
                    and_list.append({f'coverage.{t}':{'$exists':not negate}})
            if ft == 'past':
                past = self.string_bool(filters[f])
                new_key = 'past_only'
                if negate:
                    past = not past
                new_filter = past
            if new_key is not None:
                and_list.append({new_key:new_filter})
        query = {}
        if len(and_list) > 0:
            query = {'$and':and_list}
        return query

    def convert_moves_mongo_filters(self, filters, exclude=[]):
        and_list = []
        orderby = None
        for f in filters:
            negate = False
            ft = f[:]
            new_key = None
            new_filter = None
            if f[0] == '~':
                negate = True
                ft = f[1:]
            if ft == 'pow':
                power = self.get_simple_object_from_filter_value(filters[f], negate)
                new_key = 'basePower'
                new_filter = power
            if ft == 'acc':
                acc = self.get_simple_object_from_filter_value(filters[f], negate)
                if acc is None:
                    acc = self.string_bool(filters[f])
                    if negate:
                        acc = {'$ne':acc}
                new_key = 'accuracy'
                new_filter = acc
            if ft == 'c':
                cats = filters[f].lower().replace(' ','').split(',')
                caps_cats = []
                for c in cats:
                    caps_cats.append(c.capitalize())
                new_key = 'category'
                if negate:
                    new_filter = {'$nin':caps_cats}
                else:
                    new_filter = {'$in':caps_cats}
            if ft == 't':
                types = filters[f].lower().replace(' ','').split(',')
                caps_types = []
                for t in types:
                    caps_types.append(t.capitalize())
                new_key = 'type'
                if negate:
                    new_filter = {'$nin':caps_types}
                else:
                    new_filter = {'$in':caps_types}
            if ft == 'm':
                moves = filters[f].lower().replace(' ','').split(',')
                new_key = '_id'
                if negate:
                    new_filter = {'$nin':moves}
                else:
                    new_filter = {'$in':moves}
            if ft == 'sec' or ft == 'secondary':
                sec = self.string_bool(filters[f])
                if negate:
                    sec = not sec
                if sec:
                    and_list.append({'$and':[{'secondary':{'$exists':True}}, {'secondary':{'$not':{'$eq':None}}}]})
                else:
                    and_list.append({'$or':[{'secondary':{'$exists':False}}, {'secondary':None}]})
            if ft == 'bite':
                bite = self.string_bool(filters[f])
                if negate:
                    bite = not bite
                new_key = 'flags.bite'
                new_filter = {'$exists':bite}
            if ft == 'con' or ft == 'contact':
                con = self.string_bool(filters[f])
                if negate:
                    con = not con
                new_key = 'flags.contact'
                new_filter = {'$exists':con}
            if ft == 'snd' or ft == 'sound':
                snd = self.string_bool(filters[f])
                if negate:
                    snd = not snd
                new_key = 'flags.sound'
                new_filter = {'$exists':snd}
            if ft == 'pnch' or ft == 'punch':
                pnch = self.string_bool(filters[f])
                if negate:
                    pnch = not pnch
                new_key = 'flags.punch'
                new_filter = {'$exists':pnch}
            if ft == 'pls' or ft == 'pulse':
                pls = self.string_bool(filters[f])
                if negate:
                    pls = not pls
                new_key = 'flags.pulse'
                new_filter = {'$exists':pls}
            if ft == 'rec' or ft == 'recoil':
                rec = self.string_bool(filters[f])
                if negate:
                    rec = not rec
                new_key = 'recoil'
                new_filter = {'$exists':rec}
            if ft == 'p' or ft == 'prio' or ft == 'priority':
                p = self.get_simple_object_from_filter_value(filters[f], negate)
                new_key = 'priority'
                new_filter = p
            if ft == 'past':
                past = self.string_bool(filters[f])
                if negate:
                    past = not past
                new_key = 'past_only'
                new_filter = past
            if ft == 'o':
                orderby = self.get_movedex_orderby(filters[f], negate)
            if new_key is not None:
                and_list.append({new_key:new_filter})
        query = {}
        if len(and_list) > 0:
            query = {'$and':and_list}
        if orderby is not None:
            return {'$query':query,'$orderby':orderby}
        else:
            return query

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

    def get_pokedex_entry(self, id, projection=None):
        return self.pokedex.find_one({'_id':id}, projection)

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

    def get_all_pokemon_type_info(self, filters):
        collection = []
        entries = self.get_pokedex_entries_with_filters(filters=filters, projection={'_id':1, 'species':1, 'types':1, 'ability_list':1, 'baseStats.bst':1})
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
        orderby = []

        mongo_filters = self.convert_moves_mongo_filters(filters, exclude)
        if '$orderby' in mongo_filters and '$query' in mongo_filters:
            orderby = mongo_filters['$orderby']
            mongo_filters = mongo_filters['$query']
        entries = self.moves.find(mongo_filters, sort=orderby)
            
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
        orderby = []

        raw_mongo_filters = self.convert_moves_mongo_filters(filters, exclude)
        if '$orderby' in raw_mongo_filters and '$query' in raw_mongo_filters:
            orderby = raw_mongo_filters['$orderby']
            raw_mongo_filters = raw_mongo_filters['$query']
        mongo_filters = {'$and':[{'_id':{'$in':ids}}, raw_mongo_filters]}
        entries = self.moves.find(mongo_filters, sort=orderby)

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
        orderby = []

        raw_mongo_filters = self.convert_moves_mongo_filters(filters, exclude)
        if '$orderby' in raw_mongo_filters and '$query' in raw_mongo_filters:
            orderby = raw_mongo_filters['$orderby']
            raw_mongo_filters = raw_mongo_filters['$query']
        mongo_filters = {'$and':[{'_id':{'$in':ids}}, raw_mongo_filters]}
        entries = self.moves.find(mongo_filters, sort=orderby)
            
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

    def get_all_abilities(self):
        collection = []
        entries = self.abilities.find()
        for entry in entries:
            collection.append(entry)
        return collection

    def update_egg_moves(self, id, egg_moves):
        learnset = self.learnsets.find_one({'_id':id})
        if learnset is None:
            print(f'Unable to find learnset for {id}')
            return
        for move in egg_moves:
            if move not in learnset['allmoves']:
                learnset['allmoves'].append(move)
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
        learnset['species'] = dex_entry['species']
        learnset['past_only'] = dex_entry['past_only']
        self.learnsets.update_one({'_id':id}, {'$set': learnset})

    def update_learnset_coverage(self, id, coverage, learnset=None):
        if learnset is None:
            learnset = self.get_learnset(id)
        if learnset is None:
            print(f'Unable to find learnset for {id}')
            return
        learnset['coverage'] = coverage
        self.learnsets.update_one({'_id':id}, {'$set': learnset})

    def update_pokedex_entry_coverage(self, id, coverage):
        dex_entry = self.get_pokedex_entry(id)
        if dex_entry is None:
            print(f'Unable to find dex entry for {id}')
            return
        dex_entry['coverage'] = coverage
        self.pokedex.update_one({'_id':id}, {'$set': dex_entry})

    def get_learnset_entries_with_filters(self, full_entry=False, get_name=True, get_past=True, filters={}, exclude=[]):
        group = []
        orderby = {}

        projection = None if full_entry else {'_id':1, 'species':1, 'past_only':1} if get_past else {'_id':1, 'species':1}
        mongo_filters = self.convert_pokedex_mongo_filters(filters, exclude)
        if '$orderby' in mongo_filters and '$query' in mongo_filters:
            orderby = mongo_filters['$orderby']
            mongo_filters = mongo_filters['$query']
            projection = self.update_pokedex_projection_from_filters(projection, filters)
        dex_entries = self.pokedex.find(mongo_filters, projection, sort=orderby)

        #TODO: ADD POST FILTERS

        ids = []
        for dex_entry in dex_entries:
            ids.append(dex_entry['_id'])

        mongo_filters = self.convert_learnset_mongo_filters(filters, exclude)
        entries = self.learnsets.find({'$and':[{'_id':{'$in':ids}},mongo_filters]}, projection)
            
        for pokemon in entries:
            group.append(pokemon if full_entry or get_name or get_past else pokemon['_id'])
        return group

    def get_pokedex_entries_with_filters(self, full_entry=False, get_name=True, filters={}, exclude=[], projection=None):
        group = []
        orderby = {}

        if projection is None:
            projection = None if full_entry else {'_id':1, 'species':1}
        mongo_filters = self.convert_learnset_mongo_filters(filters, exclude)
        entries = self.learnsets.find(mongo_filters, projection)

        ids = []
        for entry in entries:
            ids.append(entry['_id'])

        mongo_filters = self.convert_pokedex_mongo_filters(filters, exclude)
        if '$orderby' in mongo_filters and '$query' in mongo_filters:
            orderby = mongo_filters['$orderby']
            mongo_filters = mongo_filters['$query']
            projection = self.update_pokedex_projection_from_filters(projection, filters)
        dex_entries = self.pokedex.find({'$and':[{'_id':{'$in':ids}},mongo_filters]}, projection, sort=orderby)

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

    def get_pokemon_with_move(self, learn_method, move, full_entry=False, get_name=True, get_past=True, filters={}):
        mod_filters = self.add_filter(filters, {('m'+learn_method[0]):move})
        return self.get_learnset_entries_with_filters(full_entry, get_name, get_past, mod_filters)

    def get_pokemon_with_move_levelup(self, move, full_entry=False, get_name=True, get_past=True, filters={}):
        return self.get_pokemon_with_move('levelup', move, full_entry, get_name, get_past, filters)

    def get_pokemon_with_move_machine(self, move, full_entry=False, get_name=True, get_past=True, filters={}):
        return self.get_pokemon_with_move('machine', move, full_entry, get_name, get_past, filters)

    def get_pokemon_with_move_breeding(self, move, full_entry=False, get_name=True, get_past=True, filters={}):
        return self.get_pokemon_with_move('breeding', move, full_entry, get_name, get_past, filters)

    def get_pokemon_with_move_tutor(self, move, full_entry=False, get_name=True, get_past=True, filters={}):
        return self.get_pokemon_with_move('tutor', move, full_entry, get_name, get_past, filters)

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