import discord
from discord.ext import commands
import wolframalpha
import aiohttp, io
import riotwatcher
import requests, json
import shutil, os
import tokens
import urllib.request
from bs4 import BeautifulSoup


# globals
TOKEN = tokens.DISCORD_TOKEN
WOLFRAM_ID = tokens.WOLFRAM_TOKEN
RIOTKEY = 'RGAPI-26405f6d-2e65-4ff0-a67d-fbf9bd56db05'
BETTERRIOTKEY = 'RGAPI-2330e647-0206-4545-b382-74cc029c1db3'

client = commands.Bot(command_prefix= 'chad ')
wolframClient = wolframalpha.Client(WOLFRAM_ID)
lolwatcher = riotwatcher.LolWatcher(BETTERRIOTKEY)



def isFloat(string):
    try:
        float(string)
        return True 
    except ValueError:
        return False

def isInt(string):
    if isFloat(string):
        return float(string) == int(string)
    return False

def listToString(list):
    output = ''
    for x in list:
        output += x + ' '
    return output

def is_me(m):
    return m.author == client.user 

def getjson():
    settings_file = open("./bot_settings.json", 'r')
    return json.load(settings_file)

def check_perms(user, level):
    ourjson = getjson()['userlist'][level]
    check = False
    for element in ourjson:
        if ourjson[element] == user:
            check = True
    return check

def updatejson(*args):
    obj = getjson()

    if args[0] == 'delete':
        if args[1] == 'userlist':
            del obj['userlist'][args[2]][args[3]]
        else:
            del obj['settings'][args[2]]
    else:
        if len(args) > 3:
            obj[args[0]][args[1]][args[2]] = args[3]
        else:
            obj[args[0]][args[1]] = args[2]
    
    settings_file = open('bot_settings', 'w')
    json.dump(obj, settings_file)
    settings_file.close()
    print(obj)
        
    
@client.event
async def on_ready():
    print(' the bot is ready')
    await client.change_presence(activity=discord.Game('in bed with Daddy Bot'))
    copypath = './temp/bot_settings_copy.json'
    # remove the copy of bot_settings
    if os.path.exists(copypath):
        os.remove(copypath)
    shutil.copy('./bot_settings.json', copypath)


@client.event 
async def on_message(message):
    if str(message.author) == 'DaddyBot#2616' and getjson()['settings']['rude'] == 'true':
        await message.channel.send('shut the fuck up daddybot')
    if check_perms(str(message.author), 'blacklist'):
        return
    await client.process_commands(message)


@client.event 
async def on_message_delete(message):
    await message.channel.send(f'{message.author} deleted a message: {message.content}')


@client.command()
async def ping(ctx):
    await ctx.send(f' {round(client.latency * 1000)} ms')


@client.command()
async def clearsend(ctx, *, args):
    await ctx.channel.purge(limit=1)
    await ctx.send(args)


@client.command()
async def clear(ctx, amount=10):
    if not check_perms(str(ctx.author), 'admins'):
        await ctx.send('shut up retard')
        return
    deleted = await ctx.channel.purge(limit=amount+1)
    await ctx.send(f'deleted {amount} messages')


@client.command()
async def wolfram(ctx, *args):
    try:
        message = ''
        for x in args:
            message += x
            message += ' '
        res = wolframClient.query(message)
        answer = next(res.results).text
        await ctx.send(answer)
    except:
        await ctx.send('Wolfram failed to find an answer')


@client.command()
async def wolframimage(ctx, *args):
    url = f'http://api.wolframalpha.com/v1/simple?appid={WOLFRAM_ID}&i='
    for x in args:
        url += x + '+'
    url = url[:len(url)-1]
    url += '%3F' # url is now ready 
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file...')
            data = io.BytesIO(await resp.read())
            await ctx.send(file=discord.File(data, 'cool_image.png'))


@client.command()
async def say(ctx, *args):
    await ctx.send(listToString(args))


@client.command()
async def status(ctx, *,args):
    if not check_perms(str(ctx.author), 'admins'):
        await ctx.send('shut up retard')
        return 
    await client.change_presence(activity=discord.Game(args))
    await ctx.send(f'status changed to {args}')


