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



bot.run("OTI0NTc3NDMxOTg0MTQ0Mzk0.Ycgl1Q.2T-vJSp_xl1OUJxTmvdL1IwGlxk")