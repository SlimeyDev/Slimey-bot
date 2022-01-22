import discord
from discord import embeds
from discord import colour
from discord import asset
from discord import message
from discord import channel
from discord import emoji
from discord import components
from discord.colour import Color
from discord.embeds import Embed
from discord.enums import Status
from discord.errors import ClientException
from discord.ext import commands, tasks
from discord.ui import Button, View
import json
from discord.ext.commands.bot import Bot
from discord.ext.commands.core import guild_only
from discord.ui import Button, View
from discord.utils import V
import requests
import random
from requests.models import Response
import datetime
import os
import sys
import string
import secrets
import asyncio
from discord.commands import Option

bot = commands.Bot(command_prefix="<", help_command=None)


if not os.path.exists('config.json'):
    with open("config.json", 'w') as f:
        f.write("""{"token":"","owners":[]}""")
    with open("config.json", 'r') as f:
        conf = json.load(f)

    
    print("WARNING: It looks like the configuration file does not exists. Please enter the Bot-Token and Owner IDs: ")

    input_token = input("Enter Token: ")
    print("\n\nGood! Now enter the Owner_IDs. If you don't want to set an OPTIONAL owner ID, just press enter without any input.")
    input_owner1 = input("Enter first Owner ID (required): ")
    if input_owner1 == "":
        print("Required option.")
        exit()
    input_owner2 = input("Enter second Owner ID (optional): ")
    if input_owner2 == "":
        input_owner2 = "1"
    input_owner3 = input("Enter third Owner ID (optional): ")
    if input_owner3 == "":
        input_owner3 = "1"
    print("Input recorded.\nWriting to configuration...")
    with open("config.json", 'w') as f:
        conf["token"] = input_token
        conf["owners"].append(int(input_owner1))
        conf["owners"].append(int(input_owner2))
        conf["owners"].append(int(input_owner3))

        json.dump(conf, f, indent=4)
        print("Succesfully recorded all configurations. If you want to run this setup again, delete 'config.json'.")


with open("config.json", 'r') as f:
            conf = json.load(f)

@bot.event
async def on_ready():
    #update_odds.start()
    #f"{len(bot.guilds)} servers | <help"
    # status=discord.Status.idle
    # await bot.change_presence(status=discord.Status.online, activity=discord.ActivityType.watching, name=f"{len(bot.guilds)} servers | <help")
    Bot_Status = f"{len(bot.guilds)} servers | <help"
    members = sum([guild.member_count for guild in bot.guilds])
    channels = 0
    for guild in bot.guilds:
        channels += len(guild.channels)
    stats = {"Guilds": len(bot.guilds), "Users": members, "Channels": channels}
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=Bot_Status))
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Current stats: ", stats)
    print("----------")


def update_odds():
    now = datetime.datetime.now()

    if now.hour == 12 and now.minute == 0 and now.second == 0:
        global megaflip
        global bottleflipvar
        megaflip = 0
        bottleflipvar = 0
        bottleflipvar = random.randint(30, 80)
        megaflip = random.randint(20, 60)


def is_it_me(ctx):
    owners = conf["owner"]
    if ctx.author.id in owners:
        return ctx.author.id


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)


class Joke:
    setup = ""
    punchline = ""

    def __init__(self, setup, punchline):
        self.setup = setup
        self.punchline = punchline


def get_Joke():
    url = "https://dad-jokes.p.rapidapi.com/random/joke"
    headers = {
        'x-rapidapi-host': "dad-jokes.p.rapidapi.com",
        'x-rapidapi-key': "f54cc328d6msh97c78a7088ae219p185068jsn07d335d78fe6"
    }
    response = requests.request("GET", url, headers=headers)
    json_data = json.loads(response.text)
    setup = json_data["body"][0]["setup"]
    punchline = json_data["body"][0]["punchline"]
    joke = Joke(setup, punchline)
    return(joke)

# @bot.event
# async def on_message(msg):
#     if bot.user.mentioned_in(msg) and not msg.content == "@everyone":
#         await msg.channel.send('My prefix is "<" type "<help" for all the commands!')


@bot.command()
@commands.check(is_it_me)
async def restart(ctx):
    em = discord.Embed(title="<:Slimey_tick:933232568210436136> Bot will be restarted",
                       description="The bot will restarting now", color=discord.Colour.purple())
    await ctx.reply(embed=em)
    # Restarting the bot
    os.execv(sys.executable, ['python'] + sys.argv)


