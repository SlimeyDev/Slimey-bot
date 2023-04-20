import discord
from discord.ext import commands
from PIL import Image
from io import BytesIO
import asyncio

class utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def youtube(self, ctx):
        await ctx.reply("SlimeyDev's youtube channel:\nhttps://www.youtube.com/channel/UCH-QFhiX-G8FFjQp8oL9_2A\nGO DROP ME A SUB!")

    @commands.command()
    async def website(self, ctx):
        await ctx.reply("You can view SlimeyDev's website through this link: https://slimeydev.github.io")
    
    @commands.command()
    async def report(self, ctx):
        em = discord.Embed(title="Report problems!", url="https://forms.gle/enMgTqXoVcYzm59a9",
                        description="Click the title to report a bug/problem!", color=discord.Color.gold())
        await ctx.reply(embed=em)
    
    @commands.command()
    async def rip(self, ctx, target: discord.Member = None):
        if target == None:
            target = ctx.author
        rip = Image.open("rip.jpg")
        asset = target.avatar
        data = BytesIO(await asset.read())
        pic = Image.open(data)
        pic = pic.resize((213, 213))
        rip.paste(pic, (337, 215))
        rip.save("rip_gen.jpg")
        await ctx.send(file = discord.File("rip_gen.jpg", filename="rip.jpg"))
    
    @commands.command()
    async def countdown(self, ctx, count=10):
        if count > 100:
            await ctx.send("The maximum allowed value is 100.")
            return
        current_count = count+1

        for i in range(count):
            current_count += -1
            await ctx.send(str(current_count))
            await asyncio.sleep(1)
        await ctx.send("**0**")
    
def setup(bot):
    bot.add_cog(utility(bot))