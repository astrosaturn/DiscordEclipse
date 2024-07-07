import discord
from discord.ext import commands
from databasemanager import *
from discord import app_commands
from datetime import datetime 



class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None
    
    @commands.Cog.listener()
    async def on_ready():
        print("Logging cog ready")
    
    

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id != 485057961358524427:
            #Get the log channel.
            log_channel = get_log_channel(message.guild.id)
            channel = self.bot.get_channel(log_channel)
            if channel:
                embed = discord.Embed(
                    title=f"{message.author.name} has deleted a message in #{message.channel.name}",
                    colour=0x855a0c,
                    timestamp=datetime.now()
                )
                embed.add_field(name="Message content:", value=f"{message.content}")
                embed.set_footer(text=f"Author ID: {message.author.id}")
                await channel.send(embed=embed)
            else:
                return
        else:
            return
    
    @commands.Cog.listener()
    async def on_message_edit(self, before_message, after_message):
        if before_message.author.id and after_message.author.id != 485057961358524427:
            #Either before_message or after_message works.
            log_channel = get_log_channel(before_message.guild.id)
            channel = self.bot.get_channel(log_channel)
            if channel:
                embed = discord.Embed(
                    title=f"{before_message.author.name} has edited their message in #{before_message.channel.name}",
                    colour=0x855a0c,
                    timestamp=datetime.now()
                )
                embed.add_field(name="Message content before:", value=f"{before_message.content}", inline=False)
                embed.add_field(name="Message content after:", value=f"{after_message.content}", inline=False)
                embed.set_footer(text=f"Author ID: {before_message.author.id}")
                await channel.send(embed=embed)
        else:
            return


async def setup(bot):
    await bot.add_cog(Logging(bot))