@bot.command()
@commands.check(is_it_me)
async def update(ctx):
    em = discord.Embed(title="<:Slimey_tick:933232568210436136> Bot will be updating",
                       description="Fetching new code if available", color=discord.Colour.purple())
    await ctx.reply(embed=em)
    # Running git pull for getting last commit
    os.system("git pull")


@bot.command()
async def ping(ctx):
    em = discord.Embed(
        title="Pong !!", description=f"{round(bot.latency*1000)}ms", color=discord.Colour.blue())

    await ctx.reply(embed=em)


@bot.command(aliases=["ball", "8ball"])
async def magic8ball(ctx, *, question: str):

    responses = ["It is certain.",
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Get out before I eat your cat",
                 "Yes.",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My sources say no.",
                 "Very doubtful.",
                 "nerd",
                 "I AM TRYING TO SLEEP",
                 "idk",
                 "sorry I dont answer nerds"]

    await ctx.reply(f"Question: {question}\nAnswer: {random.choice(responses)}")


@bot.command(aliases=["yorn", "YorN"])
async def yesorno(ctx):

    responses = ["Yes.", "No.", "nerd", "probs", "prob yes",
                 "prob no", "idk nerd", "most prob yes", "most prob no"]

    await ctx.reply(random.choice(responses))


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):

    await ctx.channel.purge(limit=amount + 1)


@bot.command(aliases=["cointos", "cointoss", "flipcoin"])
@commands.cooldown(1, 10, commands.BucketType.user)
async def coinflip(ctx):
    x = random.randint(1, 2)

    if (x == 1):
        em = discord.Embed(
            title="Heads!", description="The coin fliped HEADS!", color=discord.Colour.green())
        em.set_thumbnail(url="https://i.postimg.cc/mkt4HwWN/Heads.jpg")

        await ctx.reply(embed=em)
    else:
        em = discord.Embed(
            title="Tails!", description="The coin fliped TAILS!", color=discord.Colour.green())
        em.set_thumbnail(url="https://i.postimg.cc/DZCF0NHw/Tails.jpg")

        await ctx.reply(embed=em)


@bot.command()
async def dadjoke(ctx):
    joke = get_Joke()
    sending_joke = joke.setup + "." + joke.punchline

    await ctx.reply(sending_joke)


@bot.command()
async def inspire(ctx):
    quote = get_quote()
    await ctx.reply(quote)

@bot.command()
async def twitch(ctx):
    await ctx.reply("GO FOLLOW ME ON TWITCH RIGHT NOW: https://www.twitch.tv/theslimeydevloper")


@bot.command()
async def youtube(ctx):
    await ctx.reply("The youtube channel of TheSlimeyDevloper is - https://www.youtube.com/channel/UCH-QFhiX-G8FFjQp8oL9_2A SO GO SUB!")


@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def bottleflip(ctx):
    y = random.randint(1, 101)
    z = random.randint(1, 101)

    if (z < megaflip):
        em = discord.Embed(title="Triple Mega Flip!",
                           description="Wait it can't be.....**YOU JUST GOT THE TRIPPLE MEGA FLIP!!**The bottle landed on its cap after it fliped **THRICE**!!", color=discord.Colour.blue())
        await ctx.reply(embed=em)

    else:
        if (y < bottleflipvar):
            em = discord.Embed(
                title="Bottle Fliped!", description="THE BOTTLE FLIPED AND FELL UP RIGHT! Bravo!", color=discord.Colour.green())

            await ctx.reply(embed=em)

        else:
            em = discord.Embed(title="Bottle did not flip...",
                               description="The bottle did not fall upright...Better luck next time!", color=discord.Colour.red())

            await ctx.reply(embed=em)


@bot.command()
async def info(ctx):
    await ctx.reply("Information on the bot: This bot was made using VS Code using the language Python. It was made by a new creator TheSlimeyDevloper.\nCurrent creators of this bot are TheSlimeyDev_YT#8584, fun12545#5552, Fuchsdo#4581")


