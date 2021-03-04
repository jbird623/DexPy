#invite link: https://discordapp.com/oauth2/authorize?client_id=675234599504445441&scope=bot&permissions=3072
#beta invite link: https://discordapp.com/oauth2/authorize?client_id=811346201072762960&scope=bot&permissions=3072

from discord.ext import commands
from discord.embeds import Embed
from source.abilitydex import AbilityDex
from source.movedex import MoveDex
from source.pokedex import PokeDex
from source.pokehelper import PokemonHelper
from source.breedingbox import BreedingBox
from source.pokewrap import PokeMongo8
from pprint import pprint

import sys

prefix = '!'
bot = commands.Bot(command_prefix=prefix)

bot.remove_command('help')

beta = False
pokemongo = PokeMongo8()

if len(sys.argv) > 1 and sys.argv[1] == '--beta':
    beta = True
    pokemongo = PokeMongo8(beta=True)

class MessageHelper:
    def __init__(self):
        self.message = ''

    def write(self, str):
        self.message += str

    async def send(self, ctx, bookend=None, embed=None):
        if bookend is None:
            bookend = '```'
        message_lines = self.message.split('\n')
        message = ''
        while len(message_lines) > 0:
            new_message = message + f'\n{message_lines[0]}'
            if len(new_message) >= 1990:
                await ctx.send(f'{bookend}{message}{bookend}')
                message = ''
            message = message + f'\n{message_lines[0]}'
            message_lines.pop(0)
        await ctx.send(f'{bookend}{message}{bookend}', embed=embed)

def is_int(n):
    if not is_not_bool(n):
        return False
    if n == True:
        return False
    if n == False:
        return False
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

def is_not_bool(s):
    return s not in ['True', 'False']

def is_filter_shaped(s):
    return ':' in s or '>' in s or '<' in s

def split_filter(s):
    for i in range(len(s)):
        if s[i] == ':' or s[i] == '>' or s[i] == '<':
            if s[i] == ':':
                return [s[:i], s[i+1:]]
            else:
                return [s[:i], s[i:]]
    return s

def parse_arguments(arguments, positional_args=[], optional_pos_args=[], params=False):
    arguments = list(arguments)

    pos = dict()
    opt = dict()
    fil = dict()
    par = []

    for arg in arguments:
        if len(positional_args) > 0:
            pos[positional_args[0]] = arg
            positional_args.pop(0)

        elif arg[0] == '-':
            if '=' in arg:
                split_opt = arg.split('=')
                if len(split_opt) < 2:
                    opt[split_opt[0]] = ''
                else:
                    opt[split_opt[0]] = split_opt[1]
            else:
                opt[arg] = True
        
        elif is_filter_shaped(arg):
            s_filter = split_filter(arg)
            fil = pokemongo.add_filter(fil, {s_filter[0]: s_filter[1]})

        elif len(optional_pos_args) > 0:
            pos[optional_pos_args[0]] = arg
            optional_pos_args.pop(0)

        elif params:
            par.append(arg)

    if len(positional_args) > 0:
        return None

    return {'pos':pos, 'opt':opt, 'fil':fil, 'par':par}

def get_option(options, full_opt, short_opt=None):
    if short_opt is None:
        short_opt = full_opt[0]
    return f'--{full_opt}' in options or f'-{short_opt}' in options

def get_option_int_value(options, full_opt, short_opt=None, default=None):
    if f'--{full_opt}' in options:
        if is_int(options[f'--{full_opt}']):
            return int(options[f'--{full_opt}'])
        else:
            return default

    if short_opt is None:
        short_opt = full_opt[0]

    if f'-{short_opt}' in options:
        if is_int(options[f'-{short_opt}']):
            return int(options[f'-{short_opt}'])
        else:
            return default

    return None

def get_option_string_value(options, full_opt, short_opt=None, default=None):
    if f'--{full_opt}' in options:
        if is_not_bool(options[f'--{full_opt}']):
            return options[f'--{full_opt}']
        else:
            return default

    if short_opt is None:
        short_opt = full_opt[0]

    if f'-{short_opt}' in options:
        if is_not_bool(options[f'-{short_opt}']):
            return options[f'-{short_opt}']
        else:
            return default

    return None

