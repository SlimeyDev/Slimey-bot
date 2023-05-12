import discord
from discord.ext import commands
import datetime

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
    
    @commands.command()
    async def timeout(self, ctx, member: discord.Member = None, minutes: int = 10):

        if minutes > 0 and not member == None:
            duration = datetime.timedelta(minutes=minutes)
            await member.timeout_for(duration)
            await ctx.reply(f"{member} timed out for {minutes} minutes.")
        elif minutes == 0 or member == None:
            await ctx.reply(":red_circle: Parameter not mentioned!\n`<timeout [member] [time in minutes]`")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):

            em = discord.Embed(title=":red_circle: Permission Error",
                            description="You don't have the permission(s) to do that!", color=discord.Colour.red())

            await ctx.reply(embed=em)

#adding cog
def setup(bot):
    bot.add_cog(moderation(bot))