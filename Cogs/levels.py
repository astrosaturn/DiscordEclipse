import discord
from discord.ext import commands

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Levels cog ready.")

async def setup(bot):
    await bot.add_cog(Levels(bot))