@bot.command()
async def help(ctx):
    em = discord.Embed(
        title="Currently the existing commands are -", color=discord.Colour.blue())
    em.add_field(name="<coinflip", value="Flips a coin!", inline=True)
    em.add_field(name="<youtube",
                 value="Shows TheSlimeyDevloper's youtube.", inline=True)
    em.add_field(name="<info", value="Gives info on the bot.", inline=True)
    em.add_field(name="<bottleflip",
                 value="Flips a bottle! Well there are chances of getting something *rare*.", inline=False)
    em.add_field(
        name="<twitch", value="Show you TheSlimeyDevloper's twitch account.", inline=True)
    em.add_field(name="<inspire",
                 value="Sends you an insperational qoute!", inline=True)
    em.add_field(name="<dadjoke",
                 value="Sends u a stupid dadjoke\n -_-", inline=True)
    em.add_field(name="<ping", value="Tells you your latecy.", inline=False)
    em.add_field(
        name="<odds", value="Tells you your odds of getting a bottle flip!", inline=True)
    em.add_field(
        name="<invite", value="Sends an invite link to invite me to your server!", inline=True)
    em.add_field(name="<clear <value>",
                 value="Used to clear a bunch of messages!", inline=True)
    em.add_field(
        name="<report", value="Use this command to report bugs and problems on the bot!", inline=False)
    em.add_field(name="<say <value>", value="Sends the value!", inline=True)
    em.add_field(name="<magic8ball <question>",
                 value="Ask it a question and it will tell you your faith...", inline=True)
    em.add_field(name="<yesorno <question>",
                 value="Answers **Yes** or **No** to the question you entered", inline=True)
    em.add_field(name="<rps <value>",
                 value="Play some rock paper scissors with me!", inline=False)
    em.add_field(name="<send_password <value>",
                 value="Generate some passwords!", inline=True)
    em.add_field(name="/send_meme", value="Sends a meme from reddit!", inline=True)
    em.add_field(name="/timeout <user> <int> \n<s | min | h | d> [reason]", value="Timeout members!", inline=True)
    em.add_field(name="<embed <title> <description>", value="You can make embeds using this command!", inline=False)
    em.add_field(name="<kick <member> <reason>", value="kicks a member", inline=True)
    em.add_field(name="<ban <member> <reason>", value="Bans a member", inline=True)
    em.add_field(name="<vote", value="Vote the bot on top.gg!")

    await ctx.send(embed=em)


@bot.command()
async def invite(ctx):
    await ctx.reply("Invite me now @ https://discord.com/api/oauth2/authorize?client_id=915488552568123403&permissions=1538373582279&scope=bot%20applications.commands")


@bot.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def rps(ctx, response=None):
    if response == "rock" or response == "paper" or response == "scissor" or response == "scissors":

        botRes = random.choice(["rock", "paper", "scissor"])
        await ctx.reply(botRes)

        if botRes == response:
            await ctx.send("ITS A TIE!")
        elif botRes == "rock" and response == "paper":
            await ctx.send("You win!")
        elif botRes == "paper" and response == "rock":
            await ctx.send("I win!")
        elif botRes == "scissor" and response == "rock":
            await ctx.send("You win!")
        elif botRes == "rock" and response == "scissor":
            await ctx.send("I win!")
        elif botRes == "rock" and response == "scissors":
            await ctx.send("I win!")
        elif botRes == "paper" and response == "scissors":
            await ctx.send("You win!")
        elif botRes == "scissor" and response == "paper":
            await ctx.send("I win!")

    else:
        em = discord.Embed(
            title="<:Slimey_x:933232568055267359> Oops!", description="Invalid respons! Please type a response that contains rock, paper, scissor and remember its case sensitive!", color=discord.Color.red())
        await ctx.reply(embed=em)


@bot.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def report(ctx):
    em = discord.Embed(title="Report problems!", url="https://forms.gle/zwioTfRoErEZfTim6",
                       description="Click the title to report a bug/problem!", color=discord.Color.gold())
    await ctx.reply(embed=em)


@bot.command()
async def odds(ctx):

    em = discord.Embed(title="channces of getting bottle flip -", description="Normal bottle flip - " + str(
        bottleflipvar) + " in 100\nTriple mega bottle flip - " + str(megaflip) + " in 100", color=discord.Color.gold())
    em.add_field(name="These odds will randomize every 12 hours",
                 value="To make it a little bit more fun the bottleflip chances will randomize every 12 hours!", inline=False)

    await ctx.reply(embed=em)


@bot.command()
async def say(ctx, *, message: str = None):

    if message == None:
        await ctx.send("<:Slimey_x:933232568055267359> Please enter a message to send!")
    
    else:
        await ctx.message.delete()
        await ctx.send(message, allowed_mentions=discord.AllowedMentions.none())


