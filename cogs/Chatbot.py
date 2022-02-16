import discord
from discord.ext import commands
import asyncio
import random
import requests
import urllib
import sqlite3

conn = sqlite3.connect("slimeybot.db")
c = conn.cursor()

def is_it_me(ctx):
    owners = 830751616927268884, 873079348855472148
    if ctx.author.id in owners:
        return ctx.author.id

class Chatbot(commands.Cog):
    def init(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if message.channel.id == 943424168593063967:


            author_input = urllib.parse.quote(message.content, safe="")

            chat_endpoint = f"https://pixel-api-production.up.railway.app/fun/chatbot/?message={author_input}?name="
            await asyncio.sleep(random.uniform(0.6,2))
            async with message.channel.typing():
                await asyncio.sleep(random.uniform(0.2,0.6))

                chat_response = requests.get(chat_endpoint).json()
                chat_message = chat_response["message"]
            await message.reply(chat_message, mention_author=False)


    @commands.command()
    @commands.check(is_it_me)
    async def add_chatbot(self, ctx):
        m = await ctx.send("This channel will be the chatbot channel in a few seconds...")
        await asyncio.sleep(1)
        await m.edit("adding to database...")
        channel = ctx.channel.id
        server = ctx.guild.id
        c.execute("INSERT INTO chatbot VALUES(?,?)", (str(channel), str(server)))
        conn.commit()
        await m.edit("This channel is now the chatbot channel!")


def setup(bot):
    bot.add_cog(Chatbot(bot))

conn.close()