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

    def get_type_damage(self, defense_type):
        damage = dict()
        for attack_type in self.get_types():
            damage[attack_type] = 1
            if attack_type in self.get_weaknesses(defense_type):
                damage[attack_type] = 2
            if attack_type in self.get_resistances(defense_type):
                damage[attack_type] = 0.5
            if attack_type in self.get_immunities(defense_type):
                damage[attack_type] = 0
        return damage

    def get_damage_modifiers(self, types):
        if len(types) == 1:
            return self.get_type_damage(types[0])
        if len(types) == 2:
            total_damage = dict()
            type1_damage = self.get_type_damage(types[0])
            type2_damage = self.get_type_damage(types[1])
            for t in type1_damage:
                total_damage[t] = type1_damage[t] * type2_damage[t]
            return total_damage
        else:
            print('Error: Invalid number of types!')
            return None
