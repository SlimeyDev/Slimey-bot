import asyncio
import discord
from discord.ext import commands


bot = commands.Bot(command_prefix=".", help_command=None)

# class MyClient(discord.Client):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # create the background task and run it in the background
#         self.bg_task = self.loop.create_task(self.my_background_task())

#     async def on_ready(self):
#         print(f"Logged in as {self.user} (ID: {self.user.id})")
#         print("------")

#     async def my_background_task(self):
#         await self.wait_until_ready()
#         counter = 0
#         channel = self.get_channel(925322820458782750)  # channel ID goes here
#         while not self.is_closed():
#             counter += 1
#             await channel.send(counter)
#             await asyncio.sleep(60)  # task runs every 60 seconds


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")



# client = MyClient()
bot.run("OTI0NTc3NDMxOTg0MTQ0Mzk0.Ycgl1Q.68y0DVTJrQ8zfIHOcE1IFdNCWbQ")