import discord
from discord.ext import commands
import wolframalpha
import aiohttp, io, asyncio
import requests, json
import shutil, os
import time
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

# globals
TOKEN = tokens.DISCORD_TOKEN
WOLFRAM_ID = tokens.WOLFRAM_TOKEN

client = commands.Bot(command_prefix="chad ")
wolframClient = wolframalpha.Client(WOLFRAM_ID)
starttime = time.perf_counter()
deleted_image_storage = []
voice_client = None
queue_list = []

copypath = "./temp/bot_settings_copy.json"
# remove all temp files

if os.path.isdir("./temp/"):
    shutil.rmtree("temp")
os.makedirs("temp")
shutil.copy("./bot_settings.json", copypath)


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
    output = ""
    for x in list:
        output += x + " "
    return output


def is_me(m):
    return m.author == client.user


def getjson():
    settings_file = open("./bot_settings.json", "r")
    return json.load(settings_file)


def check_perms(user, level):
    ourjson = getjson()["userlist"][level]
    check = False
    for element in ourjson:
        if ourjson[element] == user:
            check = True
    return check


def updatejson(*args):
    obj = getjson()

    if args[0] == "delete":
        if args[1] == "userlist":
            del obj["userlist"][args[2]][args[3]]
        else:
            del obj["settings"][args[2]]
    else:
        if len(args) > 3:
            obj[args[0]][args[1]][args[2]] = args[3]
        else:
            obj[args[0]][args[1]] = args[2]

    settings_file = open("bot_settings", "w")
    json.dump(obj, settings_file)
    settings_file.close()
    print(obj)


@client.event
async def on_ready():
    print(" the bot is ready")
    await client.change_presence(activity=discord.Game("in bed with Daddy Bot")
                                 )


@client.event
async def on_message(message):
    rude = False
    if getjson()['settings']['rude'] == 'true':
        rude = True
    # respond to daddybot
    if (str(message.author) == "DaddyBot#2616" and rude):
        await message.channel.send("shut the fuck up daddybot")

    # respond to blacklisted users
    if (check_perms(str(message.author), "blacklist")
            and message.content[:4] == "chad"):
        await message.channel.send("shut the fuck up faggot")

    # respond to people trying to use the bot when rude
    if (not check_perms(str(message.author), 'admins') and rude
            and message.content[:4] == "chad"):
        await message.channel.send("shut the fuck up faggot")
        return

    try:
        mystr = str(message.attachments[0])
        print(mystr)
        myurl = mystr[mystr.find("https"):-1]
        deleted_image_storage.append(str(message.author) + " " + myurl)
        file = requests.get(myurl)
        open("./temp/testfile.png", "wb").write(file.content)
    except:
        pass
    if check_perms(str(message.author), "blacklist"):
        return
    await client.process_commands(message)


@client.event
async def on_message_delete(message):
    if check_perms(message.author, 'admins'):
        return
    await message.channel.send(
        f"{message.author} deleted a message: {message.content}")


@client.command()
async def ping(ctx):
    await ctx.send(f" {round(client.latency * 1000)} ms")


@client.command()
async def clear(ctx, amount, arg="quiet"):
    if not check_perms(str(ctx.author), "admins"):
        await ctx.send("shut up retard")
        return
    deleted = await ctx.channel.purge(limit=int(amount) + 1)
    if arg != "quiet":
        await ctx.send(f"deleted {amount} messages")


@client.command()
async def wolfram(ctx, *args):
    try:
        message = ""
        for x in args:
            message += x
            message += " "
        res = wolframClient.query(message)
        answer = next(res.results).text
        await ctx.send(answer)
    except:
        await ctx.send("Wolfram failed to find an answer")


@client.command()
async def wolframimage(ctx, *args):
    url = f"http://api.wolframalpha.com/v1/simple?appid={WOLFRAM_ID}&i="
    for x in args:
        url += x + "+"
    url = url[:len(url) - 1]
    url += "%3F"  # url is now ready

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return await ctx.send("Could not download file...")
            data = io.BytesIO(await resp.read())
            await ctx.send(file=discord.File(data, "cool_image.png"))


@client.command()
async def say(ctx, *args):
    await ctx.send(listToString(args))


@client.command()
async def status(ctx, *, args):
    if not check_perms(str(ctx.author), "admins"):
        await ctx.send("shut up retard")
        return
    await client.change_presence(activity=discord.Game(args))
    await ctx.send(f"status changed to {args}")


@client.command()
async def translate(ctx, *, args):
    alphabet = " abcdefghijklmnopqrstuvwxyz"
    betterAlphabet = [
        " ",
        "ᔑ",
        "ʖ",
        "ᓵ",
        "↸",
        "ᒷ",
        "⎓",
        "⊣",
        "⍑",
        "╎",
        "⋮",
        "ꖌ",
        "ꖎ",
        "ᒲ",
        "リ",
        "𝙹",
        "!",
        "¡",
        "ᑑ",
        "∷",
        "ᓭ",
        "ℸ",
        "̣",
        "⚍",
        "⍊",
        "∴",
        "'",
    ]
    newStr = ""
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
        await ctx.send("enter a number retard")


@client.command()
async def clearspace(ctx, *, args):
    newStr = ""
    for i in args:
        newStr += i if i != " " else ""
    await ctx.send(newStr)


@client.command()
async def kill(ctx):
    if str(ctx.author) != "asiank0ala#8008":
        await ctx.send("shut the fuck up faggot")
    else:
        await ctx.send(":cry:")
        exit()


@client.command()
async def sonic(ctx):
    await ctx.send(
        "https://cdn.discordapp.com/attachments/619660668580266005/712416983437803592/sonic_movie.mp4"
    )


