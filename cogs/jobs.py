import discord 
from discord import app_commands
from discord.ext import commands
import os 
from databasemanager import * 

class Jobs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None
    
    @commands.Cog.listener()
    async def on_ready():
        print("Jobs cog ready.")

    @app_commands.command(name="jobtest", description="Test job command")
    async def jobtest(self, interaction:discord.Interaction):
        await interaction.response.send_message("Jobs are functional.")

async def setup(bot):
    await bot.add_cog(Jobs(bot))