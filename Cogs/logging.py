import discord
from discord.ext import commands
from databasemanager import *
from discord import app_commands



class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None
    
    @commands.Cog.listener()
    async def on_ready():
        print("Logging cog ready")



    @commands.Cog.listener()
    async def on_message_delete(self, message):
        #Get the log channel.
        log_channel = get_log_channel(message.guild.id)
        await message.channel.send(message.content)
        



async def setup(bot):
    await bot.add_cog(Logging(bot))