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

os.chdir("C:\\Users\\Nesar.K\\Desktop\\pycord")

bot = commands.Bot(command_prefix=".")


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


@bot.command(aliases = ["bal"])
async def balance(ctx):
    await open_account(ctx.author)

    user = ctx.author
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title =  f"{ctx.author.name}'s balance", color = discord.Color.blue())
    em.add_field(name = "Wallet balance", value = wallet_amt)
    em.add_field(name = "Bank balance", value = bank_amt)

    await ctx.send(embed = em)


@bot.command()
async def beg(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()

    user = ctx.author

    earnings = random.randint(1,101)

    await ctx.send(f"Someone gave you {earnings} coins!")

    wallet_amt = users[str(user.id)]["wallet"]  =+ earnings

    with open("mainbank.json", "w") as f:
        json.dump(users, f)


async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:

        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True


@bot.command()
async def withdraw(ctx, amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Please specify a value to withdraw!")
        return
    
    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount>bal[1]:
        await ctx.send("You dont have that much money!")
        return

    if amount>0:
        await ctx.send("Amount musst be positive!")
        return

    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -1 * amount, "bank")

    await ctx.send(f"you withdrew {amount} coins")

async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    
    return users

async def update_bank(user, change = 0, mode = "wallet"):
    users = await get_bank_data

    users[str(user.id)][mode] += change

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    
    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return bal


bot.run("OTI0NTc3NDMxOTg0MTQ0Mzk0.Ycgl1Q.2T-vJSp_xl1OUJxTmvdL1IwGlxk")