@bot.command()
async def password(ctx):
    await ctx.reply("<:slash:928599693984944138> Please use the **slash command**! (`/send_password`)")

# slash command version of <password:


@bot.slash_command()
async def send_password(ctx, length):
    length = int(length)
    if length <= 100:
        if length < 4:
            embed = discord.Embed(
                title="Error", color=discord.Colour.red(), description=f"Too small... :joy:")
            await ctx.respond(embed=embed)
            return
        chars = string.digits + string.ascii_letters + string.punctuation

        passwords = []

        for i in range(5):
            password = ''.join(secrets.choice(chars) for _ in range(length))
            passwords.append(password)

        embed = discord.Embed(title="Generated passwords", color=discord.Colour.blue(), description=f"I generated **5** passwords for you, which are **{length}** characters long.\n\n"
                              f"```txt\n{passwords[0]}\n{passwords[1]}\n{passwords[2]}\n{passwords[3]}\n{passwords[4]}```")

        await ctx.respond(embed=embed)
    else:
        embed = discord.Embed(title="<:Slimey_x:933232568055267359> Error", color=discord.Colour.red(
        ), description=f"Please don't go higher than 100!")
        await ctx.respond(embed=embed)


@bot.slash_command()
async def send_meme(ctx):
    url = "https://meme-api.herokuapp.com/gimme/memes"
    resp = requests.get(url=url)
    meme_json = resp.json()
    random_meme = meme_json["url"]

    meme_subreddit = meme_json["subreddit"]
    meme_author = meme_json["author"]
    meme_title = meme_json["title"]
    meme_link = meme_json["postLink"]
    meme_upvotes = meme_json["ups"]
    if meme_upvotes > 1000:
        meme_upvotes = round(meme_json["ups"], -3)

    api_meme = discord.Embed(title="Meme", colour=discord.Colour.blue(), description=(f"**`Subreddit`** „r/{meme_subreddit}“\n**`Title`** „[{meme_title}]({meme_link})“\n\n"
                                                                                      f"**`Post-Creator`** „{meme_author}“\n**`Upvotes`** {meme_upvotes}"), timestamp=datetime.datetime.now())
    api_meme.set_image(url=random_meme)
    await ctx.respond(embed=api_meme)
    m = await ctx.interaction.original_message()
    await m.add_reaction("👍")
    await m.add_reaction("👎")


@bot.command()
async def meme(ctx):
    await ctx.reply("<:slash:928599693984944138> Please use the **slash command**! (`/send_meme`)")


@bot.command()
async def embed(ctx, title_em=None, description_em=None):

    if title_em == None and description_em == None or description_em == None or title_em == None:

        em = discord.Embed(title = "Error!", description = "No value specified for embed title or description")

        await ctx.send(embed=em)

    else:
        em = discord.Embed(title=title_em, description=description_em)
        await ctx.send(embed=em)


@bot.command()
@commands.check(is_it_me)
async def test(ctx):
    button = Button(label="Test button!", style=discord.ButtonStyle.green, emoji="👋")
    button2 = Button(emoji="😊")
    button3 = Button(label="red", style=discord.ButtonStyle.red)
    button4 = Button(label="my yt", url="https://www.youtube.com/channel/UCH-QFhiX-G8FFjQp8oL9_2A")

    view = View()
    view.add_item(button)
    view.add_item(button2)
    view.add_item(button3)
    view.add_item(button4)

    await ctx.send("Test button command!", view = view)


@bot.command()
@commands.check(is_it_me)
async def modapps(ctx):
    await ctx.send("Mod apps are now **OPEN**: https://forms.gle/kDBwcC8BQHe2YQkX9")


