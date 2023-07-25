import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation cog ready.")

    @commands.command()
    async def cogtest(self, ctx):
        await ctx.reply("congrats, you arent as worthless as you thought")

async def setup(bot):
    await bot.add_cog(Moderation(bot))