import discord
from discord.ext import commands
from discord import app_commands

class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None
    
    @commands.Cog.listener()
    async def on_ready():
        print("Currency cog ready.")

    
async def setup(bot):
    await bot.add_cog(Currency(bot))