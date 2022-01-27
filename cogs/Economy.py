import random
from discord.ext import commands
import sqlite3

conn = sqlite3.connect("slimeybot.db")
curs = conn.cursor()

class Economy(commands.Cog):
    def init(self, bot):
        self.bot = bot

    @commands.command()
    async def work(self, ctx):
        responses_good = curs.execute("SELECT response FROM economy_responses WHERE TYPE IS 1").fetchall()
        responses_bad = curs.execute("SELECT response FROM economy_responses WHERE TYPE IS 2").fetchall()

        # responses_good = ["You worked as a pizza delivery boy", "You worked as Discord mod", "You worked at a pizza place", "You worked as a chef"]
        # responses_bad = ["You were caught stealing", "You lied to your parents", "You got caught stealing a cookie", "You ate pizza with pinnaples on it"]
        i = random.randint(1,5)
        if i <= 4:
            r = random.choice(responses_good[0])
            money_s = "and earned"
        else:
            r = random.choice(responses_bad[0])
            money_s = "and lost"
        money = random.randint(50,500)
        await ctx.send(f"[Early Beta]\n💰{r} {money_s} {money}$!")

def setup(bot):
    bot.add_cog(Economy(bot))
