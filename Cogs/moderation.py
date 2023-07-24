import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None
    
    @commands.command()
    async def cogtest(ctx):
        ctx.reply("Cogs are functioning")

async def setup(bot):
    await bot.add_cog(Moderation(bot))