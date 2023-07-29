import discord
from discord.ext import commands
from profilemanager import *
from discord import app_commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None
    
    @commands.Cog.listener()
    async def on_ready():
        print("Moderation cog ready.")

    #Purge command
    @app_commands.command(name="purge", description="Removes x amount of messages")
    async def purge(self, interaction: discord.Interaction, amount:int = None):
        if interaction.user.guild_permissions.manage_messages:
            try:
                if amount is None:
                    await interaction.response.send_message('You must input a number!', ephemeral=True)
                else:
                    deleted = amount
                    await interaction.channel.purge(limit = amount)
                    await interaction.channel.send(f'Messages purged by {interaction.user.mention}: `{deleted}`')
            except Exception as e:
                await interaction.response.send_message(f"I can't purge messages here: {e}", ephemeral=True)
        else:
            await interaction.response.send_message('You do not have permission to use this command.')

    #Kick command
    @app_commands.command(name="kick", description="Kicks a user.")
    async def kick(self, interaction: discord.Interaction, user:discord.Member,*,reason: str = None):
        if interaction.user.guild_permissions.kick_members:
            if user is not None:
                await user.kick(reason=reason)
                await interaction.response.send_message(f'{user} has been kicked for the reason: `{reason}`')
            else:
                await interaction.response.send_message(f"{interaction.user.mention}, you must select a valid user!", ephemeral=True)
        else:
            await interaction.response.send_message(f"You do not have permissions to use this command.", ephemeral=True)
    
    #Ban command
    @app_commands.command(name="ban", description="Bans a selected user.")
    async def ban(self, interaction: discord.Interaction, user:discord.Member,*,reason:str = None):
        if interaction.user.guild_permissions.ban_members:
            if user is not None:
                await user.ban(reason=reason)
                await interaction.response.send_message(f'{user} has been banned for the reason: `{reason}`')
            else:
                await interaction.response.send_message(f"{interaction.user.mention}, you must select a valid user!", ephemeral=True)
        else:
            await interaction.response.send_message(f"You do not have permissions to use this command.", ephemeral=True)

    #Slowmode command
    @app_commands.command(name="slowmode", description="Sets the current channel to slowmode for x seconds")
    async def slowmode(self, interaction: discord.Interaction, *, time: int,):
        channel = interaction.channel
        if interaction.user.guild_permissions.manage_channels:
            if time is not None:
                if time > 21600:
                    interaction.response.send_message("You can not input a time over 6 hours/21600 seconds!", ephemeral=True)
                else:
                    await channel.edit(slowmode_delay=time)
                    if time > 0:
                        await interaction.response.send_message(f"Slowmode in <#{channel.id}> has been set to `{time}` seconds.", ephemeral=True)
                    else:
                        await interaction.response.send_message(f"Slowmode in <#{channel.id}> has been removed.")
            else:
                await interaction.response.send_message("You must input a time in seconds.", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)
    
    #Set a user's level
    @commands.is_owner()
    @app_commands.command(name="setlevel", description="Sets the users current level.")
    async def setlevel(self, interaction: discord.Interaction, user:discord.User, level:int):
        user = user.id        
        if user is not None:
            if level is not None:
                level_set(level,user)
                await interaction.response.send_message(f"<@{user}>'s level has been set to {level}")
            else:
                await interaction.response.send_message(f"You must input a valid level.")
        else:
            await interaction.response.send_message(f"You must input a valid user!")
        

    #Sets a user's XP
    @commands.is_owner()
    @app_commands.command(name="setxp", description="Sets the users current XP.")
    async def setxp(self, interaction: discord.Interaction, user:discord.User, xp_toset: int):
        user_id = user.id
        if user is not None:
            if xp_toset is not None:
                set_user_xp(xp_toset, user_id)
                await interaction.response.send_message(f"<@{user_id}>'s XP has been set to {xp_toset}")
            else:
                await interaction.response.send_message(f"You must enter an XP value!")
        else:
            await interaction.response.send_message(f"You must input a valid user!")
    
    #Set's a user's credits
    @commands.is_owner()
    @app_commands.command(name="setcredits", description="Sets the users current credit balance")
    async def setcredits(self, interaction: discord.Interaction, user:discord.User, amount: int):
        user_id = user.id
        if user is not None:
            set_credits(amount,user_id)
            await interaction.response.send_message(f"<@{user_id}>'s Credits have been set to {amount}")
        else:
            await interaction.response.send_message(f"You must enter a user!")
         

    #Removes a user's credits

    #Adds credit's to a user


async def setup(bot):
    await bot.add_cog(Moderation(bot))