summoner = ''
region = ''
@client.command()
async def league(ctx, *args):
    if args[0] == 'help':
        await ctx.send(''' 
        commands: settings [region] [username]: stores region and settings
        stats: gets ranked stats of stored user
        match [number]: match data from x matches ago''' )

    elif args[0] == 'settings':
        global region
        global summoner
        summoner = ''
        region = args[1]
        for x in args[2:]:
            summoner += x + ' '
        await ctx.send(f'summoner set to {summoner}')
        await ctx.send(f'region set to {region}')

    elif args[0] == 'stats':
            me = lolwatcher.summoner.by_name(region, summoner)
            statsList = lolwatcher.league.by_summoner(region, me['id'])
            ranked_stats = statsList[0]
            await ctx.send('STATS')
            await ctx.send('---------')
            for key, value in ranked_stats.items():
                await ctx.send('{}: {}'.format(key, value))
    #    except: 
  #          await ctx.send('Connection refused')
      #      await ctx.send('Fix ur api key :flushed:')


@client.command()
async def translate(ctx, *, args):
    alphabet = ' abcdefghijklmnopqrstuvwxyz'
    betterAlphabet = [' ', 'ᔑ', 'ʖ', 'ᓵ', '↸', 'ᒷ', '⎓', '⊣', '⍑', '╎', '⋮', 'ꖌ', 'ꖎ', 'ᒲ', 'リ', '𝙹', '!', '¡', 'ᑑ', '∷', 'ᓭ', 'ℸ', '̣', '⚍', '⍊', '∴', "'"]
    newStr = ''
    for i in args:
        if alphabet.find(args[0]) != -1:
            place = alphabet.find(i)
            newStr += betterAlphabet[place]
        else:
            place = betterAlphabet.index(i)
            newStr += alphabet[place]
    await ctx.send(newStr)


@client.command()
async def spam(ctx, *args):
    try:
        for i in range(int(args[-1])):
            await ctx.send(listToString(args[:-1]))
    except:
        await ctx.send('enter a number retard')


@client.command()
async def clearspace(ctx, *, args):
    newStr = ''
    for i in args:
        newStr += i if i != ' ' else ''
    await ctx.send(newStr)


@client.command()
async def kill(ctx):
    if str(ctx.author) != 'asiank0ala#8008':
        await ctx.send('shut the fuck up faggot')
    else:
        await ctx.send(':cry:')
        exit()


@client.command()
async def sonic(ctx):
    await ctx.send('https://cdn.discordapp.com/attachments/619660668580266005/712416983437803592/sonic_movie.mp4')


@client.command()
async def clearbot(ctx, amount):
    if not check_perms(str(ctx.author), 'admins'):
        await ctx.send('shut up retard')
        return 
    deleted = await ctx.channel.purge(limit=100, check=is_me )
    await ctx.send(f'deleted {amount} messages')
    

@client.command()
async def update(ctx, *args):
    if not check_perms(str(ctx.author), 'admins'):
        await ctx.send('shut up retard')
        return 
    obj = getjson()

    if args[0] == 'delete':
        if args[1] == 'userlist':
            del obj['userlist'][args[2]][args[3]]
        else:
            del obj['settings'][args[2]]
    else:
        if len(args) > 3:
            obj[args[0]][args[1]][args[2]] = args[3]
        else:
            obj[args[0]][args[1]] = args[2]
    
    settings_file = open('./bot_settings.json', 'w')
    json.dump(obj, settings_file)
    settings_file.close()
    await ctx.send(obj)


@client.command()
async def getsettings(ctx):
    await ctx.send(getjson())


@client.command()
async def opgg(ctx, *args):
    summoner = ''
    for i in args:
        summoner += i + '%20'
    await ctx.send('https://na.op.gg/summoner/{}'.format(summoner))


@client.command()
async def play(ctx, args):
    url = ''
    if args[:18] == 'youtube.com/watch?':
        url = args
    else:
        pass
    

@client.command()
async def loop(ctx):
    pass 

@client.command()
async def queue(ctx, args):
    pass 


    
client.run(TOKEN)