@bot.event
async def on_ready():
    if beta:
        print("\nDexPy running in developer mode, bzzzzrt!\n")
    else:
        print("\nDexPy ready to receive commands, bzzzzrt!\n")

#@bot.event
#async def on_message(message):
#    print("Message received, bzzzzzzrt! Here's the message:\n", message.content)

@bot.command(aliases=['h'])
async def help(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nHELP command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')

    output = MessageHelper()
    
    '''
    print('Available DexPy Commands:', file=output)
    print('', file=output)
    print('  Basic Commands:', file=output)
    print('  - !(help|h)                                     Shows a list of commands.', file=output)
    print('  - !(pokedex|p) (POKEMON) [-v|--verbose]         Show the raw pokedex entry for POKEMON.', file=output)
    print('                                                  If -v is used, shows additional information.', file=output)
    print('  - !(hiddenAbility|ha) (POKEMON)                 Show the hidden ability for POKEMON.', file=output)
    print('  - !(ability|a) (ABILITY) [-p <filter>]          Show the information about ABILITY.', file=output)
    print('                                                  Also lists all pokemon that can have ABILITY if -p is used.', file=output)
    print('                                                  If -p is used, accepts pokemon query filters (excluding "a").', file=output)
    print('  - !(move|m) (MOVE) [-p <filter>]                Show the information about MOVE.', file=output)
    print('                                                  Also lists all pokemon that can learn MOVE if -p is used.', file=output)
    print('                                                  If -p is used, accepts pokemon query filters.', file=output)
    print('  - !(damage|d) (POKEMON)                         Get the weaknesses/resistances for POKEMON.', file=output)
    print('  - !(damage|d) (TYPE1) [TYPE2]                   Get the weaknesses/resistances of the given type(s).', file=output)
    print('                                                  Add -a=ABILITY to use that ability for calculations.', file=output)
    print('', file=output)
    print('  Movesets:', file=output)
    print('  - !(moveset|ms) (POKEMON) <filter>              Show the moves that POKEMON can learn.', file=output)
    print('                                                  Accepts move query filters.', file=output)
    print('    Options:', file=output)
    print('     -s=X, --stab=X                               Show the top X STAB moves for POKEMON (default 5).', file=output)
    print('     -c=X, --coverage=X                           Show the top X coverage moves for POKEMON (default 3).', file=output)
    print('     -i, --ignore-stats                           Ignore stats when calculating top moves.', file=output)
    print('     -t, --transfer                               Include transfer-only moves.', file=output)
    print('     -p, --past                                   Include moves that are only available in past games.', file=output)
    print('     -atk=X                                       Override Attack stat for move power calculations.', file=output)
    print('     -spa=X                                       Override Sp. Attack stat for move power calculations.', file=output)
    print('     -def=X                                       Override Defense stat for move power calculations.', file=output)
    print('     -acc, --accuracy                             Include accuracy in move power calculations.', file=output)
    print('     -a=ABILITY                                   Calculate move power as though the pokemon had ABILITY.', file=output)
    print('', file=output)
    print('  Breeding:', file=output)
    print('  - !(eggGroup|eg) (EGG_GROUP) <filter>           Lists all evolutionary lines in EGG_GROUP.', file=output)
    print('                                                  Accepts pokemon query filters (excluding "eg").', file=output)
    print('  - !(eggMove|em) (POKEMON) [MOVE]                Show potential breeding chains for breeding MOVE onto POKEMON.', file=output)
    print('                                                  If MOVE is not supplied, lists the available egg moves for POKEMON.', file=output)
    #print('  - !(breedingbox|bb) (-r|--register)=POKEMON     Register POKEMON to your breeding box.', file=output)
    #print('                                                  This signifies to other users that you have this \'mon with HA.', file=output)
    #print('  - !(breedingbox|bb) (-u|--unregister)=POKEMON   Unregister POKEMON from your breeding box.', file=output)
    #print('  - !(breedingbox|bb) (-q|--query)=POKEMON        Check to see who has POKEMON with a hidden ability.', file=output)
    #print('                                                  Returns users who have registered a pokemon in the same evolutionary line.', file=output)
    print('', file=output)
    print('  Querying:', file=output)
    print('  - !(queryPokedex|qp) <filter>                   Accepts pokemon query filters.', file=output)
    print('  - !(queryMoves|qm) <filter>                     Accepts move query filters.', file=output)
    print('    Options:', file=output)
    print('      -c, --count                                 Show the total number of entries that fit this query instead of a list.', file=output)
    print('      -f, --force-list                            Force the entire list to be printed even if it\'s more than 50 entries.', file=output)
    print('', file=output)
    print('', file=output)
    print('Available Query Filters:', file=output)
    print('  Pokemon Filters:', file=output)
    print('  - m:<moves>                     Filter by pokemon that can learn all of the specified moves.', file=output)
    print('                                  Accepts a single move or a comma-separated list.', file=output)
    print('  - ml:<moves>                    Filter by pokemon that can learn all of the specified moves via level up.', file=output)
    print('                                  Accepts a single move or a comma-separated list.', file=output)
    print('  - mm:<moves>                    Filter by pokemon that can learn all of the specified moves via TM/TR.', file=output)
    print('                                  Accepts a single move or a comma-separated list.', file=output)
    print('  - mb:<moves>                    Filter by pokemon that can learn all of the specified moves via breeding.', file=output)
    print('                                  Accepts a single move or a comma-separated list.', file=output)
    print('  - mt:<moves>                    Filter by pokemon that can learn all of the specified moves via tutor.', file=output)
    print('                                  Accepts a single move or a comma-separated list.', file=output)
    print('  - mtr:<moves>                   Filter by pokemon that can only know all of the specified moves via transfer.', file=output)
    print('                                  Accepts a single move or a comma-separated list.', file=output)
    print('  - a:<abilities>                 Filter by pokemon that can have any of the abilities specified.', file=output)
    print('                                  Accepts a single ability or a comma-separated list.', file=output)
    print('  - t:<types>                     Filter by pokemon that have any of the types specified.', file=output)
    print('                                  Accepts a single type or a comma-separated list.', file=output)
    print('  - ta:<types>                    Filter by pokemon that have exactly the types specified.', file=output)
    print('                                  Accepts a single type or a comma-separated list.', file=output)
    print('  - evo:<bool>                    Filter by pokemon that can evolve (true) or can\'t evolve (false).', file=output)
    print('  - prevo:<bool>                  Filter by pokemon that have a pre-evolution (true) or do not (false).', file=output)
    print('  - eg:<eggGroup>                 Filter by pokemon in any of the specified egg groups.', file=output)
    print('                                  Accepts a single egg group or a comma-separated list.', file=output)
    print('  - ega:<eggGroup>                Filter by pokemon in exactly the specified egg groups.', file=output)
    print('                                  Accepts a single egg group or a comma-separated list.', file=output)
    print('  - tr:<bool>                     Filter by pokemon that are only obtainable via transfer.', file=output)
    print('  - base:<bool>                   Filter by pokemon that are only obtainable in the base game.', file=output)
    print('  - ioa:<bool>                    Filter by pokemon that are only obtainable on the Isle of Armor.', file=output)
    print('  - ct:<bool>                     Filter by pokemon that are only obtainable in the Crown Tundra.', file=output)
    print('  - past:<bool>                   Filter by pokemon that are only available prior to Gen 8.', file=output)
    print('    Stat Filters:                 All the following filters can also be compared via >, <, >=, or <=.', file=output)
    print('                                  The stats can be compared to int values and/or each other.', file=output)
    print('    - hp:<value>                  Filter by HP stat.', file=output)
    print('    - atk:<value>                 Filter by Attack stat.', file=output)
    print('    - def:<value>                 Filter by Defense stat.', file=output)
    print('    - spa:<value>                 Filter by Sp. Attack stat.', file=output)
    print('    - spd:<value>                 Filter by Sp. Defense stat.', file=output)
    print('    - spe:<value>                 Filter by Speed stat.', file=output)
    print('    - bst:<value>                 Filter by base stat total.', file=output)
    print('    Sorting:                      Sort query results by various stats. Negate to reverse order.', file=output)
    print('    - o:<stat>                    Sort by stat. Defaults to descending.', file=output)
    print('                                  Accepts any of the following values:', file=output)
    print('                                  hp, atk, def, spa, spd, spe, bst', file=output)
    print('    - o:num                       Sort by pokedex number. Defaults to ascending.', file=output)
    print('    - o:w, o:weight               Sort by weight. Defaults to descending.', file=output)
    print('    - o:h, o:height               Sort by height. Defaults to descending.', file=output)
    print('', file=output)
    print('  Move Filters:', file=output)
    print('  - pow:<value>                   Filter by base power. Can use >, <, >=, or <=.', file=output)
    print('  - acc:<value>                   Filter by accuracy. Can use >, <, >=, or <=.', file=output)
    print('  - c:<category>                  Filter by status, special, or physical.', file=output)
    print('                                  Accepts a single category or a comma-separated list.', file=output)
    print('  - t:<types>                     Filter by moves that are any of the specified types.', file=output)
    print('                                  Accepts a single type or a comma-separated list.', file=output)
    print('  - m:<moves>                     Filter by move names. Accepts a single move or a comma-separated list.', file=output)
    print('  - sec:<bool>                    Filter by moves that have (true) or don\'t have (false) secondary effects.', file=output)
    print('  - bite:<bool>                   Filter by moves that are/aren\'t affected by Strong Jaw.', file=output)
    print('  - con:<bool>                    Filter by moves that do/don\'t make contact.', file=output)
    print('  - snd:<bool>                    Filter by moves that are/aren\'t sound-based.', file=output)
    print('  - pnch:<bool>                   Filter by moves that are/aren\'t punch moves.', file=output)
    print('  - p:<value>                     Filter by move priority. Can use >, <, >=, or <=.', file=output)
    print('    Sorting:                      Sort query results by various stats. Negate to reverse order.', file=output)
    print('    - o:pow                       Sort by base power. Defaults to descending.', file=output)
    print('    - o:acc                       Sort by accuracy. Defaults to descending.', file=output)
    print('    - o:c, o:cat                  Sort by category. Defaults to descending.', file=output)
    print('    - o:p, o:prio                 Sort by priority. Defaults to descending.', file=output)
    print('    - o:pp                        Sort by power points. Defaults to descending.', file=output)
    print('    - o:num                       Sort by movedex number. Defaults to ascending.', file=output)
    print('', file=output)
    '''

    embed = Embed()
    embed.description = "User Docs can be found [here](https://docs.google.com/document/d/1dOJt6_xodsqWOFJPI2AY91mNmnrjLDyy7cRLki7G8qo/edit?usp=sharing)!"

    args = parse_arguments(raw_args)
    if args is None:
        print('Error parsing command, bzzzzrt!', file=output)
        await output.send(ctx)
        return
    
    force_channel = get_option(args['opt'], 'force-channel')

    await output.send(ctx if force_channel else ctx.author, '', embed)

@bot.command(aliases=['ms'])
async def moveset(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nMOVESET command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

    pos_args = ['pokemon']

    args = parse_arguments(raw_args, pos_args)
    if args is None:
        print('Error parsing command, bzzzzrt! Type "!help" for usage details.', file=output)
        await output.send(ctx)
        return

    pokemon = args['pos']['pokemon'].lower().replace(' ','')

    show_stab = get_option(args['opt'], 'stab')
    max_stab = get_option_int_value(args['opt'], 'stab', default=5)
    show_coverage = get_option(args['opt'], 'coverage')
    max_coverage = get_option_int_value(args['opt'], 'coverage', default=3)
    ignore_stats = get_option(args['opt'], 'ignore-stats')
    show_transfers = get_option(args['opt'], 'transfer')
    show_past = get_option(args['opt'], 'past')
    atk_override = get_option_int_value(args['opt'], 'atk', 'atk')
    spa_override = get_option_int_value(args['opt'], 'spa', 'spa')
    def_override = get_option_int_value(args['opt'], 'def', 'def')
    accuracy_check = get_option(args['opt'], 'accuracy', 'acc')
    ability = get_option_string_value(args['opt'], 'ability')

    if not show_stab and not show_coverage:
        ignore_stats = True

    filters = pokemongo.add_user_move_filters(args['fil'], ctx.author.id)

    pokemongo.print_filters(filters[1], output)
    MoveDex(pokemongo).do_moves_function(pokemon, filters[0], show_stab, max_stab, ignore_stats, show_coverage, max_coverage,
                                show_transfers, show_past, atk_override, spa_override, def_override, accuracy_check, ability, output)

    await output.send(ctx)

@bot.command(aliases=['em','eggmove'])
async def eggMove(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nEGGMOVE command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

    pos_args = ['pokemon']
    opt_pos_args = ['move']

    args = parse_arguments(raw_args, pos_args, opt_pos_args)
    if args is None:
        print('Error parsing command, bzzzzrt! Type "!help" for usage details.', file=output)
        await output.send(ctx)
        return

    pokemon = args['pos']['pokemon'].lower().replace(' ','')
    if 'move' in args['pos']:
        move = args['pos']['move'].lower().replace(' ','')
    else:
        move = None

    MoveDex(pokemongo).do_egg_moves_function(pokemon, move, output)

    await output.send(ctx)

@bot.command(aliases=['p'])
async def pokedex(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nPOKEDEX command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

    pos_args = ['pokemon']

    args = parse_arguments(raw_args, pos_args)
    if args is None:
        print('Error parsing command, bzzzzrt! Type "!help" for usage details.', file=output)
        await output.send(ctx)
        return

    pokemon = args['pos']['pokemon'].lower().replace(' ','')
    
    verbose = get_option(args['opt'], 'verbose')
    
    PokeDex(pokemongo).do_pokedex_function(pokemon, verbose, output)

    await output.send(ctx)

@bot.command(aliases=['ha','hiddenability'])
async def hiddenAbility(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nHIDDENABILITY command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

    pos_args = ['pokemon']

    args = parse_arguments(raw_args, pos_args)
    if args is None:
        print('Error parsing command, bzzzzrt! Type "!help" for usage details.', file=output)
        await output.send(ctx)
        return

    pokemon = args['pos']['pokemon'].lower().replace(' ','')

    PokeDex(pokemongo).do_hidden_ability_function(pokemon, output)

    await output.send(ctx)

@bot.command(aliases=['a'])
async def ability(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nABILITY command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

    pos_args = ['ability']

    args = parse_arguments(raw_args, pos_args)
    if args is None:
        print('Error parsing command, bzzzzrt! Type "!help" for usage details.', file=output)
        await output.send(ctx)
        return

    ability = args['pos']['ability'].lower().replace(' ','')

    show_list = get_option(args['opt'], 'pokemon')

    filters = pokemongo.add_user_pokemon_filters(args['fil'], ctx.author.id)

    if show_list:
        pokemongo.print_filters(filters[1], output)
    AbilityDex(pokemongo).do_ability_search_function(ability, show_list, filters[0], output)

    await output.send(ctx)

@bot.command(aliases=['m'])
async def move(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nMOVE command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

    pos_args = ['move']

    args = parse_arguments(raw_args, pos_args)
    if args is None:
        print('Error parsing command, bzzzzrt! Type "!help" for usage details.', file=output)
        await output.send(ctx)
        return

    move = args['pos']['move'].lower().replace(' ','')

    show_list = get_option(args['opt'], 'pokemon')

    filters = pokemongo.add_user_pokemon_filters(args['fil'], ctx.author.id)

    if show_list:
        pokemongo.print_filters(filters[1], output)
    MoveDex(pokemongo).do_move_search_function(move, show_list, filters[0], output)

    await output.send(ctx)

@bot.command(aliases=['d'])
async def damage(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nDAMAGE command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

    pos_args = ['token']
    opt_pos_args = ['type2']

    args = parse_arguments(raw_args, pos_args, opt_pos_args)
    if args is None:
        print('Error parsing command, bzzzzrt! Type "!help" for usage details.', file=output)
        await output.send(ctx)
        return

    token = args['pos']['token'].lower().replace(' ','').capitalize()
    if token in PokemonHelper().get_types():
        type1 = token
        pokemon = None
    else:
        pokemon = token.lower()
        type1 = None

    if 'type2' in args['pos']:
        type2 = args['pos']['type2'].lower().replace(' ','').capitalize()
    else:
        type2 = None

    abilities = None
    ability = get_option_string_value(args['opt'], 'ability')
    if ability is not None:
        abilities = [ability]
    
    if pokemon:
        PokeDex(pokemongo).do_pokemon_damage_function(pokemon, output, abilities)
    else:
        if type2:
            PokeDex(pokemongo).do_types_damage_function([type1, type2], output, False, abilities)
        else:
            PokeDex(pokemongo).do_type_damage_function(type1, output, abilities)

    await output.send(ctx)

@bot.command(aliases=['c'])
async def coverage(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nCOVERAGE command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

    pos_args = ['type1']

    args = parse_arguments(raw_args, pos_args, params=True)
    if args is None:
        print('Error parsing command, bzzzzrt! Type "!help" for usage details.', file=output)
        await output.send(ctx)
        return

    types = []
    type1 = args['pos']['type1'].lower().replace(' ','').capitalize()
    if ',' in type1:
        types = type1.split(',')
        for i in range(len(types)):
            types[i] = types[i].lower().replace(' ','').capitalize()
    else:
        types = [type1]
    for param in args['par']:
        types.append(param.lower().replace(' ','').capitalize())

    filters = pokemongo.add_user_pokemon_filters(args['fil'], ctx.author.id)

    pokemongo.print_filters(filters[1], output)
    PokeDex(pokemongo).do_coverage_calculator_function(types, filters[0], output)

    await output.send(ctx)

@bot.command(aliases=['bb'])
async def breedingbox(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nBREEDINGBOX command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

    # CURRENTLY BREEDING BOX NEEDS GUILD SUPPORT, SO IT'S BEING SHUT OFF FOR NOW
    print('Bzzzzrt! This command is currently being refactored! Sorry for the inconvenience!')
    await output.send(ctx)
    return

    args = parse_arguments(raw_args)
    if args is None:
        print('Error parsing command, bzzzzrt! Type "!help" for usage details.', file=output)
        await output.send(ctx)
        return

    user = ctx.message.author.id
    username = ctx.message.author.name

    register = get_option(args['opt'], 'register')
    if register:
        pokemon = get_option_string_value(args['opt'], 'register')
        if pokemon is None:
            print('Error: No pokemon specified, bzzzzrt!\nUsage: !bb --register=POKEMON', file=output)
            await output.send(ctx)
            return
        pokemon_list = pokemon.split(',')
        for p in pokemon_list:
            BreedingBox(pokemongo).register_ha_mon(user, username, p, output)
        await output.send(ctx)
        return
    
    unregister = get_option(args['opt'], 'unregister')
    if unregister:
        pokemon = get_option_string_value(args['opt'], 'unregister')
        if pokemon is None:
            print('Error: No pokemon specified, bzzzzrt!\nUsage: !bb --unregister=POKEMON', file=output)
            await output.send(ctx)
            return
        pokemon_list = pokemon.split(',')
        for p in pokemon_list:
            BreedingBox(pokemongo).unregister_ha_mon(user, username, p, output)
        await output.send(ctx)
        return
    
    query = get_option(args['opt'], 'query')
    if query:
        pokemon = get_option_string_value(args['opt'], 'query')
        if pokemon is None:
            print('Error: No pokemon specified, bzzzzrt!\nUsage: !bb --query=POKEMON', file=output)
            await output.send(ctx)
            return
        pokemon_list = pokemon.split(',')
        for p in pokemon_list:
            BreedingBox(pokemongo).query_ha_mon(user, p, output)
        await output.send(ctx)
        return

    print(f'Error: Unknown breeding box subcommand, bzzzzrt! Type "!help" for usage details.', file=output)

    await output.send(ctx)

@bot.command(aliases=['eg','egggroup'])
async def eggGroup(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nEGGGROUP command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

    pos_args = ['group']

    args = parse_arguments(raw_args, pos_args)
    if args is None:
        print('Error parsing command, bzzzzrt! Type "!help" for usage details.', file=output)
        await output.send(ctx)
        return

    group = args['pos']['group'].lower().replace(' ','')

    filters = pokemongo.add_user_pokemon_filters(args['fil'], ctx.author.id)
    
    pokemongo.print_filters(filters[1], output)
    PokeDex(pokemongo).do_egg_group_function(group, filters[0], output)

    await output.send(ctx)

@bot.command(aliases=['qp','querypokedex'])
async def queryPokedex(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nQUERYPOKEDEX command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

    args = parse_arguments(raw_args)
    if args is None:
        print('Error parsing command, bzzzzrt! Type "!help" for usage details.', file=output)
        await output.send(ctx)
        return
    
    count = get_option(args['opt'], 'count')
    force_list = get_option(args['opt'], 'force-list')

    filters = pokemongo.add_user_pokemon_filters(args['fil'], ctx.author.id)

    pokemongo.print_filters(filters[1], output)
    PokeDex(pokemongo).do_pokedex_query_function(filters[0], output, count, force_list)

    await output.send(ctx)

@bot.command(aliases=['qm','querymoves'])
async def queryMoves(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nQUERYMOVES command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

    args = parse_arguments(raw_args)
    if args is None:
        print('Error parsing command, bzzzzrt! Type "!help" for usage details.', file=output)
        await output.send(ctx)
        return
    
    count = get_option(args['opt'], 'count')
    force_list = get_option(args['opt'], 'force-list')

    filters = pokemongo.add_user_move_filters(args['fil'], ctx.author.id)

    pokemongo.print_filters(filters[1], output)
    MoveDex(pokemongo).do_moves_query_function(filters[0], output, count, force_list)

    await output.send(ctx)

@bot.command(aliases=['rp','randompokemon'])
async def randomPokemon(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nRANDOMPOKEMON command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

    args = parse_arguments(raw_args)
    if args is None:
        print('Error parsing command, bzzzzrt! Type "!help" for usage details.', file=output)
        await output.send(ctx)
        return

    filters = pokemongo.add_user_pokemon_filters(args['fil'], ctx.author.id)

    pokemongo.print_filters(filters[1], output)
    PokeDex(pokemongo).do_random_pokemon_function(filters[0], output)

    await output.send(ctx)

@bot.command(aliases=['rm','randommove'])
async def randomMove(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nRANDOMMOVE command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

    args = parse_arguments(raw_args)
    if args is None:
        print('Error parsing command, bzzzzrt! Type "!help" for usage details.', file=output)
        await output.send(ctx)
        return

    filters = pokemongo.add_user_move_filters(args['fil'], ctx.author.id)

    pokemongo.print_filters(filters[1], output)
    MoveDex(pokemongo).do_random_move_function(filters[0], output)

    await output.send(ctx)

@bot.command(aliases=['ra','randomability'])
async def randomAbility(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nRANDOMABILITY command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

    args = parse_arguments(raw_args)
    if args is None:
        print('Error parsing command, bzzzzrt! Type "!help" for usage details.', file=output)
        await output.send(ctx)
        return

    AbilityDex(pokemongo).do_random_ability_function(output)

    await output.send(ctx)

@bot.command(aliases=['rt','randomtype'])
async def randomType(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nRANDOMTYPE command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

    args = parse_arguments(raw_args)
    if args is None:
        print('Error parsing command, bzzzzrt! Type "!help" for usage details.', file=output)
        await output.send(ctx)
        return

    PokemonHelper().do_random_type_function(output)

    await output.send(ctx)

@bot.command(aliases=['rc','randomcolor'])
async def randomColor(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nRANDOMCOLOR command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

    args = parse_arguments(raw_args)
    if args is None:
        print('Error parsing command, bzzzzrt! Type "!help" for usage details.', file=output)
        await output.send(ctx)
        return

    PokemonHelper().do_random_color_function(output)

    await output.send(ctx)

@bot.command(aliases=['n'])
async def nature(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nNATURE command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

    pos_args = ['token']
    opt_pos_args = ['down']

    args = parse_arguments(raw_args, pos_args, opt_pos_args)
    if args is None:
        print('Error parsing command, bzzzzrt! Type "!help" for usage details.', file=output)
        await output.send(ctx)
        return

    if 'down' in args['pos']:
        PokemonHelper().do_get_nature_name_function(args['pos']['token'], args['pos']['down'], output)
    else:
        PokemonHelper().do_get_nature_stats_function(args['pos']['token'], output)

    await output.send(ctx)

@bot.command(aliases=['s'])
async def shiny(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nSHINY command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

    pos_args = ['pokemon']

    args = parse_arguments(raw_args, pos_args)
    if args is None:
        print('Error parsing command, bzzzzrt! Type "!help" for usage details.', file=output)
        await output.send(ctx)
        return

    pokemon = args['pos']['pokemon'].lower().replace(' ','')

    shiny_info = PokeDex(pokemongo).do_get_shiny_image_function(pokemon, output)
    species = 'Missingno'
    shiny_link = 'https://www.serebii.net/pokearth/sprites/rb/000.png'
    if shiny_info is not None:
        species = shiny_info[0]
        shiny_link = shiny_info[1]

    embed = Embed()
    embed.description = f'Image for {species} sourced from [Serebii.net](https://www.serebii.net/)!'
    embed.set_image(url=shiny_link)

    await output.send(ctx, embed=embed)

@bot.command(aliases=['fp','pokemonfilters','filterpokemon'])
async def pokemonFilters(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nPOKEMONFILTERS command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

    args = parse_arguments(raw_args)
    if args is None:
        print('Error parsing command, bzzzzrt! Type "!help" for usage details.', file=output)
        await output.send(ctx)
        return
    
    pokemongo.update_user_pokemon_filters(ctx.author.id, args['fil'])

    if len(args['fil']) == 0:
        print('Default pokemon filters reset, bzzzzrt!', file=output)
    else:
        print('Default pokemon filters updated, bzzzzrt!', file=output)
        for f in args['fil']:
            print(f' - {f}:{args["fil"][f]}', file=output)

    await output.send(ctx)

@bot.command(aliases=['fm','movefilters','filtermoves'])
async def moveFilters(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nMOVEFILTERS command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

    args = parse_arguments(raw_args)
    if args is None:
        print('Error parsing command, bzzzzrt! Type "!help" for usage details.', file=output)
        await output.send(ctx)
        return
    
    pokemongo.update_user_move_filters(ctx.author.id, args['fil'])

    if len(args['fil']) == 0:
        print('Default move filters reset, bzzzzrt!', file=output)
    else:
        print('Default move filters updated, bzzzzrt!', file=output)
        for f in args['fil']:
            print(f' - {f}:{args["fil"][f]}', file=output)

    await output.send(ctx)

@bot.command()
async def test(ctx, *raw_args):
    return
    message = ctx.message.content
    print(f'\nTEST command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

    args = parse_arguments(raw_args)
    if args is None:
        print('Error parsing command, bzzzzrt! Type "!help" for usage details.', file=output)
        await output.send(ctx)
        return

    pprint(ctx.author.id)

    await output.send(ctx)

if beta:
    bot.run('ODExMzQ2MjAxMDcyNzYyOTYw.YCw3CA.aMEwKzL0iAKnV9gs577-0EaJGVg')
else:
    bot.run('Njc1MjM0NTk5NTA0NDQ1NDQx.Xj0LQw.4aoRdNE6P2VgV17YRDkwcOcsMEo')