@bot.slash_command(pass_context=True)
async def timeout(ctx, target: Option(discord.Member, "The member you want to timeout"), time: Option(int, "Time you want to time them out for"), time_unit: Option(str, "Time unit", choices=["s", "min", "h", "d"]),  reason: Option(str, "Reason", required=False, default="No reason was specified.")):
    if not ctx.author.guild_permissions.moderate_members:
        await ctx.respond("<:Slimey_x:933232568055267359> You have no permission to timeout members!", ephemeral=True)
        return

    duration = None
    time_unit_text = None

    if time_unit == "s":
        duration = time * 1
        time_unit_text = "Second(s)"
    elif time_unit == "min":
        duration = time * 60
        time_unit_text = "Minute(s)"
    elif time_unit == "h":
        duration = time * 3600
        time_unit_text = "Hour(s)"
    elif time_unit == "d":
        duration = time * 86400
        time_unit_text = "Day(s)"

    time_to_timeout = datetime.timedelta(seconds=duration)
    try:
        await target.timeout_for(time_to_timeout, reason=reason)
    except discord.HTTPException:
        await ctx.respond("I don't have the permission to do that.", ephemeral=True)
        return

    timeout_embed = discord.Embed(
        title=f"Timed {target} out", color=discord.Colour.blue())
    timeout_embed.add_field(
        name="Server", value=f"{ctx.guild.name}", inline=True)
    timeout_embed.add_field(
        name="Responsible moderator", value=f"<@{ctx.author.id}>", inline=True)
    timeout_embed.add_field(
        name="Target", value=f"<@{target.id}>", inline=True)
    timeout_embed.add_field(
        name="Time", value=f"{time} {time_unit_text}", inline=True)
    timeout_embed.add_field(
        name="Reason", value=f"```{reason}```", inline=True)

    await ctx.respond(embed=timeout_embed)

    try:
        timeout_embed = discord.Embed(
            title=f"You have been timed out!", description=f"You have been timed-out on {ctx.guild.name} for {time} {time_unit_text}!\nReason: ```{reason}```", color=discord.Colour.blue())
        await target.send(embed=timeout_embed)
    except discord.errors.DiscordException:
        pass

    await asyncio.sleep(duration)
    try:
        timeout_over_embed = discord.Embed(
            title=f"Your timeout has expired", description=f"Your timeout on {ctx.guild.name} for {time} {time_unit_text} has expired.", color=discord.Colour.blue())
        await target.send(embed=timeout_over_embed)
    except discord.errors.DiscordException:
        pass



@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member = None, *, reason=None):

    if member==None:
        await ctx.reply("<:Slimey_x:933232568055267359> Please specify a member to kick")
    
    else:

        if reason==None:

            reason="No reason was specified"

        await ctx.guild.kick(member)
        
        em = discord.Embed(title = f"<:Slimey_tick:933232568210436136> Kicked successfully", color = discord.Color.green())
        em.add_field(name = "Member", value = f"Name: {member.name}" + "\n" + f"ID: {member.id}")
        em.add_field(name = "Reason", value = f"{reason}")
        
        await ctx.sfend(embed = em)


@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member == None, *, reason = None):

    if member==None:
        await ctx.send("<:Slimey_x:933232568055267359> Please specify a member to ban")
    
    else:

        if reason==None:

            reason="No reason was specified"
            
        await member.ban(reason = reason)

        em = discord.Embed(title = f"<:Slimey_tick:933232568210436136> Banned successfully", color = discord.Color.green())
        em.add_field(name = "Member", value = f"Name: {member.name}" + "\n" + f"ID: {member.id}")
        em.add_field(name = "Reason", value = f"{reason}")

        await ctx.send(embed = em)


@bot.command()
async def vote(ctx):

    button = Button(label="Top.gg", url="https://top.gg/bot/915488552568123403/vote")

    view = View()
    view.add_item(button)

    await ctx.send("Vote this bot on top.gg!", view = view)


@bottleflip.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"<:Slimey_x:933232568055267359> Slow it down bro!",
                           description=f"Try again in {error.retry_after:.2f}s.", color=discord.Colour.red())
        await ctx.send(embed=em)


@report.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"<:Slimey_x:933232568055267359> Slow it down bro!",
                           description=f"Try again in {error.retry_after:.2f}s.", color=discord.Colour.red())
        await ctx.send(embed=em)


@rps.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"<:Slimey_x:933232568055267359> Slow it down bro!",
                           description=f"Try again in {error.retry_after:.2f}s.", color=discord.Colour.red())
        await ctx.send(embed=em)


@coinflip.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"<:Slimey_x:933232568055267359> Slow it down bro!",
                           description=f"Try again in {error.retry_after:.2f}s.", color=discord.Colour.red())
        await ctx.send(embed=em)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):

        em = discord.Embed(title="<:Slimey_x:933232568055267359> Permission Error",
                           description="You don't have the permission(s) to do that!", color=discord.Colour.red())

        await ctx.reply(embed=em)



update_odds()


bot.run(conf["token"])
#OTE1NDg4NTUyNTY4MTIzNDAz.YacVJw.cTMdj9INhXSTguBGBwKGToiahrc