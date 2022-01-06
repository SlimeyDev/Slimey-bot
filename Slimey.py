import discord
from discord import embeds
from discord import colour
from discord import asset
from discord import message
from discord import channel
from discord.colour import Color
from discord.embeds import Embed
from discord.enums import Status
from discord.errors import ClientException
from discord.ext import commands, tasks
import json
from discord.ext.commands.bot import Bot
from discord.ext.commands.core import guild_only
import requests
import random
from requests.models import Response
import datetime
import os
import sys
import string
import secrets
bot = commands.Bot(command_prefix="<", help_command=None)


@bot.event
async def on_ready():
    update_odds.start()
    #f"{len(bot.guilds)} servers | <help"
    # status=discord.Status.idle
    # await bot.change_presence(status=discord.Status.online, activity=discord.ActivityType.watching, name=f"{len(bot.guilds)} servers | <help")
    Bot_Status = f"{len(bot.guilds)} servers | <help"
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=Bot_Status))
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("----------")


@tasks.loop(seconds=1)
async def update_odds():
    now = datetime.datetime.now()

    if now.hour == 12 and now.minute == 0 and now.second == 0:
        global megaflip
        global bottleflipvar
        megaflip = 0
        bottleflipvar = 0
        bottleflipvar = random.randint(30, 80)
        megaflip = random.randint(20, 60)


def is_it_me(ctx):
    owners = [830751616927268884, 899672685112594554]
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


@bot.command()
@commands.check(is_it_me)
async def restart(ctx):
    em = discord.Embed(title="Bot will be restarted",
                       description="The bot will restarting now", color=discord.Colour.purple())
    await ctx.reply(embed=em)
    # Restarting the bot
    os.execv(sys.executable, ['python'] + sys.argv)


@bot.command()
@commands.check(is_it_me)
async def update(ctx):
    em = discord.Embed(title="Bot will be updating",
                       description="I fetch new code now if available", color=discord.Colour.purple())
    await ctx.reply(embed=em)
    # Running git pull for getting last commit
    os.system("git pull")


@bot.command()
async def ping(ctx):
    em = discord.Embed(
        title="Pong !", description=f"{round(bot.latency*1000)}ms", color=discord.Colour.blue())

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


@bot.slash_command(description="testing slash command, work in progress...", guild_ids=[888382819427057714])
async def test(ctx):
    await ctx.respond("test slash command!")


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
    await ctx.reply("Information on the bot: This bot was made using VS Code using the language Python. It was made by a new creator TheSlimeyDevloper.")


@bot.command()
async def help(ctx):
    em = discord.Embed(
        title="Currently the existing commands are -", color=discord.Colour.blue())
    em.add_field(name="<coinflip", value="Flips a coin!", inline=False)
    em.add_field(name="<youtube",
                 value="Shows TheSlimeyDevloper's youtube.", inline=False)
    em.add_field(name="<info", value="Gives info on the bot.", inline=False)
    em.add_field(name="<bottleflip",
                 value="Flips a bottle! Well there are chances of getting something *rare*.", inline=False)
    em.add_field(
        name="<twitch", value="Show you TheSlimeyDevloper's twitch account.", inline=False)
    em.add_field(name="<inspire",
                 value="Sends you an insperational qoute!", inline=False)
    em.add_field(name="<dadjoke",
                 value="Sends u a stupid dadjoke -_-", inline=False)
    em.add_field(name="<ping", value="Tells you your latecy.", inline=False)
    em.add_field(
        name="<odds", value="Tells you your odds of getting a bottle flip!", inline=False)
    em.add_field(
        name="<invite", value="Sends an invite link to invite me to your server!", inline=False)
    em.add_field(name="<clear <value>",
                 value="Used to clear a bunch of messages!", inline=False)
    em.add_field(
        name="<report", value="Use this command to report bugs and problems on the bot!", inline=False)
    em.add_field(name="<say <value>", value="Sends the value!", inline=False)
    em.add_field(name="<magic8ball <question>",
                 value="Ask it a question and it will tell you your faith...", inline=False)
    em.add_field(name="<yesorno <question>",
                 value="Answers **Yes** or **No** to the question you entered", inline=False)
    em.add_field(name="<rps <value>",
                 value="Play some rock paper scissors wwwith me!", inline=False)
    em.add_field(name="<send_password <value>",
                 value="Generate some passwords!", inline=False)
    em.add_field(name="/send_meme", value="Sends a meme from reddit!")

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
            title="Oops!", description="Invalid respons! Please type a response that contains rock, paper, scissor and remember its case sensitive!", color=discord.Color.red())
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
async def say(ctx, *, message: str):
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
        embed = discord.Embed(title="Error", color=discord.Colour.red(
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
@commands.check(is_it_me)
async def embed(ctx, title_em="please enter the title!", description_em="please enter the description!"):
    em = discord.Embed(title=title_em, description=description_em)
    await ctx.send(embed=em)


@bot.command()
@commands.check(is_it_me)
async def test(ctx):
    emoji = '✅'
    await ctx.send(emoji)
    emoji = '❌'
    await ctx.send(emoji)
    await ctx.send("updated testing command ... again")


@bot.command()
@commands.check(is_it_me)
async def modapps(ctx):
    await ctx.send("Mod apps are now **OPEN**: https://forms.gle/kDBwcC8BQHe2YQkX9")


@bottleflip.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow it down bro!",
                           description=f"Try again in {error.retry_after:.2f}s.", color=discord.Colour.red())
        await ctx.send(embed=em)


@report.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow it down bro!",
                           description=f"Try again in {error.retry_after:.2f}s.", color=discord.Colour.red())
        await ctx.send(embed=em)


@rps.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow it down bro!",
                           description=f"Try again in {error.retry_after:.2f}s.", color=discord.Colour.red())
        await ctx.send(embed=em)


@coinflip.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow it down bro!",
                           description=f"Try again in {error.retry_after:.2f}s.", color=discord.Colour.red())
        await ctx.send(embed=em)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):

        em = discord.Embed(title="Permission Error",
                           description="You don't have the permission(s) to do that!", color=discord.Colour.red())

        await ctx.reply(embed=em)

bot.run("OTE1NDg4NTUyNTY4MTIzNDAz.YacVJw.DvgaNxLR__3LkjcaBhFe7wv-y7M")
