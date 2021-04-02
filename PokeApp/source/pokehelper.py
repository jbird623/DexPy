import random

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

    def get_colors(self):
        return [
            'Red',
            'Brown',
            'Yellow',
            'Green',
            'Blue',
            'Purple',
            'Pink',
            'White',
            'Gray',
            'Black'
        ]

    def get_egg_groups(self):
        return [
            'bug',
            'flying',
            'grass',
            'water1',
            'water2',
            'water3',
            'field',
            'fairy',
            'mineral',
            'human-like',
            'amorphous',
            'monster',
            'ditto',
            'dragon',
            'undiscovered'          
        ]

    def get_move_flags(self):
        return [
            'heal',
            'protect',
            'contact',
            'bullet',
            'reflectable',
            'pulse',
            'bite',
            'recharge',
            'sound',
            'charge',
            'gravity',
            'punch',
            'defrost',
            'powder'
        ]

    def get_stats(self):
        return {
            'hp':'HP',
            'atk':'Attack',
            'def':'Defense',
            'spa':'Sp. Atk',
            'spd':'Sp. Def',
            'spe':'Speed',
            'bst':'Base Stat Total'
        }

    def get_boost_stats(self):
        return {
            'atk':'Attack',
            'def':'Defense',
            'spa':'Sp. Atk',
            'spd':'Sp. Def',
            'spe':'Speed',
            'eva':'Evasion',
            'acc':'Accuracy'
        }

    def get_nature_stats(self):
        return {
            'atk':'Attack',
            'def':'Defense',
            'spa':'Sp. Atk',
            'spd':'Sp. Def',
            'spe':'Speed'
        }

    def get_nature_name(self, up, down):
        if up == 'atk':
            if down == 'atk':
                return 'Hardy'
            elif down == 'def':
                return 'Lonely'
            elif down == 'spa':
                return 'Adamant'
            elif down == 'spd':
                return 'Naughty'
            elif down == 'spe':
                return 'Brave'
        elif up == 'def':
            if down == 'atk':
                return 'Bold'
            elif down == 'def':
                return 'Docile'
            elif down == 'spa':
                return 'Impish'
            elif down == 'spd':
                return 'Lax'
            elif down == 'spe':
                return 'Relaxed'
        elif up == 'spa':
            if down == 'atk':
                return 'Modest'
            elif down == 'def':
                return 'Mild'
            elif down == 'spa':
                return 'Bashful'
            elif down == 'spd':
                return 'Rash'
            elif down == 'spe':
                return 'Quiet'
        elif up == 'spd':
            if down == 'atk':
                return 'Calm'
            elif down == 'def':
                return 'Gentle'
            elif down == 'spa':
                return 'Careful'
            elif down == 'spd':
                return 'Quirky'
            elif down == 'spe':
                return 'Sassy'
        elif up == 'spe':
            if down == 'atk':
                return 'Timid'
            elif down == 'def':
                return 'Hasty'
            elif down == 'spa':
                return 'Jolly'
            elif down == 'spd':
                return 'Naive'
            elif down == 'spe':
                return 'Serious'

    def get_neutral_natures(self):
        return [
            'Hardy',
            'Docile',
            'Bashful',
            'Quirky',
            'Serious'
        ]

    def get_nature_stats_map(self):
        return {
            'Hardy': {'up':'atk', 'down':'atk'},
            'Lonely': {'up':'atk', 'down':'def'},
            'Adamant': {'up':'atk', 'down':'spa'},
            'Naughty': {'up':'atk', 'down':'spd'},
            'Brave': {'up':'atk', 'down':'spe'},
            'Bold': {'up':'def', 'down':'atk'},
            'Docile': {'up':'def', 'down':'def'},
            'Impish': {'up':'def', 'down':'spa'},
            'Lax': {'up':'def', 'down':'spd'},
            'Relaxed': {'up':'def', 'down':'spe'},
            'Modest': {'up':'spa', 'down':'atk'},
            'Mild': {'up':'spa', 'down':'def'},
            'Bashful': {'up':'spa', 'down':'spa'},
            'Rash': {'up':'spa', 'down':'spd'},
            'Quiet': {'up':'spa', 'down':'spe'},
            'Calm': {'up':'spd', 'down':'atk'},
            'Gentle': {'up':'spd', 'down':'def'},
            'Careful': {'up':'spd', 'down':'spa'},
            'Quirky': {'up':'spd', 'down':'spd'},
            'Sassy': {'up':'spd', 'down':'spe'},
            'Timid': {'up':'spe', 'down':'atk'},
            'Hasty': {'up':'spe', 'down':'def'},
            'Jolly': {'up':'spe', 'down':'spa'},
            'Naive': {'up':'spe', 'down':'spd'},
            'Serious': {'up':'spe', 'down':'spe'}
        }

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
    
    def get_stat_evaluation(self, stats):
        tags = []
        good_modifiers = [
            'Extremely',
            'Extraordinarily',
            'Excessively',
            'Incredibly',
            'Absurdly',
            'Remarkably',
            'Decidedly',
            'Considerably',
            'Noticeably',
            'Strikingly',
            'Startlingly',
            'Abnormally',
            'Amazingly',
            'Ludicrously',
            'Preposterously'
        ]
        bad_modifiers = [
            'Extraordinarily',
            'Excessively',
            'Absurdly',
            'Remarkably',
            'Strikingly',
            'Startlingly',
            'Laughably',
            'Comically',
            'Insanely',
            'Foolishly',
            'Ludicrously',
            'Preposterously',
            'Pathetically',
            'Miserably',
            'Lamentably',
            'Pitifully',
            'Woefully'
        ]
        random.shuffle(good_modifiers)
        random.shuffle(bad_modifiers)
        HP = int(stats['hp'])
        Atk = int(stats['atk'])
        Def = int(stats['def'])
        SpA = int(stats['spa'])
        SpD = int(stats['spd'])
        Spe = int(stats['spe'])
        BST = int(stats['bst'])
        Physical = int((Atk + Def) / 2)
        Special = int((SpA + SpD) / 2)
        Offensive = int((Atk + SpA) / 2)
        Defensive = int((Def + SpD) / 2)
        Average = int((HP + Atk + Def + SpA + SpD + Spe) / 6)
        maxOffense = max(Atk, SpA)
        maxDefense = max(Def, SpD)
        if abs(HP - Average) > 0.15 * Average and HP > Average:
            if HP >= 120:
                tags.append(good_modifiers.pop())
            tags.append('Bulky')
        if abs(Spe - Average) > 0.15 * Average and Spe > Average:
            if 'Bulky' in tags:
                tags.append('and')
            if Spe >= 120:
                tags.append(good_modifiers.pop())
            tags.append('Speedy')
        if abs(Spe - Average) > 0.15 * Average and Spe < Average:
            if 'Bulky' in tags or 'Speedy' in tags:
                tags.append('but')
            if Spe <= 30:
                tags.append(bad_modifiers.pop())
            tags.append('Slow')
        if abs(HP - Average) > 0.15 * Average and HP < Average:
            if 'Slow' in tags:
                tags[-1] = 'Slow,'
            elif 'Speedy' in tags:
                tags.append('but')
            if HP <= 30:
                tags.append(bad_modifiers.pop())
            tags.append('Low-Stamina')
        if BST >= 450:
            if abs(Physical - Special) > 0.1 * ((Physical + Special) / 2):
                if Physical > Special:
                    tags.append('Physical')
                if Special > Physical:
                    tags.append('Special')
            else:
                tags.append('Mixed')
            if abs(Offensive - Defensive) > 0.15 * ((Offensive + Defensive) / 2):
                if Offensive > Defensive:
                    tags.append('Sweeper')
                if Defensive > Offensive:
                    tags.append('Wall')
            elif abs(maxOffense - maxDefense) > 0.15 * ((maxOffense + maxDefense) / 2):
                if maxOffense > maxDefense:
                    tags.append('Sweeper')
                if maxDefense > maxOffense:
                    tags.append('Wall')
            else:
                tags.append('Generalist')
            if 'Sweeper' in tags and 'Wall' in tags:
                tags.remove('Sweeper')
                tags.remove('Wall')
                tags.append('Generalist')
        elif BST >=300:
            tags.append('Mid-Game \'Mon')
        else:
            tags.append('Small Fry')
        assessment = ' '.join(tags)
        if len(tags) == 1:
            if max(HP, Atk, Def, SpA, SpD, Spe) - Average <= 0.15 * Average:
                assessment = f'{bad_modifiers.pop()} Average {tags[0]}'
        if len(tags) == 2 and 'Mixed' in tags and 'Generalist' in tags and BST <= 500:
            assessment = f'{bad_modifiers.pop()} Average'
        if maxOffense >= 120:
            assessment = f'{assessment}; {good_modifiers.pop()} Powerful'
        if maxDefense >= 120:
            assessment = f'{assessment}; {good_modifiers.pop()} Tanky'
        if maxOffense <= 30:
            assessment = f'{assessment}; {bad_modifiers.pop()} Feeble'
        if maxDefense <= 30:
            assessment = f'{assessment}; {bad_modifiers.pop()} Paper-Like in Constitution'
        return assessment

    def get_random_response(self, context_value, additional_responses=None):
        responses = [
            f'Hmmm... Bzzzzrt. How about {context_value}?',
            f'Have you considered {context_value}, perhaps? Seems pretty interesting to me, bzzzzrt!',
            f'I\'ve got one for you, bzzzzrt: {context_value}!',
            f'Considering all of those options, bzzzzrt... Oh, I know! What about {context_value}?',
            f'Selecting one randomly from the list, bzzzzrt... I choose {context_value}!',
            f'Oh, here\'s a good one, I think: {context_value}, bzzzzrt!',
            f'Maybe {context_value}? What do you think, bzzzzrt?',
            f'I spun the wheel, and it landed on {context_value}, bzzzzrt!',
            f'I think {context_value} could be an interesting choice, bzzzzrt!'
        ]
        if additional_responses is not None:
            responses.extend(additional_responses)
        random_choice = random.choice(responses)
        return random_choice

    def do_random_type_function(self, print_to):
        print(f'Allow me to select a random type for you, bzzzzrt...', file=print_to)
        random_type = random.choice(self.get_types())
        random_response = self.get_random_response(random_type, additional_responses=[
            f'I\'ve always thought that {random_type}-type pokemon were cool, bzzzrt!',
            f'I\'ve always thought that the {random_type} type had some interesting moves, bzzzrt!'
        ])
        if random_type.lower() == 'ghost' or random_type.lower() == 'electric':
            random_response = f'Oh, how about {random_type}? (I promise this was chosen randomly and is not biased, bzzzzrt!)'
        print(random_response, file=print_to)

    def do_random_color_function(self, print_to):
        print(f'Allow me to select a random color for you, bzzzzrt...', file=print_to)
        random_color = random.choice(self.get_colors())
        random_response = self.get_random_response(random_color, additional_responses=[
            f'I\'ve always been fond of the color {random_color}! How about that one, bzzzzrt?'
        ])
        if random_color.lower() == 'red':
            random_response = f'Oh, what about {random_color}? That one is my favorite!'
        print(random_response, file=print_to)

    def do_get_nature_stats_function(self, nature, print_to):
        nature = nature.lower().capitalize()
        nature_dict = self.get_nature_stats_map()
        stats_dict = self.get_nature_stats()

        if nature not in nature_dict:
            print(f'Error: Unrecognized nature "{nature}", bzzzzrt!', file=print_to)
            return
        else:
            nature_obj = nature_dict[nature]
            up = stats_dict[nature_obj['up']]
            down = stats_dict[nature_obj['down']]
            if nature in self.get_neutral_natures():
                print(f'A pokemon with the {nature} nature will have its {up} both increased and decreased, resulting in a net zero change, bzzzzrt!', file=print_to)
            else:
                print(f'A pokemon with the {nature} nature will have its {up} increased and its {down} decreased, bzzzzrt!', file=print_to)

    def do_get_nature_name_function(self, up, down, print_to):
        up = up.lower()
        down = down.lower()
        stats_dict = self.get_nature_stats()

        if up == 'hp' or down == 'hp':
            print(f'There are no natures that affect the HP stat, bzzzzrt!')
            return

        if up == 'bst' or down == 'bst':
            print(f'Natures do not affect the Base Stat Total of a pokemon, bzzzzrt!')
            return

        if up not in stats_dict:
            print(f'Error: Unkown stat "{up}", bzzzzrt! Please use one of the following: atk, def, spa, spd, spe', file=print_to)
            return
        elif down not in stats_dict:
            print(f'Error: Unkown stat "{down}", bzzzzrt! Please use one of the following: atk, def, spa, spd, spe', file=print_to)
            return
        else:
            nature = self.get_nature_name(up, down)
            up_stat = stats_dict[up]
            down_stat = stats_dict[down]
            print(f'If you want your pokemon to have an increased {up_stat} and decreased {down_stat}, it should have the {nature} nature, bzzzzrt!', file=print_to)
