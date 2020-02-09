#invite link: https://discordapp.com/oauth2/authorize?client_id=675234599504445441&scope=bot&permissions=3072

from discord.ext import commands
from source.abilitydex import AbilityDex
from source.movedex import MoveDex
from source.pokedex import PokeDex
from source.pokehelper import PokemonHelper
from pprint import pprint

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

@bot.event
async def on_ready():
    print("\nRotom Dex booted up! Bzzzrt!\n")

#@bot.event
#async def on_message(message):
#    print("Message received, bzzzzzzrt! Here's the message:\n", message.content)

@bot.command(aliases=['h'])
async def help(ctx):
    message = ctx.message.content
    print(f'\nHELP command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')

    output = MessageHelper()
    
    print('Available commands:', file=output)
    print('  - !(help|h)                                                    Shows a list of commands.', file=output)
    print('  - !(pokedex|p) (POKEMON)                                       Show the raw pokedex entry for POKEMON.', file=output)
    print('  - !(hiddenAbility|ha) (POKEMON)                                Show the hidden ability for POKEMON.', file=output)
    print('  - !(eggMove|em) (POKEMON) [MOVE]                               Show potential breeding chains for breeding MOVE onto POKEMON.', file=output)
    print('                                                                 If MOVE is not supplied, lists the available egg moves for POKEMON.', file=output)
    print('  - !(moveset|ms) (POKEMON)                                      Show the moves that POKEMON can learn.', file=output)
    print('  - !(moveset|ms) (POKEMON) [-s|--stab] [--ignore-stats|-i]      Show the top 5 STAB moves for POKEMON.', file=output)
    print('                                                                 Defaults to taking stats into account. Use -i to ignore them.', file=output)
    print('  - !(moveset|ms) (POKEMON) [-s=X] [--ignore-stats|i]            Show the top X STAB moves for POKEMON.', file=output)
    print('  - !(moveset|ms) (POKEMON) [-c|--coverage] [--ignore-stats|-i]  Show the top 3 coverage moves for POKEMON.', file=output)
    print('                                                                 Defaults to taking stats into account. Use -i to ignore them.', file=output)
    print('  - !(moveset|ms) (POKEMON) [-c=X] [--ignore-stats|i]            Show the top X coverage moves for POKEMON.', file=output)
    print('  - !(ability|a) (ABILITY)                                       Show the information about ABILITY.', file=output)
    print('                                                                 Also lists all pokemon that can have ABILITY.', file=output)
    print('  - !(damage|d) (POKEMON)                                        Get the weaknesses/resistances for POKEMON.', file=output)
    print('  - !(damage|d) (TYPE1) [TYPE2]                                  Get the weaknesses/resistances of the given type(s).', file=output)
    print('', file=output)

    await output.send(ctx)

@bot.command(aliases=['ms'])
async def moveset(ctx):
    message = ctx.message.content
    print(f'\nMOVESET command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')

    arguments = message.split(' ')
    
    pokemon = arguments[1].lower()

    show_stab = False
    max_stab = 5
    ignore_stats = False
    show_coverage = False
    max_coverage = 3

    for arg in arguments:
        if arg[:2] == '-s':
            show_stab = True
            try:
                max_stab = int(arg[3:])
            except:
                max_stab = 5
        if arg[:2] == '-c':
            show_coverage = True
            try:
                max_coverage = int(arg[3:])
            except:
                max_coverage = 3
        if arg[:2] == '-i':
            ignore_stats = True

    if '--stab' in arguments:
        show_stab = True
    if '--coverage' in arguments:
        show_coverage = True
    if '--ignore-stats' in arguments:
        ignore_stats = True

    if not show_stab and not show_coverage:
        ignore_stats = True

    output = MessageHelper()
    MoveDex().do_moves_function(pokemon, show_stab, max_stab, ignore_stats, show_coverage, max_coverage, output)

    await output.send(ctx)

@bot.command(aliases=['em'])
async def eggMove(ctx):
    message = ctx.message.content
    print(f'\nEGGMOVE command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')

    arguments = message.split(' ')
    
    pokemon = arguments[1].lower()

    move = None
    if len(arguments) > 2:
        move = arguments[2].lower()

    output = MessageHelper()
    MoveDex().do_egg_moves_function(pokemon, move, output)

    await output.send(ctx)

@bot.command(aliases=['p'])
async def pokedex(ctx):
    message = ctx.message.content
    print(f'\nPOKEDEX command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')

    arguments = message.split(' ')
    
    pokemon = arguments[1].lower()
    
    output = MessageHelper()
    PokeDex().do_pokedex_function(pokemon, output)

    await output.send(ctx)

@bot.command(aliases=['ha'])
async def hiddenAbility(ctx):
    message = ctx.message.content
    print(f'\nHIDDENABILITY command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')

    arguments = message.split(' ')
    
    pokemon = arguments[1].lower()
    
    output = MessageHelper()
    PokeDex().do_hidden_ability_function(pokemon, output)

    await output.send(ctx)

@bot.command(aliases=['a'])
async def ability(ctx):
    message = ctx.message.content
    print(f'\nABILITY command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')

    arguments = message.split(' ')
    
    ability = arguments[1].lower()
    
    output = MessageHelper()
    AbilityDex().do_ability_search_function(ability, output)

    await output.send(ctx)

@bot.command(aliases=['m'])
async def move(ctx):
    message = ctx.message.content
    print(f'\nMOVE command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')

    arguments = message.split(' ')
    
    move = arguments[1].lower()
    
    output = MessageHelper()
    MoveDex().do_move_search_function(move, output)

    await output.send(ctx)

@bot.command(aliases=['d'])
async def damage(ctx):
    message = ctx.message.content
    print(f'\nDAMAGE command triggered, bzzzzrt! Message details:\n{ctx.message.author} @ ({ctx.message.created_at}): {message}\n')

    arguments = message.split(' ')
    
    pokemon = None
    type1 = None
    type2 = None

    output = MessageHelper()

    if len(arguments) == 2:
        token = arguments[1]
        if token.lower().capitalize() in PokemonHelper().get_types():
            type1 = token.lower().capitalize()
        else:
            pokemon = token.lower()

    elif len(arguments) == 3:
        type1 = arguments[1].lower().capitalize()
        type2 = arguments[2].lower().capitalize()

    else:
        print('Error: Invalid number of arguments, bzzzzrt!', file=output)
        await output.send(ctx)
        return
    
    if pokemon:
        PokeDex().do_pokemon_damage_function(pokemon, output)
    else:
        if type2:
            PokeDex().do_types_damage_function([type1, type2], output)
        else:
            PokeDex().do_type_damage_function(type1, output)

    await output.send(ctx)

bot.run('Njc1MjM0NTk5NTA0NDQ1NDQx.Xj0LQw.4aoRdNE6P2VgV17YRDkwcOcsMEo')