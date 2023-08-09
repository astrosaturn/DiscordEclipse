import discord
from discord.ext import commands
from databasemanager import *
from discord import app_commands
from discord import SyncWebhook


class Scraper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None
    
    @commands.Cog.listener()
    async def on_ready():
        print("Scraper cog ready.")

    @app_commands.command(name="setscraperchannel", value="Sets the scraper channel to the channel this command is executed in.")
    async def setscraperchannel(self, interaction: discord.Interaction):
        return

async def setup(bot):
    await bot.add_cog(Scraper(bot))