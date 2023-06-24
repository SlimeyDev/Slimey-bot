import discord
import datetime
import asyncio
from discord.ext import commands

class moderation(commands.Cog):
    #initializing cog
    def __init__(self, bot):
        self.bot = bot
    
    #commands
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def kick(self, ctx, user: discord.Member = None, *, reason=None):
        if user==None:
            await ctx.reply(":red_circle: Please specify a member to kick")
    
        else:

            if reason==None:

                reason="No reason was specified"

            await user.kick(reason=reason)
            embed = discord.Embed(title = f":green_circle: Kicked successfully", color = discord.Color.green())
            embed.add_field(name = "Member", value = f"Name: {user.name}" + "\n" + f"ID: {user.id}")
            embed.add_field(name = "Reason", value = f"{reason}")
            await user.send(embed=embed)
            await ctx.reply(embed=embed)
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def ban(self, ctx, member: discord.Member = None, *, reason=None):
        if member==None:
            await ctx.reply(":red_circle: Please specify a member to ban")
    
        else:

            if reason==None:

                reason="No reason was specified"

            await member.ban(reason=reason)

            embed = discord.Embed(title = f":green_circle: Banned successfully", color = discord.Color.green())
            embed.add_field(name = "Member", value = f"Name: {member.name}" + "\n" + f"ID: {member.id}")
            embed.add_field(name = "Reason", value = f"{reason}")
            await member.send(embed=embed)
            await ctx.reply(embed=embed)
    
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int=5):

        await ctx.channel.purge(limit=amount + 1)
    
    @commands.command(aliases = ["sm"])
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, seconds: int = 0):
        if seconds > 21600:
            
            await ctx.reply(":red_circle:The limit for slow mode is 21600 seconds(6 hours)!")

        else:
            if seconds > 0:
                await ctx.channel.edit(slowmode_delay=seconds)
                await ctx.reply(f"Set the slowmode in this channel to {seconds} seconds!")
            elif seconds == 0:
                await ctx.channel.edit(slowmode_delay=seconds)
                await ctx.reply("Disabled slowmode!")

#adding cog
def setup(bot):
    bot.add_cog(moderation(bot))