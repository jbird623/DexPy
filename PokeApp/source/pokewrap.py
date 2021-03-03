import pymongo
import re

from pymongo import MongoClient
from .pokehelper import PokemonHelper
from pprint import pprint

class PokeMongo8:
    def __init__(self, beta=False):
        if beta:
            self.client = MongoClient('localhost', 27018)
        else:
            self.client = MongoClient('localhost', 27017)
        self.pokehelper = PokemonHelper()
        self.db = self.client['gen8']
        self.ctx = self.client['user-ctx']
        self.pokedex = self.db.pokedex
        self.learnsets = self.db.learnsets
        self.moves = self.db.moves
        self.abilities = self.db.abilities
        self.breedingboxes = self.db.breedingboxes
        self.user_options = self.ctx.options

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

    def add_filters(self, filters, new_filters):
        for f in new_filters:
            filters = self.add_filter(filters, {f:new_filters[f]})
        return filters

    def update_user_pokemon_filters(self, user_id, filters):
        self.update_user_filters(user_id, filters, 'filters_pokemon')

    def update_user_move_filters(self, user_id, filters):
        self.update_user_filters(user_id, filters, 'filters_moves')

    def update_user_filters(self, user_id, filters, filters_key):
        user_options = self.get_user_options(user_id)
        if user_options is None:
            user_options = {'_id':user_id}
        user_options[filters_key] = filters
        try:
            self.ctx.options.update_one({'_id':user_id}, {'$set': user_options}, upsert=True)
            return True
        except:
            print(f'Hit exception trying to update filter options for user {user_id}')
            return False

    def get_user_options(self, user_id):
        user_options = self.ctx.options.find_one({'_id':user_id})
        return user_options

    def get_user_filters(self, user_id, filters_key):
        user_options = self.get_user_options(user_id)
        if user_options is not None and filters_key in user_options:
            return user_options[filters_key]
        return {}

    def add_user_pokemon_filters(self, filters, user_id):
        user_filters = self.get_user_filters(user_id, 'filters_pokemon')
        return (self.add_filters(user_filters, filters), user_filters)

    def add_user_move_filters(self, filters, user_id):
        user_filters = self.get_user_filters(user_id, 'filters_moves')
        return (self.add_filters(user_filters, filters), user_filters)

    def print_filters(self, filters, print_to):
        if len(filters) == 0:
            return
        filter_list = []
        for f in filters:
            filter_list.append(f'{f}:{filters[f]}')
        print(f'* Using additional query filters - {" ".join(filter_list)}\n', file=print_to)

    def string_bool(self, s):
        if s == 'true' or s == 'True':
            return True
        if s == 'false' or s == 'False':
            return False
        return None

    def get_stat_or_none(self, filter_key, filter_value, comparator):
        if filter_value in self.pokehelper.get_stats():
            return {'$where': f'this.baseStats.{filter_key} {comparator} this.baseStats.{filter_value}'} 
        return None

    def get_boost_stat_bool_or_none(self, boost_list, filter_value, negate):
        if filter_value in self.pokehelper.get_boost_stats():
            return {f'{boost_list}.{filter_value}':{'$exists':not negate}}
        bool_value = self.string_bool(filter_value)
        if bool_value is not None:
            if negate:
                bool_value = not bool_value
            return {f'{boost_list}':{'$exists':bool_value}}
        return None

    def get_pokedex_order_filters(self):
        types = self.pokehelper.get_types()
        lowercase_types = []
        for t in types:
            lowercase_types.append(t.lower())
        lowercase_types.extend(self.pokehelper.get_stats())
        lowercase_types.extend([
            'num',
            'weight', 'w', 'weightkg',
            'height', 'h', 'heightm'
        ])
        return lowercase_types

    def get_pokedex_orderby(self, filter_value, negate):
        filter_value = filter_value.lower()
        if filter_value not in self.get_pokedex_order_filters():
            return None
        if filter_value in self.pokehelper.get_stats():
            return [(f'baseStats.{filter_value}', 1 if negate else -1)]
        types = self.pokehelper.get_types()
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
                ab_ids = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
                new_key = 'ability_list'
                if negate:
                    new_filter = {'$nin':ab_ids}
                else:
                    new_filter = {'$in':ab_ids}
            if ft == 'hp':
                hp = self.get_object_from_filter_value('hp', filters[f].lower(), negate)
                and_list.append(hp)
            if ft == 'atk':
                atk = self.get_object_from_filter_value('atk', filters[f].lower(), negate)
                and_list.append(atk)
            if ft == 'def':
                Def = self.get_object_from_filter_value('def', filters[f].lower(), negate)
                and_list.append(Def)
            if ft == 'spa':
                spa = self.get_object_from_filter_value('spa', filters[f].lower(), negate)
                and_list.append(spa)
            if ft == 'spd':
                spd = self.get_object_from_filter_value('spd', filters[f].lower(), negate)
                and_list.append(spd)
            if ft == 'spe':
                spe = self.get_object_from_filter_value('spe', filters[f].lower(), negate)
                and_list.append(spe)
            if ft == 'bst':
                bst = self.get_object_from_filter_value('bst', filters[f].lower(), negate)
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
                eg = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
                new_key = 'eggGroups'
                if negate:
                    new_filter = {'$nin':eg}
                else:
                    new_filter = {'$in':eg}
            if ft == 'ega':
                eg = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
                if negate:
                    and_list.append({'eggGroups':{'$nin':eg}})
                else:
                    and_list.append({'$or':[{'eggGroups':{'$eq':eg}},{'eggGroups':{'$eq':eg[::-1]}}]})
            if ft == 'c':
                colors = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
                caps_colors = []
                for c in colors:
                    caps_colors.append(c.capitalize())
                new_key = 'color'
                if negate:
                    new_filter = {'$nin':caps_colors}
                else:
                    new_filter = {'$in':caps_colors}
            if ft == 't':
                types = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
                caps_types = []
                for t in types:
                    caps_types.append(t.capitalize())
                new_key = 'types'
                if negate:
                    new_filter = {'$nin':caps_types}
                else:
                    new_filter = {'$in':caps_types}
            if ft == 'ta':
                types = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
                caps_types = []
                for t in types:
                    caps_types.append(t.capitalize())
                if negate:
                    and_list.append({'types':{'$nin':caps_types}})
                else:
                    and_list.append({'$or':[{'types':{'$eq':caps_types}},{'types':{'$eq':caps_types[::-1]}}]})
            if ft == 'p':
                pokemon = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
                new_key = '_id'
                if negate:
                    new_filter = {'$nin':pokemon}
                else:
                    new_filter = {'$in':pokemon}
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
                mv_ids = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
                new_key = 'allmoves'
                if negate:
                    new_filter = {'$nin':mv_ids}
                else:
                    new_filter = {'$all':mv_ids}
            if ft == 'ml' and 'ml' not in exclude:
                mv_ids = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
                new_key = 'levelup'
                if negate:
                    new_filter = {'$nin':mv_ids}
                else:
                    new_filter = {'$all':mv_ids}
            if ft == 'mm' and 'mm' not in exclude:
                mv_ids = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
                new_key = 'machine'
                if negate:
                    new_filter = {'$nin':mv_ids}
                else:
                    new_filter = {'$all':mv_ids}
            if ft == 'mb' and 'mb' not in exclude:
                mv_ids = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
                new_key = 'breeding'
                if negate:
                    new_filter = {'$nin':mv_ids}
                else:
                    new_filter = {'$all':mv_ids}
            if ft == 'mt' and 'mt' not in exclude:
                mv_ids = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
                new_key = 'tutor'
                if negate:
                    new_filter = {'$nin':mv_ids}
                else:
                    new_filter = {'$all':mv_ids}
            if ft == 'mtr' and 'mtr' not in exclude:
                mv_ids = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
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
                types = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
                caps_types = []
                for t in types:
                    caps_types.append(t.capitalize())
                or_list = []
                for t in caps_types:
                    or_list.append({f'coverage.{t}':{'$exists':not negate}})
                if negate:
                    and_list.append({'$and':or_list})
                else:
                    and_list.append({'$or':or_list})
            if ft == 'mca' and 'mca' not in exclude:
                types = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
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
                cats = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
                caps_cats = []
                for c in cats:
                    caps_cats.append(c.capitalize())
                new_key = 'category'
                if negate:
                    new_filter = {'$nin':caps_cats}
                else:
                    new_filter = {'$in':caps_cats}
            if ft == 't':
                types = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
                caps_types = []
                for t in types:
                    caps_types.append(t.capitalize())
                new_key = 'type'
                if negate:
                    new_filter = {'$nin':caps_types}
                else:
                    new_filter = {'$in':caps_types}
            if ft == 'pp':
                pp = self.get_simple_object_from_filter_value(filters[f], negate)
                new_key = 'pp'
                new_filter = pp
            if ft == 'm':
                moves = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
                new_key = '_id'
                if negate:
                    new_filter = {'$nin':moves}
                else:
                    new_filter = {'$in':moves}
            if ft == 's' or ft == 'sec' or ft == 'secondary':
                sec = self.string_bool(filters[f])
                if negate:
                    sec = not sec
                if sec:
                    and_list.append({'$or':[{'$and':[{'secondary':{'$exists':True}}, {'secondary':{'$not':{'$eq':None}}}]}, {'secondaries':{'$exists':True}}]})
                else:
                    and_list.append({'$and':[{'$or':[{'secondary':{'$exists':False}}, {'secondary':None}]}, {'secondaries':{'$exists':False}}]})
            if ft == 'r' or ft == 'rec' or ft == 'recoil':
                rec = self.string_bool(filters[f])
                if negate:
                    rec = not rec
                new_key = 'recoil'
                new_filter = {'$exists':rec}
            if ft == 'ko' or ft == 'ohko':
                ko = self.string_bool(filters[f])
                if negate:
                    ko = not ko
                new_key = 'ohko'
                new_filter = {'$exists':ko}
            if ft == 'dr' or ft == 'drain':
                dr = self.string_bool(filters[f])
                if negate:
                    dr = not dr
                new_key = 'drain'
                new_filter = {'$exists':dr}
            if ft == 'mh' or ft == 'multi' or ft == 'multihit':
                mh = self.string_bool(filters[f])
                if negate:
                    mh = not mh
                new_key = 'multihit'
                new_filter = {'$exists':mh}
            if ft == 'pr' or ft == 'prot' or ft == 'protect':
                pr = self.string_bool(filters[f])
                if negate:
                    pr = not pr
                new_key = 'stallingMove'
                new_filter = {'$exists':pr}
            if ft == 'sw' or ft == 'switch':
                sw = self.string_bool(filters[f])
                if negate:
                    sw = not sw
                new_key = 'selfSwitch'
                new_filter = {'$exists':sw}
            if ft == 'fsw' or ft == 'fswitch' or ft == 'forceswitch':
                fsw = self.string_bool(filters[f])
                if negate:
                    fsw = not fsw
                new_key = 'forceSwitch'
                new_filter = {'$exists':fsw}
            if ft == 'st' or ft == 'stat' or ft == 'status':
                st = self.string_bool(filters[f])
                if negate:
                    st = not st
                if st:
                    and_list.append({'$or':[{'status':{'$exists':True}}, {'secondary.status':{'$exists':True}}, {'secondaries.status':{'$exists':True}}]})
                else:
                    and_list.append({'$and':[{'status':{'$exists':False}}, {'secondary.status':{'$exists':False}}, {'secondaries.status':{'$exists':False}}]})
            if ft == 'te' or ft == 'ter' or ft == 'terrain':
                te = self.string_bool(filters[f])
                if negate:
                    te = not te
                new_key = 'terrain'
                new_filter = {'$exists':te}
            if ft == 'w' or ft == 'weather':
                w = self.string_bool(filters[f])
                if negate:
                    w = not w
                new_key = 'weather'
                new_filter = {'$exists':w}
            if ft == 'rm' or ft == 'room':
                rm = self.string_bool(filters[f])
                if negate:
                    rm = not rm
                new_key = 'pseudoWeather'
                new_filter = {'$exists':rm}
            if ft == 'sd' or ft == 'selfdes' or ft == 'selfdestruct':
                sd = self.string_bool(filters[f])
                if negate:
                    sd = not sd
                new_key = 'selfdestruct'
                new_filter = {'$exists':sd}
            if ft == 'cr' or ft == 'crit':
                cr = self.string_bool(filters[f])
                if negate:
                    cr = not cr
                if cr:
                    and_list.append({'$or':[{'critRatio':{'$exists':True}}, {'willCrit':{'$exists':True}}]})
                else:
                    and_list.append({'$and':[{'critRatio':{'$exists':False}}, {'willCrit':{'$exists':False}}]})
            if ft == 'f' or ft == 'flag' or ft == 'flags':
                flags = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
                for flag in flags:
                    and_list.append({f'flags.{flag}':{'$exists':not negate}})
            if ft == 'p' or ft == 'prio' or ft == 'priority':
                p = self.get_simple_object_from_filter_value(filters[f], negate)
                new_key = 'priority'
                new_filter = p
            if ft == 'bs' or ft == 'boostself':
                bs = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
                for boost in bs:
                    boost_filter = self.get_boost_stat_bool_or_none('boost_self', boost, negate)
                    if boost_filter is not None:
                        and_list.append(boost_filter)
            if ft == 'ls' or ft == 'lowerself':
                ls = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
                for boost in ls:
                    boost_filter = self.get_boost_stat_bool_or_none('lower_self', boost, negate)
                    if boost_filter is not None:
                        and_list.append(boost_filter)
            if ft == 'bt' or ft == 'boosttarget':
                bt = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
                for boost in bt:
                    boost_filter = self.get_boost_stat_bool_or_none('boost_target', boost, negate)
                    if boost_filter is not None:
                        and_list.append(boost_filter)
            if ft == 'lt' or ft == 'lowertarget':
                lt = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
                for boost in lt:
                    boost_filter = self.get_boost_stat_bool_or_none('lower_target', boost, negate)
                    if boost_filter is not None:
                        and_list.append(boost_filter)
            if ft == 'b' or ft == 'boost':
                b = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
                for boost in b:
                    self_filter = self.get_boost_stat_bool_or_none('boost_self', boost, negate)
                    target_filter = self.get_boost_stat_bool_or_none('boost_target', boost, negate)
                    filter_bool = self.string_bool(filters[f].lower())
                    if self_filter is not None and target_filter is not None:
                        if filter_bool is not None and filter_bool == negate:
                            and_list.append({'$and':[self_filter, target_filter]})
                        elif negate and filter_bool is None:
                            and_list.append({'$and':[self_filter, target_filter]})
                        else:
                            and_list.append({'$or':[self_filter, target_filter]})
            if ft == 'l' or ft == 'lower':
                l = re.sub(r'[^a-zA-Z0-9\,]', '', filters[f].lower()).split(',')
                for boost in l:
                    self_filter = self.get_boost_stat_bool_or_none('lower_self', boost, negate)
                    target_filter = self.get_boost_stat_bool_or_none('lower_target', boost, negate)
                    filter_bool = self.string_bool(filters[f].lower())
                    if self_filter is not None and target_filter is not None:
                        if filter_bool is not None and filter_bool == negate:
                            and_list.append({'$and':[self_filter, target_filter]})
                        elif negate and filter_bool is None:
                            and_list.append({'$and':[self_filter, target_filter]})
                        else:
                            and_list.append({'$or':[self_filter, target_filter]})
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
        return pokemon_id

    def insert_learnset(self, learnset):
        try:
            learnset_id = self.learnsets.insert_one(learnset).inserted_id
        except:
            pass
        return learnset_id

    def insert_move(self, move):
        try:
            move_id = self.moves.insert_one(move).inserted_id
        except:
            pass
        return move_id

    def insert_ability(self, ability):
        try:
            ability_id = self.abilities.insert_one(ability).inserted_id
        except:
            pass
        return ability_id

    def get_or_register_bb(self, user, username):
        bb_entry = self.breedingboxes.find_one({'_id':user})
        if bb_entry is None:
            bb_entry = dict()
            bb_entry['_id'] = user
            bb_entry['username'] = username
            bb_entry['ha_list'] = []
            try:
                self.breedingboxes.insert_one(bb_entry).inserted_id
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