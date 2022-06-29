import discord
from discord.ext import commands
import random

class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.activities = {}


    @commands.command()
    async def cekilis(self, ctx):
        winner = random.choice(self.bot.guilds[0].members)
        await ctx.send(f"Çekiliş kazananı : {winner}")


    @commands.command()
    async def change_status(self, ctx, activity, *, text):
        self.bind_text(text)
        await self.bot.change_presence(**self.activities.get(activity))


    def bind_text(self, text, url = ""):
        self.activities = {
            "game" : {"activity" : discord.Game(name = text)},
            "listening" : {"activity" : discord.Activity(type = discord.ActivityType.listening, name = text)},
            "watching" : {"activity" : discord.Activity(type = discord.ActivityType.watching, name = text)},
            "streaming" : {"activity" : discord.Streaming(name = text, url = url)}
        }



def setup(bot):
    bot.add_cog(Other(bot))