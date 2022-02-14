import discord
from discord.ext import commands

class ChannelEditing(commands.Cog):
    def init(self, bot):
        self.bot = bot
    
    @commands.command(aliases = ["cc", "createtextchannel"])
    @commands.has_permissions(manage_messages=True)
    async def createchannel(self, ctx, channel_name):
        guild = ctx.guild
        channel = await guild.create_text_channel(channel_name)

    @commands.command(aliases = ["sm"])
    @commands.has_permissions(manage_messages=True)
    async def slowmode(ctx, seconds: int = 0):

        if seconds > 21600:
            
            await ctx.reply("The limit for slow mode is 21600 seconds(6 hours)!")

        else:

            if seconds == 0:
                await ctx.channel.edit(slowmode_delay=seconds)
                await ctx.reply("Reset slow mode to 0 seconds!")
            
            else:
                await ctx.channel.edit(slowmode_delay=seconds)
                await ctx.send(f"Set the slowmode in this channel to {seconds} seconds!")
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):

            em = discord.Embed(title="<:Slimey_x:933232568055267359> Permission Error",
                            description="You don't have the permission(s) to do that!", color=discord.Colour.red())

        await ctx.reply(embed=em)

def setup(bot):
    bot.add_cog(ChannelEditing(bot))