import discord
from discord.ext import commands
import requests
import json
import random
import string
import secrets
import asyncio
import socket
import struct

#important functions
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)


class Joke:
    setup = ""
    punchline = ""

    def __init__(self, setup, punchline):
        self.setup = setup
        self.punchline = punchline


def get_Joke():
    url = "https://dad-jokes.p.rapidapi.com/random/joke"
    headers = {
        'x-rapidapi-host': "dad-jokes.p.rapidapi.com",
        'x-rapidapi-key': "f54cc328d6msh97c78a7088ae219p185068jsn07d335d78fe6"
    }
    response = requests.request("GET", url, headers=headers)
    json_data = json.loads(response.text)
    setup = json_data["body"][0]["setup"]
    punchline = json_data["body"][0]["punchline"]
    joke = Joke(setup, punchline)
    return(joke)

class fun(commands.Cog):
    #initializing cog
    def __init__(self, bot):
        self.bot = bot
    
    #commands
    @commands.command()
    async def dadjoke(self, ctx):
        joke = get_Joke()
        sending_joke = joke.setup + "." + joke.punchline

        await ctx.reply(sending_joke)

    @commands.command()
    async def inspire(self, ctx):
        quote = get_quote()
        await ctx.reply(quote)

    @commands.command()
    async def inspire(self, ctx):
        quote = get_quote()
        await ctx.reply(quote)
    
    @commands.command(aliases=["ball", "8ball"])
    async def magic8ball(self, ctx, *, question: str):

        responses = ["It is certain.",
                    "It is decidedly so.",
                    "Without a doubt.",
                    "Yes - definitely.",
                    "You may rely on it.",
                    "As I see it, yes.",
                    "Most likely.",
                    "Get out before I eat your cat",
                    "Yes.",
                    "Signs point to yes.",
                    "Reply hazy, try again.",
                    "Ask again later.",
                    "Cannot predict now.",
                    "Concentrate and ask again.",
                    "My reply is no.",
                    "My sources say no.",
                    "Very doubtful.",
                    "ofc",
                    "I AM TRYING TO SLEEP",
                    "idk",
                    "sorry I dont answer nerds"]

        await ctx.reply(f"Question: {question}\nAnswer: {random.choice(responses)}")
    
    @commands.command(aliases=["yorn", "YorN"])
    async def yesorno(self, ctx):

        responses = ["Yes.", "No.", "nerd", "probs", "prob yes",
                    "prob no", "idk nerd", "most prob yes", "most prob no"]

        await ctx.reply(random.choice(responses))
    
    @commands.command()
    async def rps(self, ctx, response=None):
        if response == "rock" or response == "paper" or response == "scissor" or response == "scissors":

            botRes = random.choice(["rock", "paper", "scissor"])
            await ctx.reply(botRes)

            if botRes == response:
                await ctx.send("ITS A TIE!")
            elif botRes == "rock" and response == "paper":
                await ctx.send("You win!")
            elif botRes == "paper" and response == "rock":
                await ctx.send("I win!")
            elif botRes == "scissor" and response == "rock":
                await ctx.send("You win!")
            elif botRes == "rock" and response == "scissor":
                await ctx.send("I win!")
            elif botRes == "rock" and response == "scissors":
                await ctx.send("I win!")
            elif botRes == "paper" and response == "scissors":
                await ctx.send("You win!")
            elif botRes == "scissor" and response == "paper":
                await ctx.send("I win!")

        else:
            em = discord.Embed(
                title=":red_circle: Oops!", description="Invalid respons! Please type a response that contains rock, paper, scissor and remember its case sensitive!", color=discord.Color.red())
            await ctx.reply(embed=em)
    

    @commands.command(aliases=["weird", "weirdify", "upper_lower", "ul", "kek", "weirdsay"])
    async def sayweird(self, ctx, *, message: str = None):
        if message == None:
            await ctx.send(":red_circle: Please enter a message to send!")
        
        else:
            await ctx.message.delete()
            message = "".join([x.upper() if i % 2 != 0 else x for i, x in enumerate(message)])

            await ctx.send(message, allowed_mentions=discord.AllowedMentions.none())
    
    @commands.command()
    async def say(self, ctx, *, message: str = None):

        if message == None:
            await ctx.send(":red_circle: Please enter a message to send!")
        
        else:
            await ctx.message.delete()
            await ctx.send(message, allowed_mentions=discord.AllowedMentions.none())
    
    @commands.command(aliases=["ball", "8ball"])
    async def magic8ball(self, ctx, *, question: str):

        responses = ["It is certain.",
                    "It is decidedly so.",
                    "Without a doubt.",
                    "Yes - definitely.",
                    "You may rely on it.",
                    "As I see it, yes.",
                    "Most likely.",
                    "Get out before I eat your cat",
                    "Yes.",
                    "Signs point to yes.",
                    "Reply hazy, try again.",
                    "Ask again later.",
                    "Cannot predict now.",
                    "Concentrate and ask again.",
                    "Don't count on it.",
                    "My reply is no.",
                    "My sources say no.",
                    "Very doubtful.",
                    "nerd",
                    "I AM TRYING TO SLEEP",
                    "idk",
                    "sorry I dont answer nerds"]

        await ctx.reply(f"Question: {question}\nAnswer: {random.choice(responses)}")
    
    @commands.command()
    async def password(self, ctx, length):
        length = int(length)
        if length <= 100:
            if length < 4:
                embed = discord.Embed(
                    title="Error", color=discord.Colour.red(), description=f"Too small... :joy:")
                await ctx.respond(embed=embed)
                return
            chars = string.digits + string.ascii_letters + string.punctuation

            passwords = []

            for i in range(5):
                password = ''.join(secrets.choice(chars) for _ in range(length))
                passwords.append(password)

            embed = discord.Embed(title="Generated passwords", color=discord.Colour.blue(), description=f"I generated **5** passwords for you, which are **{length}** characters long.\n\n"
                                f"```txt\n{passwords[0]}\n{passwords[1]}\n{passwords[2]}\n{passwords[3]}\n{passwords[4]}```")

            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title=":red_circle: Error", color=discord.Colour.red(
            ), description=f"Please don't go higher than 100!")
            await ctx.respond(embed=embed)

    @commands.command()
    async def kill(self, ctx, target: discord.Member = None):
        if target == None:
            target = ctx.author
        
        kill = [
            " choked on a lego and died",
            " stepped on a lego and died",
            " died when they were writing their death note",
            " died.",
            " choked on a carrot and died",
            " died eating expired choclate",
            " tripped and died",
            " died due to WiLd DoG AtAcK",
            " died because they were looking at the microwave while cooking burrito's",
            " drowned to death ",
            " died because there mom killed them",
            " died because of shame",
            " died due to cold",
            " died because they were noob",
            " died after he found out he was alergic to air",
            " died after looking at his horrifying face",
            " died because he realised he was dead",
            " died cuz y not",
        ]

        message = f"{target}{random.choice(kill)}"

        await ctx.send(message)

    @commands.command(aliases=["randomfox"])
    async def fox(self, ctx):
        response = requests.get("https://randomfox.ca/floof/")
        json_data = json.loads(response.text)
        fox_image_url = json_data["image"]
        fox_link = json_data["link"]
        em = discord.Embed(color=discord.Colour(0xE97451), title="Random fox!", url=fox_link)
        em.set_image(url=fox_image_url)
        await ctx.send(embed=em)
    
    @commands.command(aliases=["get_ip"])
    async def ip(self, ctx, member: discord.Member = None):
        if member == None:
            await ctx.send("Please specify a member to get its ip address.")
            return
        elif member == ctx.author:
            await ctx.send("Please specify a member to get its ip address.")
            return
        generated_ip = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        m = await ctx.send("Starting IP grabber tool...")
        await asyncio.sleep(random.uniform(1, 2.5))
        await m.edit(f"Starting IP grabber tool... :white_check_mark:\nSending request to {member.id}...")
        await asyncio.sleep(random.uniform(0.5, 1.8))
        await m.edit(f"Starting IP grabber tool... :white_check_mark:\nSending request to {member.id}... :x: HTTP 403: _REQUEST DENIED_")
        await asyncio.sleep(random.uniform(0.6, 0.6))
        await m.edit(f"Starting IP grabber tool... :white_check_mark:\nSending request to {member.id}... :x: HTTP 403: _REQUEST DENIED_\nSearching opened ports...")
        await asyncio.sleep(random.uniform(0.9, 2.3))
        port = random.randint(0,8000)
        await m.edit(f"Starting IP grabber tool... :white_check_mark:\nSending request to {member.id}... :x: HTTP 403: _REQUEST DENIED_\nSearching opened ports... :white_check_mark:\nSuccess! Port **{port}**")
        await asyncio.sleep(random.uniform(0.5, 1.95))
        await m.edit(f"Starting IP grabber tool... :white_check_mark:\nSending request to {member.id}... :x: HTTP 403: _REQUEST DENIED_\nSearching opened ports... :white_check_mark:\nSuccess! Port **{port}**\nFetching IP...")
        await asyncio.sleep(random.uniform(0.5, 3.95))
        i = random.randint(1,4)
        if i != 4:
            await m.edit(f"Starting IP grabber tool... :white_check_mark:\nSending request to {member.id}... :x: HTTP 403: _REQUEST DENIED_\nSearching opened ports... :white_check_mark:\nSuccess! Port **{port}**\nFetching IP... :white_check_mark:\n**Result:** {member.name}'s IP is: `{generated_ip}`")
        else:
            await m.edit(f"Starting IP grabber tool... :white_check_mark:\nSending request to {member.id}... :x: HTTP 403: _REQUEST DENIED_\nSearching opened ports... :white_check_mark:\nSuccess! Port **{port}**\nFetching IP... :x:\n**FATAL ERROR** Something went wrong. The firewall blocked my `GET` request. Try again later.")
    
    @commands.command()
    async def hack(self, ctx, member : discord.Member = None):

        if member == None:
            await ctx.send("Please include the member you want to hack.")

        else:
            most_used_word = ["Chungus", "Big Chungus", "Me is nerd", "I like pinapples on pizzas", "I like homework"]
            most_used_app = ["Discord", "Facebook(damn what a dweeb)", "Instagram", "Twitter", "Tik Tok"]

            files = random.randint(2000,10000)
            em = discord.Embed(title = f"Hacking {member}.", description = f"hacking computer...({files} files)")
            word = random.choice(most_used_word)
            em2 = discord.Embed(title = f"Hacking {member}..", description = f"hacking epic games, roblox and minecraft account...(most used word in chat: {word})")
            app = random.choice(most_used_app)
            locations = ["Nerd island", "Stupid island", "parents house", "basement of a serial killer", "in space", "on mars", "on the moon"]
            location_of_user = random.choice(locations)
            em3 = discord.Embed(title = f"Hacking {member}...", description = f"hacking their phone...(most used app: {app})")
            em4 = discord.Embed(title = f"Hacking {member}..", description = f"hacking their location...(location: {location_of_user})")
            em5 = discord.Embed(title = f"Succesfully hacked {member}!", description = f"Most used app: {app}\nMost used word: {word}\nlocation: ||{location_of_user}||")

            m = await ctx.reply(embed=em)
            await asyncio.sleep(random.randint(4, 6))
            await m.edit(embed = em2)
            await asyncio.sleep(random.randint(3, 6))
            await m.edit(embed = em3)
            await asyncio.sleep(random.randint(5, 8))
            await m.edit(embed = em4)
            await asyncio.sleep(random.randint(6, 9))
            await m.edit(embed = em5)

    @commands.command(aliases=["cointos", "cointoss", "flipcoin"])
    async def coinflip(self, ctx):
        x = random.randint(1, 2)

        if (x == 1):
            em = discord.Embed(
                title="Heads!", description="The coin fliped HEADS!", color=discord.Colour.green())
            em.set_thumbnail(url="https://i.postimg.cc/mkt4HwWN/Heads.jpg")

            await ctx.reply(embed=em)
        else:
            em = discord.Embed(
                title="Tails!", description="The coin fliped TAILS!", color=discord.Colour.green())
            em.set_thumbnail(url="https://i.postimg.cc/DZCF0NHw/Tails.jpg")

            await ctx.reply(embed=em)

#adding cog
def setup(bot):
    bot.add_cog(fun(bot))