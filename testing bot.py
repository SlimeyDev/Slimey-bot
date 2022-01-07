import discord
from discord import emoji
from discord import user
from discord.commands import context
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.core import guild_only
from discord.flags import alias_flag_value
from discord.ui import Button, View
import json
import os
import random

os.chdir("C:\\Users\\Nesar.K\\Desktop\\Testing bot\\mainbank.json")

bot = commands.Bot(command_prefix=".", help_command=None)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.command()
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


bot.command(aliases = ["bal"])
async def balance(ctx):
    await open_account(ctx.author)

    user = ctx.author
    users = get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title =  f"{ctx.author.name}'s balance", color = discord.Color.blue())
    em.add_field(name = "Wallet balance", value = wallet_amt)
    em.add_field(name = "Bank balance", value = bank_amt)

    await ctx.send(embed = em)


@bot.command()
async def beg(ctx):
    await open_account(ctx.author)

    users = get_bank_data()

    user = ctx.author

    earnings = random.randrange(101)

    await ctx.send(f"Someone gave you {earnings} coins!")

    wallet_amt = users[str(user.id)]["wallet"] + earnings

    with open("mainbainkk.json", "w") as f:
        json.dump(users, f)


async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:

        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbainkk.json", "w") as f:
        json.dump(users, f)
    return True


async def get_bank_data():
    with open("mainbainkk.json", "r") as f:
        users = json.load(f)
    
    return users


bot.run("OTI0NTc3NDMxOTg0MTQ0Mzk0.Ycgl1Q.2T-vJSp_xl1OUJxTmvdL1IwGlxk")