@client.command()
async def clearbot(ctx, amount):
    if not check_perms(str(ctx.author), "admins"):
        await ctx.send("shut up retard")
        return
    deleted = await ctx.channel.purge(limit=100, check=is_me)
    await ctx.send(f"deleted {amount} messages")


@client.command()
async def update(ctx, *args):
    if not check_perms(str(ctx.author), "admins"):
        await ctx.send("shut up retard")
        return
    obj = getjson()

    if args[0] == "delete":
        if args[1] == "userlist":
            del obj["userlist"][args[2]][args[3]]
        else:
            del obj["settings"][args[2]]
    else:
        if len(args) > 3:
            username = ''
            for k in args[3:]:
                username += k
                username += ' '
            obj[args[0]][args[1]][args[2]] = username[:-1]
        else:
            obj[args[0]][args[1]] = args[2]

    settings_file = open("./bot_settings.json", "w")
    json.dump(obj, settings_file)
    settings_file.close()
    await ctx.send(obj)


@client.command()
async def getsettings(ctx):
    await ctx.send(getjson())


@client.command()
async def opgg(ctx, *args):
    summoner = ""
    for i in args:
        summoner += i + "%20"
    await ctx.send("https://na.op.gg/summoner/{}".format(summoner))


@client.command()
async def join(ctx):
    global voice_client
    channel = ctx.author.voice.channel
    voice_client = await channel.connect()


@client.command()
async def play(ctx, *, args):
    global voice_client
    channel = ctx.author.voice.channel
    if not voice_client.is_connected():
        voice_client = await channel.connect()

    newargs = ""
    for i in args:
        if i != " ":
            newargs += i
        else:
            newargs += "+"
    print(newargs)
    myurl = "https://www.youtube.com/results?search_query={}".format(newargs)

    uClient = uReq(myurl)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    results_text = page_soup.findAll("body",
                                     {"dir": "ltr"})[0].findAll("script")[1]
    code_index = str(results_text).index(r"/watch?v=") + 9
    vid_code = str(results_text)[code_index:code_index + 11]

    newargs = ""
    for i in args:
        if i != " ":
            newargs += i
        else:
            newargs += "_"
    video_url = "https://www.youtube.com/watch?v={}".format(vid_code)
    os.system(
        r"youtube-dl -o C:\Users\neilm\Documents\vscode\chadbot\temp\{}.%(ext)s --extract-audio --audio-format mp3 {}"
        .format(newargs, video_url))

    await ctx.send("video found: {}".format(video_url))

    if voice_client.is_playing():
        queue_list.append(newargs)
    voice_client.play(discord.FFmpegPCMAudio("./temp/{}.mp3".format(newargs)))


@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@client.command()
async def dm(ctx, user, *, args):
    target = ctx.guild.get_member_named(user)
    await target.send(args)
    await ctx.channel.purge(limit=1)


@client.command()
async def id_dm(ctx, id, *, args):
    target = await client.fetch_user(id)
    await target.send()
    await ctx.channel.purge(limit=1)


@client.command()
async def uptime(ctx):
    diff = time.perf_counter() - starttime  # in seconds
    hours = diff // 3600
    minutes = diff // 60
    seconds = diff - hours * 3600 - minutes * 60
    await ctx.send(f"{int(hours)}:{int(minutes)}:{int(seconds)}")


@client.command()
async def getid(ctx, user):
    target = ctx.guild.get_member_named(user)
    await ctx.send(target.id)


@client.command()
async def test(ctx, url):
    r = requests.get(url, allow_redirects=True)
    open("./5Head.jpg", "wb").write(r.content)


@client.command()
async def belle(ctx):
    await ctx.send("""You were thinking I died? Bitch, surprise
I still got them double-thick thighs, french fries
I get down and gobble, gobble up, with my booty up
She be going wobble wobble up, here's a big duck
Slide, slide in the peanut butter, don’t Zucc her
Who actually regrets me? My mother
I trolled betas with my Pornhub, betrayer
You nothin' but a hater hater, clout chaser

Now I watch my favorite Twitch thot, damn, she hot
What the fuck is with this mugshot? Ratatata
Elon's baby eat a Mars rock
Now I TikTok, begone, thot, begone, thot
All these simps always talkin’ shit, yada-yada-ya
When you see me, what you talking 'bout, little beansprout?
We're laughing 'cause you burnt out, got no clout
Yeah, you weak without your ass out (Yeah, yeah)
(What are you, fucking gay?)
Are you dumb, stupid, or dumb, huh?
Play me like a dummy, like, bitch, are dumb?
Are you dumb, stupid, or dumb?
Yeah, you got your money but you still freakin' ugly
XD, listen, you're not a politician
Yes, I'm a gamer, also a taxpayer
Skeet, yada, pass me Doritos
Send nudes, nani? Delphine, you nasty
Egg white, bite it, see that, get excited
Good vid, Susan, not allowed, copyrighted
You're boomer, I’m doomer, guess what? You die sooner
(Hey, that’s pretty good)

You were thinking I died? Bitch, surprise
I still got them double-thick thighs, no lies
I get down and gobble, gobble up, with my booty up
She be going wobble wobble up, here's a big duck
Slide, slide in the peanut butter, don’t Zucc her
Who actually regrets me? My mother
I trolled betas with my Pornhub, betrayer
You nothin' but a hater hater, clout chaser

You're mad I'm back? Big mad
He’s mad, she's mad, big sad
Haha, don't care, stay mad
Aha, aha, aha
Uwu, buy my OnlyFans, you big Chad
Little titties, big ass, and no dad
Bathwater sold out, big sad
OnlyFans now to get a big bag

Omae wa mō shindeiru
Nani?""")


client.run(TOKEN)
