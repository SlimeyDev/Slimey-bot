import discord
from discord.ext import commands
from PIL import Image
from io import BytesIO
import asyncio
import requests
import json
import wikipedia

class utility(commands.Cog):
    #initializing cog
    def __init__(self, bot):
        self.bot = bot
        self.sniped_messages = {}
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        # Store the deleted message in the sniped_messages dictionary
        self.sniped_messages[message.channel.id] = {
            'content': message.content,
            'author': message.author.name
        }

    #commands
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
    
    @commands.command()
    async def weather(self, ctx, location = None):
        if location == None:
            await ctx.send("Please include a location!")
            return

        response = requests.get(f"https://pixel-api-blvw.onrender.com/data/weather/?location={location}")
        json_data = json.loads(response.text)
        if "error" in json_data:
            if json_data["error"] == "Location not found":
                await ctx.send("I didn't find that city/location.")
            else:
                await ctx.send("Unknown Error. :person_shrugging:")
            return

        resp_location = json_data["info"]["location"]
        resp_country = json_data["info"]["country"]
        #resp_region = json_data["info"]["region"]
        resp_temp = json_data["weather"]["temp_c"]
        resp_temp_feel = json_data["weather"]["feels_c"]
        resp_desc = json_data["weather"]["condition"]
        resp_ico = json_data["weather"]["icon"]

        if float(resp_temp_feel) <4:
            color = 0x153db0
        elif float(resp_temp_feel) <4:
            color = 0x3a80d3
        elif float(resp_temp_feel) <8:
            color = 0x3ad3c5
        elif float(resp_temp_feel) <15:
            color = 0xf0da3d
        elif float(resp_temp_feel) <20:
            color = 0xf08e3d
        elif float(resp_temp_feel) <25:
            color = 0xf0633d
        elif float(resp_temp_feel) <30:
            color = 0xf31106
        elif float(resp_temp_feel) <35:
            color = 0xc40900
        embed = discord.Embed(color=discord.Colour(color), title=f"Weather in {resp_location} ({resp_country})", description=f"**`Temperatur`:** {resp_temp} °C\n"
        f"**`Feels like`:** {resp_temp_feel} °C\n"
        f"**`Description`:** {resp_desc}\n\nWind and humidity coming soon!")
        embed.set_thumbnail(url=resp_ico)
        embed.set_footer(icon_url=ctx.author.avatar.url, text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)
    
    @commands.command()
    async def avatar(self, ctx, target: discord.Member = None):
        if target == None:
            target = ctx.author
  
              
        em = discord.Embed(title = f"{target.name}'s Avatar")
        em.set_footer(icon_url=ctx.author.avatar, text=f"Requested by {ctx.author.name}")
        em.set_image(url=target.avatar.url)
        await ctx.send(embed = em)
    
    @commands.command()
    async def snipe(self, ctx):
        # Check if there is a sniped message in the current channel
        if ctx.channel.id in self.sniped_messages:
            sniped_message = self.sniped_messages[ctx.channel.id]
            # Retrieve and send the sniped message
            embed = discord.Embed(
                title="Sniped Message",
                description=sniped_message['content'],
                color=0x00FF00  # You can customize the color as desired
            )
            embed.set_footer(text=f"Sent by {sniped_message['author']}")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="No Sniped Message",
                description="No recently deleted messages to snipe.",
                color=0xFF0000  # You can customize the color as desired
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def wiki(ctx,*, query):
        try:
            results = wikipedia.summary(query, sentences=10)
            embed = discord.Embed(title=query, description=results, color=discord.Color.green())
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title=":red_circle: An Error Occured!", description="This topic is either not on wikipedia or there has been an internal error.", color=discord.Color.red())
            await ctx.send(embed=embed)
    
#adding cog
def setup(bot):
    bot.add_cog(utility(bot))