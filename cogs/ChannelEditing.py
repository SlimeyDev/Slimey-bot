import discord
from discord.ext import commands

class ChannelEditing(commands.Cog):
    def init(self, bot):
        self.bot = bot
    
    @commands.command(aliases = ["cc", "createtextchannel"])
    @commands.has_permissions
    async def createchannel(self, ctx, channel_name):
        guild = ctx.guild
        channel = await guild.create_text_channel(channel_name)

    # @commands.command(aliases = ["cv", "createvoicechannel"])
    # @commands.has_permissions
    # async def createvoice(self, ctx, channel_name):
    #     guild = ctx.guild
    #     channel = await guild.create_text_channel(channel_name)

    @commands.command(aliases = ["sm"])
    @commands.cooldown(1, 5, commands.BucketType.user)
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