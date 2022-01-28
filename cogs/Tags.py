import discord
import random
from discord.ext import commands
import sqlite3
import asyncio
conn = sqlite3.connect("slimeybot.db")
curs = conn.cursor()

class Tags(commands.Cog):
    def init(self, bot):
        self.bot = bot

    @commands.command()
    async def tag(self, ctx, *, name: str = None):
        prefix = curs.execute(f"SELECT prefix FROM custom_prefixes WHERE guild = ?", (ctx.guild.id,)).fetchone()
        prefix = prefix[0]
        if not prefix:
            prefix = "<"
        else:
            prefix = prefix
        if not name:
            await ctx.send(f"What's the name of the tag which content you want to see?\n**Usage: `{prefix}tag <name>`**")
            return
        # if method == "create":
        #     pass
        # elif method == "delete" or "remove":
        #     pass
        # elif method == "transfer":
        #     pass    
        # elif method == "edit":
        #     pass
        # elif method == "help":
        #     pass
        # elif method == "info":
        #     pass
        # elif method == "list":
        #     pass
        # elif method == "search":
        #     pass
        # else:
        #     pass

        name_s = name
        if len(name) >= 20:
            name_s = f'{name[:20]}… '
        data = curs.execute("SELECT name FROM tags WHERE name=? AND guild=?",(name,ctx.guild.id)).fetchall()
        if not data:
            await ctx.send(f'The tag "{name_s}" doesn\'t exists. Please use the command `{prefix}tag_create {name_s}` instead.')
            return
        tag_description = curs.execute("SELECT description FROM tags WHERE guild = ? AND name = ?", (ctx.guild.id, name)).fetchone()
        await ctx.message.add_reaction('✅')
        await ctx.send(tag_description[0])
    @commands.command()
    async def tag_create(self, ctx, name=None, description=None):
        if not name or not description:
            await ctx.send("Please include a `name` and a `description` for the tag.")
            return
        if len(name) > 55:
            await ctx.send("Please don't choose a higher value than 55 for the `name` of the tag.")
            return
        if len(description) > 500:
            await ctx.send("Please don't choose a higher value than 500 for the `description` of the tag.")
            return
        data = curs.execute("SELECT name FROM tags WHERE name=? AND guild=?",(name,ctx.guild.id)).fetchall()
        prefix = curs.execute(f"SELECT prefix FROM custom_prefixes WHERE guild IS {ctx.guild.id}").fetchone()
        prefix = prefix[0]

        if not prefix:
            prefix = "<"
        else:
            prefix = prefix
        name_s = name
        if len(name) >= 20:
            name_s = f'{name[:20]}… '
        if data:
            await ctx.send(f'The tag "{name_s}" already exists. Please use the command `{prefix}tag_edit {name_s}` instead or delete this tag first with `{prefix}tag_delete {name_s}`. (coming soon)')
            return
        em = discord.Embed(title="Successfully created tag", color=discord.Color.green(), description=f"Tag created.\n**Creator:** {ctx.author.mention}\n**Tag name:** {name}\n**Tag description:** {description}")
        em.set_footer(text=f"You can see the content of the tag with {prefix}tag {name_s}")
        curs.execute("""
        
        INSERT INTO tags(guild,creator,current_owner,name,description) 
               VALUES (?,?,?,?,?);""", (ctx.guild.id,ctx.author.id,ctx.author.id,name,description))
        conn.commit()
        await ctx.send(embed=em)
    @commands.command()
    async def tag_edit(self, ctx, name=None, description=None):
        if not name or not description:
            await ctx.send("Please include a `name` and a `description` for the tag.")
            return
        if len(name) > 55:
            await ctx.send("Please don't choose a higher value than 55 for the `name` of the tag.")
            return
        if len(description) > 500:
            await ctx.send("Please don't choose a higher value than 500 for the `description` of the tag.")
            return
        data = curs.execute("SELECT name FROM tags WHERE name=? AND guild=?",(name,ctx.guild.id)).fetchall()
        prefix = curs.execute(f"SELECT prefix FROM custom_prefixes WHERE guild IS {ctx.guild.id}").fetchone()
        prefix = prefix[0]

        if not prefix:
            prefix = "<"
        else:
            prefix = prefix
        name_s = name
        if len(name) >= 20:
            name_s = f'{name[:20]}… '
        if not data:
            await ctx.send(f'The tag "{name_s}" doesn\'t exists. Please use the command `{prefix}tag_create {name_s}` instead to create a new tag.')
            return
        curs.execute("""
        
        UPDATE tags SET guild=?,creator=?,current_owner=?,name=?,description=? WHERE guild=? AND name=?""", (ctx.guild.id,ctx.author.id,ctx.author.id,name,description,ctx.guild.id,name))
        conn.commit()
        creator = curs.execute("SELECT creator FROM tags WHERE guild=? AND name=?", (ctx.guild.id,name)).fetchone()
        em = discord.Embed(title="Successfully updated tag", color=discord.Color.green(), description=f"Tag updated.\n**Creator:** <@{creator[0]}>\n**Tag name:** {name}\n**Tag description:** {description}")
        em.set_footer(text=f"You can see the content of the tag with {prefix}tag {name_s}")
        await ctx.send(embed=em)
def setup(bot):
    bot.add_cog(Tags(bot))
