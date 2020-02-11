#invite link: https://discordapp.com/oauth2/authorize?client_id=675234599504445441&scope=bot&permissions=3072

from discord.ext import commands
from source.abilitydex import AbilityDex
from source.movedex import MoveDex
from source.pokedex import PokeDex
from source.pokehelper import PokemonHelper
from source.breedingbox import BreedingBox
from pprint import pprint

import sys

prefix = '!'
bot = commands.Bot(command_prefix=prefix)

bot.remove_command('help')

class MessageHelper:
    def __init__(self):
        self.message = ''

    def write(self, str):
        self.message += str

    async def send(self, ctx):
        message_lines = self.message.split('\n')
        message = ''
        while len(message_lines) > 0:
            new_message = message + f'\n{message_lines[0]}'
            if len(new_message) >= 1990:
                await ctx.send(f'```{message}```')
                message = ''
            message = message + f'\n{message_lines[0]}'
            message_lines.pop(0)
        await ctx.send(f'```{message}```')

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

def parse_arguments(arguments, positional_args=[], optional_pos_args=[]):
    arguments = list(arguments)

    pos = dict()
    opt = dict()
    fil = dict()

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

        elif len(optional_pos_args) > 0:
            pos[optional_pos_args[0]] = arg
            optional_pos_args.pop(0)

    if len(positional_args) > 0:
        return None

    return {'pos':pos, 'opt':opt, 'fil':fil}

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
    print("\nDexPy ready to receive commands, bzzzzrt!\n")

#@bot.event
#async def on_message(message):
#    print("Message received, bzzzzzzrt! Here's the message:\n", message.content)

@bot.command(aliases=['h'])
async def help(ctx):
    message = ctx.message.content
    print(f'\nHELP command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')

    output = MessageHelper()
    
    print('Available DexPy Commands:', file=output)
    print('', file=output)
    print(' Basic Commands:', file=output)
    print('  - !(help|h)                                                    Shows a list of commands.', file=output)
    print('  - !(pokedex|p) (POKEMON)                                       Show the raw pokedex entry for POKEMON.', file=output)
    print('  - !(hiddenAbility|ha) (POKEMON)                                Show the hidden ability for POKEMON.', file=output)
    print('  - !(ability|a) (ABILITY) [-p]                                  Show the information about ABILITY.', file=output)
    print('                                                                 Also lists all pokemon that can have ABILITY if -p is used.', file=output)
    print('  - !(move|m) (MOVE) [-p]                                        Show the information about MOVE.', file=output)
    print('                                                                 Also lists all pokemon that can learn MOVE if -p is used.', file=output)
    print('  - !(damage|d) (POKEMON)                                        Get the weaknesses/resistances for POKEMON.', file=output)
    print('  - !(damage|d) (TYPE1) [TYPE2]                                  Get the weaknesses/resistances of the given type(s).', file=output)
    print('', file=output)
    print(' Movesets:', file=output)
    print('  - !(moveset|ms) (POKEMON)                                      Show the moves that POKEMON can learn.', file=output)
    print('  - !(moveset|ms) (POKEMON) (-s|--stab) [--ignore-stats|-i]      Show the top 5 STAB moves for POKEMON.', file=output)
    print('                                                                 Defaults to taking stats into account. Use -i to ignore them.', file=output)
    print('  - !(moveset|ms) (POKEMON) (-s=X) [--ignore-stats|-i]           Show the top X STAB moves for POKEMON.', file=output)
    print('  - !(moveset|ms) (POKEMON) (-c|--coverage) [--ignore-stats|-i]  Show the top 3 coverage moves for POKEMON.', file=output)
    print('                                                                 Defaults to taking stats into account. Use -i to ignore them.', file=output)
    print('  - !(moveset|ms) (POKEMON) (-c=X) [--ignore-stats|-i]           Show the top X coverage moves for POKEMON.', file=output)
    print('', file=output)
    print(' Breeding:', file=output)
    print('  - !(eggGroup|eg) (EGG_GROUP)                                   Lists all evolutionary lines in EGG_GROUP.', file=output)
    print('  - !(eggMove|em) (POKEMON) [MOVE]                               Show potential breeding chains for breeding MOVE onto POKEMON.', file=output)
    print('                                                                 If MOVE is not supplied, lists the available egg moves for POKEMON.', file=output)
    print('  - !(breedingbox|bb) (-r|--register)=POKEMON                    Register POKEMON to your breeding box.', file=output)
    print('                                                                 This signifies to other users that you have this \'mon with HA.', file=output)
    print('  - !(breedingbox|bb) (-u|--unregister)=POKEMON                  Unregister POKEMON from your breeding box.', file=output)
    print('  - !(breedingbox|bb) (-q|--query)=POKEMON                       Check to see who has POKEMON with a hidden ability.', file=output)
    print('                                                                 Returns users who have registered a pokemon in the same evolutionary line.', file=output)
    print('', file=output)

    await output.send(ctx.author)

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

    if not show_stab and not show_coverage:
        ignore_stats = True

    MoveDex().do_moves_function(pokemon, show_stab, max_stab, ignore_stats, show_coverage, max_coverage, output)

    await output.send(ctx)

@bot.command(aliases=['em'])
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

    MoveDex().do_egg_moves_function(pokemon, move, output)

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
    
    PokeDex().do_pokedex_function(pokemon, verbose, output)

    await output.send(ctx)

@bot.command(aliases=['ha'])
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

    PokeDex().do_hidden_ability_function(pokemon, output)

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

    AbilityDex().do_ability_search_function(ability, show_list, output)

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

    MoveDex().do_move_search_function(move, show_list, output)

    await output.send(ctx)

@bot.command(aliases=['d'])
async def damage(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nDAMAGE command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

    pos_args = ['token']
    opt_pos_args = ['type2']

    args = parse_arguments(raw_args, pos_args)
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
    
    if pokemon:
        PokeDex().do_pokemon_damage_function(pokemon, output)
    else:
        if type2:
            PokeDex().do_types_damage_function([type1, type2], output)
        else:
            PokeDex().do_type_damage_function(type1, output)

    await output.send(ctx)

@bot.command(aliases=['bb'])
async def breedingbox(ctx, *raw_args):
    message = ctx.message.content
    print(f'\nBREEDINGBOX command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')
    output = MessageHelper()

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
            BreedingBox().register_ha_mon(user, username, p, output)
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
            BreedingBox().unregister_ha_mon(user, username, p, output)
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
            BreedingBox().query_ha_mon(user, p, output)
        await output.send(ctx)
        return

    print(f'Error: Unknown breeding box subcommand, bzzzzrt! Type "!help" for usage details.', file=output)

    await output.send(ctx)

@bot.command(aliases=['eg'])
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
    
    PokeDex().do_egg_group_function(group, output)

    await output.send(ctx)

bot.run('Njc1MjM0NTk5NTA0NDQ1NDQx.Xj0LQw.4aoRdNE6P2VgV17YRDkwcOcsMEo')