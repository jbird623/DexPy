import sys
import re
import yaml

class Validators:

    def __init__(self, pokemongo8):
        self.pokemongo = pokemongo8
        self.valid_pokemon = self.init_pokemon_list()
        self.valid_moves = self.init_move_list()
        self.valid_abilities = self.init_ability_list()
        self.valid_abilities_type_effectiveness = self.init_ability_type_effectiveness_list()
        self.valid_abilities_damage_taken = self.init_ability_damage_taken_list()
        self.valid_abilities_damage_dealt = self.init_ability_damage_dealt_list()
        self.valid_types = self.init_type_list()
        self.valid_egg_groups = self.init_egg_group_list()
        self.valid_stats = self.init_stat_list()
        self.valid_stat_boosts = self.init_stat_boost_list()
        self.valid_nature_stats = self.init_stat_nature_list()
        self.valid_natures = self.init_nature_list()
        self.valid_categories = self.init_category_list()
        self.valid_move_flags = self.init_move_flag_list()
        self.valid_colors = self.init_color_list()

    def init_pokemon_list(self):
        collection = []
        raw_list = self.pokemongo.get_all_pokedex_ids()
        for entry in raw_list:
            collection.append(entry['_id'])
        return collection

    def init_move_list(self):
        collection = []
        raw_list = self.pokemongo.get_all_moves()
        for entry in raw_list:
            collection.append(entry['_id'])
        return collection
    
    def init_ability_list(self):
        collection = []
        raw_list = self.pokemongo.get_all_abilities()
        for entry in raw_list:
            collection.append(entry['_id'])
        return collection

    def init_ability_type_effectiveness_list(self):
        collection = []
        ability_dict = self.pokemongo.pokehelper.get_type_effectiveness_ability_dict()
        for ability in ability_dict:
            collection.append(ability)
        return collection

    def init_ability_damage_taken_list(self):
        collection = []
        ability_dict = self.pokemongo.pokehelper.get_defensive_ability_dict()
        for ability in ability_dict:
            collection.append(ability)
        return collection

    def init_ability_damage_dealt_list(self):
        collection = []
        ability_dict = self.pokemongo.pokehelper.get_offensive_ability_dict()
        for ability in ability_dict:
            collection.append(ability)
        return collection

    def init_type_list(self):
        collection = []
        caps_types = self.pokemongo.pokehelper.get_types()
        for t in caps_types:
            collection.append(t.lower())
        return collection

    def init_egg_group_list(self):
        return self.pokemongo.pokehelper.get_egg_groups()

    def init_stat_list(self):
        collection = []
        stat_dict = self.pokemongo.pokehelper.get_stats()
        for stat in stat_dict:
            collection.append(stat)
        return collection

    def init_stat_boost_list(self):
        collection = []
        stat_dict = self.pokemongo.pokehelper.get_boost_stats()
        for stat in stat_dict:
            collection.append(stat)
        return collection
    
    def init_stat_nature_list(self):
        collection = []
        stat_dict = self.pokemongo.pokehelper.get_nature_stats()
        for stat in stat_dict:
            collection.append(stat)
        return collection

    def init_nature_list(self):
        collection = []
        nature_dict = self.pokemongo.pokehelper.get_nature_stats_map()
        for nature in nature_dict:
            collection.append(nature.lower())
        return collection

    def init_category_list(self):
        return ['physical','special','status']
    
    def init_move_flag_list(self):
        return self.pokemongo.pokehelper.get_move_flags()

    def init_color_list(self):
        collection = []
        caps_colors = self.pokemongo.pokehelper.get_colors()
        for c in caps_colors:
            collection.append(c.lower())
        return collection

    def validate_value(self, value, value_type):
        if isinstance(value_type, list):
            for v_type in value_type:
                if self.validate_value(value, v_type)[0]:
                    return (True, value)
            return (False, value)
        if 'list-' in value_type:
            list_type = value_type[5:]
            value_tokens = value.split(',')
            for token in value_tokens:
                if not self.validate_value(token, list_type)[0]:
                    return (False, token)
            return (True, value)
        if 'comp-' in value_type:
            comp_value = re.sub('[<>=]', '', value)
            comp_type = value_type[5:]
            return self.validate_value(comp_value, comp_type)
        elif value_type == 'pokemon':
            return (value in self.valid_pokemon, value)
        elif value_type == 'move':
            return (value in self.valid_moves, value)
        elif value_type == 'ability':
            return (value in self.valid_abilities, value)
        elif value_type == 'ability-te':
            return (value in self.valid_abilities_type_effectiveness, value)
        elif value_type == 'ability-dt':
            return (value in self.valid_abilities_damage_taken, value)
        elif value_type == 'ability-dd':
            return (value in self.valid_abilities_damage_dealt, value)
        elif value_type == 'type':
            return (value in self.valid_types, value)
        elif value_type == 'egg-group':
            return (value in self.valid_egg_groups, value)
        elif value_type == 'stat':
            return (value in self.valid_stats, value)
        elif value_type == 'stat-b':
            return (value in self.valid_stat_boosts, value)
        elif value_type == 'stat-n':
            return (value in self.valid_nature_stats, value)
        elif value_type == 'nature':
            return (value in self.valid_natures, value)
        elif value_type == 'category':
            return (value in self.valid_categories, value)
        elif value_type == 'move-flag':
            return (value in self.valid_move_flags, value)
        elif value_type == 'color':
            return (value in self.valid_colors, value)
        elif value_type == 'boolean':
            value_is_bool = value.lower() == 'true' or value.lower() == 'false'
            return (value_is_bool, value)
        elif value_type == 'int':
            return (value.isnumeric(), value)
        elif value_type == 'sort-pkmn':
            valid_sort_value = value in ['num','weight','w','height','h']
            return (valid_sort_value, value)
        elif value_type == 'sort-move':
            valid_sort_value = value in ['num','power','pow','accuracy','acc','a','category','cat','c','priority','prio','p']
            return (valid_sort_value, value)
        else:
            print(f'ERROR: Unknown value type \'{value_type}\'')
            return (False, value)

    def get_caps_value_type(self, value_type):
        if isinstance(value_type, list):
            return None
        if 'list-' in value_type:
            return self.get_caps_value_type(value_type[5:])
        if 'comp-' in value_type:
            return f'{self.get_caps_value_type(value_type[5:])} Comparator'
        caps_value_type = value_type.capitalize()
        if value_type == 'egg-group':
            caps_value_type = 'Egg Group'
        if value_type == 'move-flag':
            caps_value_type = 'Move Flag'
        if value_type == 'ability-te':
            caps_value_type = 'Ability that changes type effectiveness'
        if value_type == 'ability-dt':
            caps_value_type = 'Ability that changes damage taken'
        if value_type == 'ability-dd':
            caps_value_type = 'Ability that changes damage dealt'
        if value_type == 'stat-b':
            caps_value_type = 'Stat that can be boosted'
        if value_type == 'stat-n':
            caps_value_type = 'Stat that can be affected by natures'
        if 'sort' in value_type:
            caps_value_type = 'Sorting Key'
        return caps_value_type

    def format_error_message(self, value, value_type):
        caps_value_type = self.get_caps_value_type(value_type)
        if isinstance(value_type, list):
            cv_types = []
            for v_type in value_type:
                cv_types.append(self.get_caps_value_type(v_type))
            caps_value_type = ' or '.join(cv_types)
        return f'\'{value}\' is not a valid {caps_value_type}!'

    def format_filter_error_message(self, filter_key, message):
        return f'Invalid value for the \'{filter_key}\' filter; {message}'

    def validate_filter(self, filter_key, filter_value, filter_type):
        filter_value_type = None
        if filter_type == 'pkmn' and filter_key == 'a':
            filter_value_type = 'list-ability'
        elif filter_type == 'pkmn' and filter_key == 'num':
            filter_value_type = 'comp-int'
        elif filter_type == 'pkmn' and filter_key == 'evo':
            filter_value_type = 'boolean'
        elif filter_type == 'pkmn' and filter_key == 'prevo':
            filter_value_type = 'boolean'
        elif filter_type == 'pkmn' and filter_key == 'eg':
            filter_value_type = 'list-egg-group'
        elif filter_type == 'pkmn' and filter_key == 'ega':
            filter_value_type = 'list-egg-group'
        elif filter_type == 'pkmn' and filter_key == 'c':
            filter_value_type = 'list-color'
        elif filter_type == 'pkmn' and filter_key == 't':
            filter_value_type = 'list-type'
        elif filter_type == 'pkmn' and filter_key == 'ta':
            filter_value_type = 'list-type'
        elif filter_type == 'pkmn' and filter_key == 'p':
            filter_value_type = 'list-pokemon'
        elif filter_type == 'pkmn' and filter_key == 'base':
            filter_value_type = 'boolean'
        elif filter_type == 'pkmn' and filter_key == 'tr':
            filter_value_type = 'boolean'
        elif filter_type == 'pkmn' and filter_key == 'ioa':
            filter_value_type = 'boolean'
        elif filter_type == 'pkmn' and filter_key == 'ct':
            filter_value_type = 'boolean'
        elif filter_type == 'pkmn' and filter_key == 'past':
            filter_value_type = 'boolean'
        elif filter_type == 'pkmn' and filter_key == 'm':
            filter_value_type = 'list-move'
        elif filter_type == 'pkmn' and filter_key == 'ml':
            filter_value_type = 'list-move'
        elif filter_type == 'pkmn' and filter_key == 'mm':
            filter_value_type = 'list-move'
        elif filter_type == 'pkmn' and filter_key == 'mb':
            filter_value_type = 'list-move'
        elif filter_type == 'pkmn' and filter_key == 'mt':
            filter_value_type = 'list-move'
        elif filter_type == 'pkmn' and filter_key == 'mtr':
            filter_value_type = 'list-move'
        elif filter_type == 'pkmn' and filter_key == 'mc':
            filter_value_type = 'list-type'
        elif filter_type == 'pkmn' and filter_key == 'mca':
            filter_value_type = 'list-type'
        elif filter_type == 'pkmn' and filter_key in self.valid_stats:
            filter_value_type = ['list-comp-int','list-comp-stat']
        elif filter_type == 'pkmn' and filter_key == 'o':
            filter_value_type = ['stat','type','sort-pkmn']
        elif filter_type == 'move' and filter_key == 'pow':
            filter_value_type = 'comp-int'
        elif filter_type == 'move' and filter_key == 'acc':
            filter_value_type = ['comp-int','boolean']
        elif filter_type == 'move' and filter_key == 'pp':
            filter_value_type = 'comp-int'
        elif filter_type == 'move' and filter_key == 'priority':
            filter_value_type = 'comp-int'
        elif filter_type == 'move' and filter_key == 'prio':
            filter_value_type = 'comp-int'
        elif filter_type == 'move' and filter_key == 'p':
            filter_value_type = 'comp-int'
        elif filter_type == 'move' and filter_key == 'c':
            filter_value_type = 'list-category'
        elif filter_type == 'move' and filter_key == 't':
            filter_value_type = 'list-type'
        elif filter_type == 'move' and filter_key == 'm':
            filter_value_type = 'list-move'
        elif filter_type == 'move' and filter_key == 'b':
            filter_value_type = ['list-stat-b','boolean']
        elif filter_type == 'move' and filter_key == 'bs':
            filter_value_type = ['list-stat-b','boolean']
        elif filter_type == 'move' and filter_key == 'bt':
            filter_value_type = ['list-stat-b','boolean']
        elif filter_type == 'move' and filter_key == 'l':
            filter_value_type = ['list-stat-b','boolean']
        elif filter_type == 'move' and filter_key == 'ls':
            filter_value_type = ['list-stat-b','boolean']
        elif filter_type == 'move' and filter_key == 'lt':
            filter_value_type = ['list-stat-b','boolean']
        elif filter_type == 'move' and filter_key == 'crit':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'cr':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'ohko':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'ko':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'multihit':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'mh':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'status':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'st':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'flags':
            filter_value_type = 'list-move-flag'
        elif filter_type == 'move' and filter_key == 'flag':
            filter_value_type = 'list-move-flag'
        elif filter_type == 'move' and filter_key == 'f':
            filter_value_type = 'list-move-flag'
        elif filter_type == 'move' and filter_key == 'secondary':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'sec':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 's':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'recoil':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'rec':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'r':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'drain':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'dr':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'selfdestruct':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'sd':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'protect':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'pr':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'switch':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'sw':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'forceswitch':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'fsw':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'terrain':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'te':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'weather':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'w':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'room':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'rm':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'past':
            filter_value_type = 'boolean'
        elif filter_type == 'move' and filter_key == 'o':
            filter_value_type = 'sort-move'
        if filter_value_type is None:
            return None
        else:
            validation_result = self.validate_value(filter_value, filter_value_type)
            if not validation_result[0]:
                return (False, self.format_error_message(validation_result[1], filter_value_type))
            return validation_result