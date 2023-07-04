import discord
from discord.ext import commands
from discord.ext.commands.bot import Bot
import psutil
import platform
import time
import shutil
import socket
import os
from dotenv import load_dotenv
import requests
from online import keep_online

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="<", help_command=None, intents=intents)


@bot.event
async def on_ready():
  print("=" * 50)
  print("Bot starting...")
  print("-" * 50)
  print("Loading stats...")
  #loading stats
  global members
  global stats
  global channels
  global start_time
  global owners
  owners = [986619341132951562]
  members = sum([guild.member_count for guild in bot.guilds])
  channels = 0
  for guild in bot.guilds:
    channels += len(guild.channels)
  stats = {"guilds": len(bot.guilds), "users": members, "channels": channels}
  print("Current stats:", stats)
  global bot_version
  bot_version = "20.2.0"
  global cpu_usage, ram_usage, python_version, os_system, os_release, disk_stats
  start_time = int(time.time())
  cpu_usage = psutil.cpu_percent(4)
  ram_usage = psutil.virtual_memory()[2]
  python_version = platform.python_version()
  os_system = platform.system()
  os_release = platform.release()
  total, used, free = shutil.disk_usage("/")
  disk_stats = f"**Disk** Total: %d MB" % (
    total // (2**30)) + "\n Used: %d MB" % (
      used // (2**30)) + "\n Free: %d MB" % (free // (2**30)) + "\n"
  host = socket.gethostname()
  print("All stats loaded!")
  print("-" * 50)
  print("Loading cogs...")
  # initialization of cogs
  bot.load_extension('cogs.moderation')
  bot.load_extension('cogs.fun')
  bot.load_extension('cogs.utility')
  print("All cogs loaded!")
  print("-" * 50)
  Bot_Status = f"{len(bot.guilds)} servers | <help"
  await bot.change_presence(status=discord.Status.online,
                            activity=discord.Activity(
                              type=discord.ActivityType.watching,
                              name=Bot_Status))
  print(f"Logged in as {bot.user} (ID: {bot.user.id})")
  print("Bot is ready!")
  #sending message in bot status channel
  channel = bot.get_channel(1097962463661670480)
  em = discord.Embed(
    title="Bot status",
    description="Bot is online and all systems are operational!",
    color=discord.Colour.green())
  em.set_thumbnail(url="https://i.ibb.co/9t7bbhY/Slimey.jpg")
  await channel.send(embed=em)
  response = requests.get("https://discordstatus.com/api/v2/status.json")
  json_data = response.json()
  status = json_data["status"]["description"]
  if status == "All Systems Operational":
    color = 0xA9F37F
    text = f"Discord works! – {status}"
  else:
    color = 0xF37F7F
    text = f"It looks like something is not working at the moment:\n{status}"
  em = discord.Embed(colour=discord.Colour(color),
                     title="Discord Status",
                     description=text)
  em.set_thumbnail(url="https://i.ibb.co/0Cz6QWz/Discord.png")
  await channel.send(embed=em)
  print("=" * 50)


#sending a message when pinged
@bot.event
async def on_message(message):
  if message.content == "<@!990460875309723659>" or message.content == "<@990460875309723659>":
    await message.channel.send(
      f'My prefix is **`<`**. Type "<help" for all the commands!')
  await bot.process_commands(message)


#send a message when the bot joins a server
@bot.event
async def on_guild_join(guild):

  embed = discord.Embed(
    color=discord.Color(0xC77FF3),
    title="Hey! I'm Slimey",
    description=
    "Thanks for adding me to your server!\nType `<help` for commands and `<info` for some information on the bot and the owner of this bot!"
  )
  embed.set_thumbnail(url="https://i.ibb.co/9t7bbhY/Slimey.jpg")
  embed.set_footer(icon_url="https://i.ibb.co/9t7bbhY/Slimey.jpg",
                   text="Slimey bot")
  try:
    joinchannel = guild.system_channel
    await joinchannel.send(embed=embed)
  except:
    await guild.text_channels[0].send(embed=embed)


#important functions


def is_it_me(ctx):
  if ctx.author.id in owners:
    return ctx.author.id


#commands
@bot.command()
async def ping(ctx):
  em = discord.Embed(title="Pong!",
                     description=f"{round(bot.latency*1000)}ms",
                     color=discord.Colour.purple())

  await ctx.reply(embed=em)


@bot.command()
async def help(ctx, mode: str = None):
  if mode == None:
    em = discord.Embed(
      title="Current commands:",
      description=f"`<help fun`, `<help moderation`, `<help utility`",
      color=discord.Color.gold())
    em.add_field(name="Prefix", value=f"My prefix is '`<`'..", inline=False)
    await ctx.reply(embed=em)
  else:
    if mode == "fun":
      em = discord.Embed(
        title="😂 Fun commands:",
        description=
        f"`<dadjoke`\n`<inspire`\n`<magic8ball`\n`<yesorno`\n`<sayweird`\n`<say`\n`<password`\n`/rip`\n`<kill`\n`<fox`\n`<hack`\n`<ip`\n`<coinflip`\n`<rps`",
        color=discord.Color.green())

      await ctx.reply(embed=em)

    elif mode == "moderation":
      em = discord.Embed(
        title="🔒 Moderation commands:",
        description=f"`<kick`\n`<ban`\n`<timeout`\n`<clear`\n`<slowmode`",
        color=discord.Color.red())

      await ctx.reply(embed=em)
    elif mode == "utility":
      em = discord.Embed(
        title="👀 Utility/other commands:",
        description=
        f"`<youtube`\n`<website`\n`<invite`\n`<report`\n`<info`\n`/avatar`\n`<countdown`\n`<discord`\n`<ping`",
        color=discord.Color.purple())

      await ctx.reply(embed=em)


@bot.command()
@commands.check(is_it_me)
async def stats(ctx):
  await ctx.message.add_reaction('🔄')
  members = sum([guild.member_count for guild in bot.guilds])
  channels = 0
  for guild in bot.guilds:
    channels += len(guild.channels)

  stats = {"guilds": len(bot.guilds), "users": members, "channels": channels}
  total, used, free = shutil.disk_usage("/")
  disk_stats = f"**Disk**" + "\n" + "Total: %d GB" % (
    total // (2**30)) + "\n Used: %d GB" % (
      used // (2**30)) + "\n Free: %d GB" % (free // (2**30)) + "\n"

  info = (
    f'__**CURRENT Stats**__\n\nTotal users: {stats["users"]}\nTotal channels: {stats["channels"]}\nGuilds: {stats["guilds"]}\n--------------------\n'
    f"**Last restarted** <t:{start_time}:R>\n"
    f"**CPU usage** {psutil.cpu_percent(4)}%\n"
    f"**RAM usage** {psutil.virtual_memory()[2]}%\n"
    f"{disk_stats}\n"
    f"**Python-Version** {platform.python_version()}\n"
    f"**Bot-Version** {bot_version}\n"
    f"**OS info** {platform.system()} {platform.release()}\n\n"
    f"**API connection ping** {round(bot.latency * 1000)}ms")

  await ctx.send(info)
  await ctx.message.remove_reaction("🔄", bot.user)


@bot.command(aliases=["about", "botinfo", "bot"])
async def info(ctx):
  info = (
    f"Information on the bot: This bot was made using VS Code using the language Python. It's maintained by `slimeydev#5493`.\n"
    f':information_source: __**Stats**__\n\nTotal users: {stats["users"]}\nTotal channels: {stats["channels"]}\nGuilds: {stats["guilds"]}\n--------------------\n'
    f"**Last restarted** <t:{start_time}:R>\n"
    f"**CPU usage** {cpu_usage}%\n"
    f"**RAM usage** {ram_usage}%\n"
    f"{disk_stats}\n"
    f"**Python-Version** {python_version}\n"
    f"**Bot-Version** {bot_version}\n"
    f"**OS info** {os_system} {os_release}\n\n"
    f"**API connection ping** {round(bot.latency * 1000)}ms\n\n"
    f":information_source: **Note:** Because of performance reasons, the most stats are last updated on <t:{start_time}>."
  )

  await ctx.reply(info)


@bot.command()
async def invite(ctx):
  await ctx.reply(
    "You can invite this bot using this link: https://slimeydev.github.io/SlimeyBOT"
  )


@bot.command()
async def support(ctx):
  await ctx.reply(
    "You can join our support server from this link:\nhttps://discord.gg/f8WgAS733R"
  )


@bot.command(aliases=["discord", "isdiscorddown", "discorddown"])
async def discordstatus(ctx):
  response = requests.get("https://discordstatus.com/api/v2/status.json")
  json_data = response.json()
  status = json_data["status"]["description"]
  if status == "All Systems Operational":
    color = 0xA9F37F
    text = f"Discord works! – {status}"
  else:
    color = 0xF37F7F
    text = f"It looks like something is not working at the moment:\n{status}"
  em = discord.Embed(colour=discord.Colour(color),
                     title="Discord Status",
                     description=text)
  em.set_thumbnail(url="https://i.ibb.co/0Cz6QWz/Discord.png")
  await ctx.reply(embed=em, mention_author=False)

#setting up server to keep bot online
keep_online()
#loading TOKEN from env
load_dotenv()
#logging into bot using TOKEN
bot.run(os.environ.get("TOKEN"))
