class PokemonHelper:
    def __init__(self):
        pass

    def get_types(self):
        return [
            'Normal',
            'Fire',
            'Water',
            'Electric',
            'Grass',
            'Ice',
            'Fighting',
            'Poison',
            'Ground',
            'Flying',
            'Psychic',
            'Bug',
            'Rock',
            'Ghost',
            'Dragon',
            'Dark',
            'Steel',
            'Fairy'
        ]

    def get_weaknesses(self, t):
        if t == 'Normal':
            return ['Fighting']
        if t == 'Fire':
            return ['Water', 'Ground', 'Rock']
        if t == 'Water':
            return ['Electric', 'Grass']
        if t == 'Electric':
            return ['Ground']
        if t == 'Grass':
            return ['Fire', 'Ice', 'Poison', 'Flying', 'Bug']
        if t == 'Ice':
            return ['Fire', 'Fighting', 'Rock', 'Steel']
        if t == 'Fighting':
            return ['Flying', 'Psychic', 'Fairy']
        if t == 'Poison':
            return ['Ground', 'Psychic']
        if t == 'Ground':
            return ['Water', 'Grass', 'Ice']
        if t == 'Flying':
            return ['Electric', 'Ice', 'Rock']
        if t == 'Psychic':
            return ['Bug', 'Ghost', 'Dark']
        if t == 'Bug':
            return ['Fire', 'Flying', 'Rock']
        if t == 'Rock':
            return ['Water', 'Grass', 'Fighting', 'Ground', 'Steel']
        if t == 'Ghost':
            return ['Ghost', 'Dark']
        if t == 'Dragon':
            return ['Ice', 'Dragon', 'Fairy']
        if t == 'Dark':
            return ['Fighting', 'Bug', 'Fairy']
        if t == 'Steel':
            return ['Fire', 'Fighting', 'Ground']
        if t == 'Fairy':
            return ['Poison', 'Steel']
        print(f'Error: Unknown type "{t}"!')

    def get_resistances(self, t):
        if t == 'Normal':
            return []
        if t == 'Fire':
            return ['Fire', 'Grass', 'Ice', 'Bug', 'Steel', 'Fairy']
        if t == 'Water':
            return ['Fire', 'Water', 'Ice', 'Steel']
        if t == 'Electric':
            return ['Electric', 'Flying', 'Steel']
        if t == 'Grass':
            return ['Water', 'Electric', 'Grass', 'Ground']
        if t == 'Ice':
            return ['Ice']
        if t == 'Fighting':
            return ['Bug', 'Rock', 'Dark']
        if t == 'Poison':
            return ['Grass', 'Fighting', 'Poison', 'Bug', 'Fairy']
        if t == 'Ground':
            return ['Poison', 'Rock']
        if t == 'Flying':
            return ['Grass', 'Fighting', 'Bug']
        if t == 'Psychic':
            return ['Fighting', 'Psychic']
        if t == 'Bug':
            return ['Grass', 'Fighting', 'Ground']
        if t == 'Rock':
            return ['Normal', 'Fire', 'Poison', 'Flying']
        if t == 'Ghost':
            return ['Poison', 'Bug']
        if t == 'Dragon':
            return ['Fire', 'Water', 'Electric', 'Grass']
        if t == 'Dark':
            return ['Ghost', 'Dark']
        if t == 'Steel':
            return ['Normal', 'Grass', 'Ice', 'Flying', 'Psychic', 'Bug', 'Rock', 'Dragon', 'Steel', 'Fairy']
        if t == 'Fairy':
            return ['Fighting', 'Bug', 'Dark']
        print(f'Error: Unknown type "{t}"!')

    def get_immunities(self, t):
        if t == 'Normal':
            return ['Ghost']
        if t == 'Fire':
            return []
        if t == 'Water':
            return []
        if t == 'Electric':
            return []
        if t == 'Grass':
            return []
        if t == 'Ice':
            return []
        if t == 'Fighting':
            return []
        if t == 'Poison':
            return []
        if t == 'Ground':
            return ['Electric']
        if t == 'Flying':
            return ['Ground']
        if t == 'Psychic':
            return []
        if t == 'Bug':
            return []
        if t == 'Rock':
            return []
        if t == 'Ghost':
            return ['Normal', 'Fighting']
        if t == 'Dragon':
            return []
        if t == 'Dark':
            return ['Psychic']
        if t == 'Steel':
            return ['Poison']
        if t == 'Fairy':
            return ['Dragon']
        print(f'Error: Unknown type "{t}"!')

    def get_type_damage(self, defense_type, abilities=None, one_type=False):
        damage = dict()
        if abilities is None or len(abilities) > 1:
            abilities = []
        for attack_type in self.get_types():
            damage[attack_type] = 0 if 'wonderguard' in abilities and one_type else 1
            if attack_type in self.get_weaknesses(defense_type):
                damage[attack_type] = 2
            if attack_type in self.get_resistances(defense_type):
                if 'wonderguard' in abilities:
                    damage[attack_type] = 0
                else:
                    damage[attack_type] = 0.5
            if attack_type in self.get_immunities(defense_type):
                damage[attack_type] = 0
            if attack_type == 'Ground' and 'levitate' in abilities:
                damage[attack_type] = 0
            if attack_type == 'Water':
                if 'dryskin' in abilities or 'waterabsorb' in abilities or 'stormdrain' in abilities:
                    damage[attack_type] = 0
            if attack_type == 'Fire':
                if 'flashfire' in abilities:
                    damage[attack_type] = 0
                if 'heatproof' in abilities or 'thickfat' in abilities or 'waterbubble' in abilities:
                    damage[attack_type] = damage[attack_type] * 0.5
                if 'fluffy' in abilities:
                    damage[attack_type] = damage[attack_type] * 2
            if attack_type == 'Electric':
                if 'voltabsorb' in abilities or 'motordrive' in abilities or 'lightningrod' in abilities:
                    damage[attack_type] = 0
            if attack_type == 'Grass':
                if 'sapsipper' in abilities:
                    damage[attack_type] = 0
            if attack_type == 'Ice':
                if 'thickfat' in abilities:
                    damage[attack_type] = damage[attack_type] * 0.5
        return damage

    def get_damage_modifiers(self, types, abilities=None):
        if abilities is None or len(abilities) > 1:
            abilities = []
        if len(types) == 1:
            return self.get_type_damage(types[0], abilities, one_type=True)
        if len(types) == 2:
            total_damage = dict()
            type1_damage = self.get_type_damage(types[0], abilities)
            type2_damage = self.get_type_damage(types[1], abilities)
            for t in type1_damage:
                total_damage[t] = type1_damage[t] * type2_damage[t]
                if 'wonderguard' in abilities and total_damage[t] <= 1:
                    total_damage[t] = 0
            return total_damage
        else:
            print('Error: Invalid number of types!')
            return None

    def get_defensive_ability_dict(self):
        return {
            'levitate': 'Levitate',
            'wonderguard': 'Wonder Guard',
            'bulletproof': 'Bulletproof',
            'disguise': 'Disguise',
            'dryskin': 'Dry Skin',
            'filter': 'Filter',
            'flashfire': 'Flash Fire',
            'fluffy': 'Fluffy',
            'friendguard': 'Friend Guard',
            'heatproof': 'Heatproof',
            'iceface': 'Ice Face',
            'lightningrod': 'Lightning Rod',
            'motordrive': 'Motor Drive',
            'multiscale': 'Multiscale',
            'prismarmor': 'Prism Armor',
            'punkrock': 'Punk Rock',
            'sapsipper': 'Sap Sipper',
            'shadowshield': 'Shadow Shield',
            'solidrock': 'Solid Rock',
            'soundproof': 'Soundproof',
            'stormdrain': 'Storm Drain',
            'thickfat': 'Thick Fat',
            'voltabsorb': 'Volt Absorb',
            'waterabsorb': 'Water Absorb',
            'waterbubble': 'Water Bubble'
        }

    def get_type_effectiveness_ability_dict(self):
        return {
            'levitate': 'Levitate',
            'wonderguard': 'Wonder Guard',
            'dryskin': 'Dry Skin',
            'flashfire': 'Flash Fire',
            'fluffy': 'Fluffy',
            'heatproof': 'Heatproof',
            'lightningrod': 'Lightning Rod',
            'motordrive': 'Motor Drive',
            'sapsipper': 'Sap Sipper',
            'stormdrain': 'Storm Drain',
            'thickfat': 'Thick Fat',
            'voltabsorb': 'Volt Absorb',
            'waterabsorb': 'Water Absorb',
            'waterbubble': 'Water Bubble'
        }

    def get_offensive_ability_dict(self):
        return {
            'adaptability': 'Adaptability',
            'aerilate': 'Aerilate',
            'galvanize': 'Galvanize',
            'ironfist': 'Iron Fist',
            'megalauncher': 'Mega Launcher',
            'normalize': 'Normalize',
            'pixilate': 'Pixilate',
            'punkrock': 'Punk Rock',
            'reckless': 'Reckless',
            'refrigerate': 'Refrigerate',
            'sheerforce': 'Sheer Force',
            'steelworker': 'Steelworker',
            'steelyspirit': 'Steely Spirit',
            'strongjaw': 'Strong Jaw',
            'technician': 'Technician',
            'toughclaws': 'Tough Claws',
            'waterbubble': 'Water Bubble',
            'skilllink': 'Skill Link',
            'libero': 'Libero',
            'protean': 'Protean',
            'hustle': 'Hustle',
            'hugepower': 'Huge Power',
            'purepower': 'Pure Power',
            'darkaura': 'Dark Aura',
            'fairyaura': 'Fairy Aura',
            'liquidvoice': 'Liquid Voice'
        }