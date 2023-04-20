import discord
from discord.ext import commands
import openai
import os
from dotenv import load_dotenv

class ai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def askGPT(self, ctx, *, asking: str = None):
        if asking == None:
            await ctx.reply(":red_circle:Please enter text to ask ChatGPT.")
        else:
            await ctx.reply("chatGPT is thinking, this might take a while...", mention_author=False)
            load_dotenv()
            key = str(os.environ.get("OPEN_AI"))
            openai.api_key = key
            messages = []
            system_msg = "cat"
            messages.append({"role": "system", "content": system_msg})
            messages.append({"role": "user", "content": asking})
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            reply = response["choices"][0]["message"]["content"]
            messages.append({"role": "assistant", "content": reply})
            await ctx.reply("ChatGPT says:\n"+str(reply))

def setup(bot):
    bot.add_cog(ai(bot))