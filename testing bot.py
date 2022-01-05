import discord
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.core import guild_only


bot = commands.Bot(command_prefix=".", help_command=None)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


@bot.slash_command(description="Testing slash command, work in progress.", guild_ids=[888382819427057714])
async def test(ctx):
  await ctx.respond("test slash command")


bot.run("OTI0NTc3NDMxOTg0MTQ0Mzk0.Ycgl1Q.68y0DVTJrQ8zfIHOcE1IFdNCWbQ")