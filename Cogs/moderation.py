import discord
from discord.ext import commands
from profilemanager import *

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation cog ready.")

    #Purge command
    @commands.command()
    async def purge(self, ctx: commands.Context, *, number:int = None):
        if ctx.message.author.guild_permissions.manage_messages:
            try:
                if number is None:
                    await ctx.reply('You must input a number!', mention_author=False)
                else:
                    deleted = await ctx.message.channel.purge(limit = number + 1)
                    await ctx.channel.send(f'Messages purged by {ctx.message.author.mention}: `{len(deleted) - 1}`')
            except:
                await ctx.reply("I can't purge messages here.", mention_author=False)
        else:
            await ctx.reply('You do not have permission to use this command.', mention_author=False)

    #Kick command
    @commands.command()
    async def kick(self, ctx:commands.Context, user:discord.Member,*,reason=None):
        if ctx.author.guild_permissions.kick_members:
            if user is not None:
                await user.kick(reason=reason)
                await ctx.reply(f'{user} has been kicked for the reason: `{reason}`')
            else:
                await ctx.reply(f"{ctx.message.author}, you must select a valid user!")
        else:
            await ctx.reply(f"You do not have permissions to use this command.")
    
    #Ban command
    @commands.command()
    async def ban(self, ctx:commands.Context, user:discord.Member,*,reason=None):
        if ctx.author.guild_permissions.ban_members:
            if user is not None:
                await user.ban(reason=reason)
                await ctx.reply(f'{user} has been banned for the reason: `{reason}`')
            else:
                await ctx.reply(f"{ctx.message.author}, you must select a valid user!")
        else:
            await ctx.reply(f"You do not have permissions to use this command.")

    #Slowmode command
    @commands.command()
    async def slowmode(self, ctx:commands.Context, *, time: int):
        channel = ctx.channel
        if ctx.author.guild_permissions.manage_channels:
            if time is not None:
                if time > 21600:
                    await ctx.reply("You can not input a time over 6 hours/21600 seconds!")
                else:
                    await channel.edit(slowmode_delay=time)
                    if time > 0:
                        await ctx.reply(f"Slowmode in <#{ctx.channel.id}> has been set to `{time}` seconds.")
                    else:
                        await ctx.reply(f"Slowmode in <#{ctx.channel.id}> has been removed.")
            else:
                await ctx.reply("You must input a time in seconds.")
        else:
            await ctx.reply("You do not have permission to use this command!")
    
    #Set a user's level
    @commands.command()
    async def setlevel(self, ctx:commands.Context, user:discord.User, level:int):
        user = user.id
        if ctx.author.guild_permissions.manage_roles:
            if user is not None:
                if level is not None:
                    level_set(new_level=level,user_id=user)
                    await ctx.reply(f"<@{user}>'s level has been set to {level}")
                else:
                    await ctx.reply(f"You must input a valid level.")
            else:
                await ctx.reply(f"You must input a valid user!")
        else:
            await ctx.reply(f"You do not have permission to do that!") 

    

async def setup(bot):
    await bot.add_cog(Moderation(bot))