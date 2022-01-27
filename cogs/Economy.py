import random
from discord.ext import commands

class Economy(commands.Cog):
    def init(self, bot):
        self.bot = bot

    @commands.command()
    async def work(self, ctx):

        responses_good = ["You worked as a pizza delivery boy", "You worked as Discord mod"]
        responses_bad = ["You were caught stealing", "You lied to your parents"]
        i = random.randint(1,2)
        if i == 1:
            r = random.choice(responses_good)
            s = ""
            money_s = "earned"
        if i == 2:
            r = random.choice(responses_bad)
            s = ""
            money_s = "losed"
        money = random.randint(50,500)
        await ctx.send(f"[Early Beta]\n{r} and {money_s}€!")

def setup(bot):
    bot.add_cog(Economy(bot))
