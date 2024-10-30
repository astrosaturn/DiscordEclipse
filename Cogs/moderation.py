import discord
from discord.ext import commands
from databasemanager import *
from discord import app_commands
from datetime import datetime
import asyncio 
from typing import Literal

activated = False
"""
async def check_mute_timers():
    activated = True
    print("Beginning mute check routine..")
    while True:
        await asyncio.sleep(2)
        timestamp = int(datetime.now().timestamp())
        users = check_mutes(timestamp)
        print("Mutes checked..")
"""

class Moderation(commands.Cog):
            
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None


    @commands.Cog.listener()
    async def on_ready(self, message):
        print("Moderation cog ready.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if activated:
            pass
        else:
            pass
            #await check_mute_timers()

    @app_commands.command(name="mute", description="Mutes a user for X time.")
    async def mute(self, interaction: discord.Interaction, target:discord.Member, amount:int = None, reason:str = None):
        timestamp = int(datetime.now().timestamp()) + amount


        create_mute(target.id, timestamp, interaction.guild_id, reason)

        await interaction.response.send_message(f"{target.name} has been muted for {amount} seconds for {reason}.")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user): 
        if user.id == 69:
            if reaction.emoji == "🫃":
                await reaction.remove(user)
                print('no pregnant men allowed.')

    @app_commands.command(name="warn", description="Makes a case against the user as a warn.")
    async def warn(self, interaction:discord.Interaction, target:discord.Member, reason:str = None):
        if interaction.user.guild_permissions.manage_messages:
            try:
                if reason is None:
                    reason = "No reason"
                    create_action(target.id,interaction.guild_id,"Warn",reason,interaction.user.id,target.name)
                    case_number = get_case_num(target.id)
                    await interaction.response.send_message(f"{target.name} has been warned. Case #{case_number}", ephemeral=True)
                    await target.send(f"You have been warned in {interaction.guild.name} by {interaction.user.name}.")
                else:
                    create_action(target.id,interaction.guild_id,"Warn",reason,interaction.user.id,target.name)
                    case_number = get_case_num(target.id)
                    await target.send(f"You have been warned in {interaction.guild.name} by {interaction.user.name} for:\n\"{reason}\"")
                    await interaction.response.send_message(f"{target.name} has been warned for {reason}. Case #{case_number}", ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"Unable to warn user: {e}")
        else:
            await interaction.response.send_message(f"{interaction.user.mention} you do not have permission to use this command.")

    #Purge command
    @app_commands.command(name="purge", description="Removes x amount of messages")
    async def purge(self, interaction: discord.Interaction, amount:int = None):
        if interaction.user.guild_permissions.manage_messages:
            try:
                if amount is None:
                    await interaction.response.send_message('You must input a number!', ephemeral=True)
                else:
                    deleted = amount
                    await interaction.response.send_message("Purging..") # Do this or you get an ugly "The application did not respond" message 
                    await interaction.channel.purge(limit = amount)
                    await interaction.channel.send(f"Messages purged by {interaction.user.mention}: `{deleted}`")
                
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
                create_action(user.id,interaction.guild.id,"Kick",reason,interaction.user.id,user.name)
                case_num = get_case_num(user_id=user.id)
                await interaction.response.send_message(f'{user} has been kicked for the reason: `{reason}` | Case #{case_num}')
            else:
                await interaction.response.send_message(f"{interaction.user.mention}, you must select a valid user!", ephemeral=True)
        else:
            await interaction.response.send_message(f"You do not have permissions to use this command.", ephemeral=True)
    
    #Ban command
    @app_commands.command(name="ban", description="Bans a selected user.")
    @app_commands.describe(anonymous="If the user will see your username in the ban message")
    async def ban(self, interaction: discord.Interaction, user: discord.Member, reason: str = "No reason", *, anonymous: Literal['true', 'false'] = 'true'):
        if interaction.user.guild_permissions.ban_members:
            if user is not None:
                create_action(user.id, interaction.guild.id, "Ban", reason, interaction.user.id, user.name)
                case_num = get_case_num(user_id=user.id)
                
                try:
                    if anonymous == "true":
                        await user.send(f'You have been banned from "{interaction.guild.name}" for: **{reason}**.')
                    else:
                        await user.send(f'You have been banned from "{interaction.guild.name}" by {interaction.user.global_name} for: **{reason}**.')
                    await user.ban(reason=reason)
                except Exception as e:
                    print(f"An error has occurred: {e}")
                    await interaction.response.send_message(f"An error has occurred.", ephemeral=True)
                    return 

                channel = get_log_channel(interaction.guild.id)
                channel = self.bot.get_channel(channel)
                embed = discord.Embed(
                    title=f"{user.name} was banned. Case number #{case_num}",
                    colour=0x855a0c,
                    timestamp=datetime.now()
                )
                if channel is not None:
                    await channel.send(embed=embed)
                embed.add_field(name="Reason:", value=reason, inline=False)
                embed.add_field(name="Duration:", value="To be implemented.", inline=False)
                embed.set_footer(text=f"Moderator: {interaction.user.name}", icon_url=interaction.user.avatar.url)
                await interaction.response.send_message(f'{user} has been banned for the reason: `{reason}` | Case #{case_num}')
            else:
                await interaction.response.send_message(f"{interaction.user.mention}, you must select a valid user!", ephemeral=True)
        else:
            await interaction.response.send_message(f"You do not have permissions to use this command.", ephemeral=True)



    #Slowmode command
    @app_commands.command(name="slowmode", description="Sets the current channel to slowmode for x seconds")
    async def slowmode(self, interaction: discord.Interaction, *, time: int,):
        channel = interaction.channel
        log_channel = get_log_channel(interaction.guild.id)
        if interaction.user.guild_permissions.manage_channels:
            if time is not None:
                if time > 21600:
                    interaction.response.send_message("You can not input a time over 6 hours/21600 seconds!", ephemeral=True)
                else:
                    await channel.edit(slowmode_delay=time)
                    if time > 0:                        
                        #Send a log
                        if log_channel:     #But only if the channel has been defined!
                            log_embed = discord.Embed(
                                title="Slowmode has been set.",
                                colour=0xed5f5a,
                                timestamp=datetime.now()
                            )
                            log_embed.add_field(name=f"Moderator: {interaction.user.name}", value=f"Channel: <#{channel.id}>\nDuration: `{time}` seconds")
                            log_channel = self.bot.get_channel(log_channel)
                            await log_channel.send(embed=log_embed)

                        await interaction.response.send_message(f"Slowmode in <#{channel.id}> has been set to `{time}` seconds.", ephemeral=True)
                    else:
                        if log_channel: 
                            log_embed = discord.Embed(
                                title="Slowmode was removed",
                                colour=0xed5f5a,
                                timestamp=datetime.now()
                            )
                            log_embed.add_field(name=f"Moderator: {interaction.user.name}", value=f"Channel: <#{channel.id}>\nSlowmode removed")
                            log_channel = self.bot.get_channel(log_channel)
                            await log_channel.send(embed=log_embed)
                        await interaction.response.send_message(f"Slowmode in <#{channel.id}> has been removed.")
            else:
                await interaction.response.send_message("You must input a time in seconds.", ephemeral=True)
        else:
            await interaction.response.send_message("You do not have permission to use this command!", ephemeral=True)
    
    #Gets a user's case
    @app_commands.command(name="getcase", description="Gets a user's moderaton case.")
    async def getcase(self, interaction:discord.Interaction, casenumber:int):
        try:
            casenum, user_id, guild_id, action_type, reason, moderator, username = get_case(case_num=casenumber)
            reason = str(reason)
            guild_id = int(guild_id)
            if casenumber != None:
                if guild_id == interaction.guild.id:
                    embed = discord.Embed(
                        title=f"User: {username}",
                        colour=0xed5f5a,
                        timestamp=datetime.now()
                    )
                    embed.add_field(name=f"Case #{casenum}", value=f"User ID: {user_id}", inline=False)
                    embed.add_field(name=f"Action: {action_type}", value=f"**Reason:**\n`{reason}`", inline=False)
                    embed.set_footer(text=f"Moderator: {moderator}")
                    await interaction.response.send_message(embed=embed)
                else:
                    await interaction.response.send_message(f"Sorry, this case {guild_id} is not from this guild {interaction.guild.id}.")
            else:
                await interaction.response.send_message("You must input a case number!")
        except Exception as e:
            await interaction.response.send_message(f"Casenumber `{casenumber}` does not exist.")
            target = interaction.guild.get_member(345683515528183808)
            await target.send(e)

    @commands.command()
    async def setstat(self, ctx, user:discord.User, action: str, stat: str, value: int):
        action = action.lower()
        user_id = user.id

        if user is not None:
            if action == "add" or action == "remove" or action == "set":
                if value is not None:
                    if ctx.author.id == 345683515528183808: # This is an owner only command, isOwner() doesn't work for some reason.
                        try:
                            set_user_stat(f"{stat}", f"{action}", value, user_id)
                            await ctx.reply(f"`{action}` `{stat}` for user <@{user_id}> for value `{value}`")
                        except Exception as e:
                            await print(f"There was an error: `{e}`")   
                    else:
                        ctx.reply("You do not have permission to use that command.")
                else:
                    ctx.reply("You must input a value.")
            else:
                ctx.reply("Must be a valid action!")
        else:
            ctx.reply("You must input a user!")     

    @commands.command()
    async def sex(self, ctx, user:discord.User = None):
        if ctx.author.id == 345683515528183808:
            if user is not None:
                try:
                    set_user_stat("user_level", "set", 0, user.id) 
                    set_user_stat("current_xp", "set", 0, user.id)
                    await ctx.reply(f"Set <@{user.id}>'s level and XP to 0")
                
                except Exception as e:
                    await ctx.reply(f"OOPS!")
                    print(f"There was a sex error: {e}")
            else:
                await ctx.reply("cant sex noone unlike you")
        else:
            await ctx.reply("no sex for you")
        
    @commands.command()
    async def ver(self, ctx):
        await ctx.reply("Version 0.8.1")

    #Sets the channel to send logs to in the database
    @commands.command()
    async def setlogchannel(self, ctx, channel:commands.TextChannelConverter):
        if ctx.author.guild_permissions.manage_channels:
            guild_id = ctx.guild.id
            set_log_channel(channel.id, guild_id)
            await ctx.reply(f"The log channel has been set to <#{channel.id}>! in guild id `{guild_id}`!")
        else:
            await ctx.reply(f"You do not have permission to use this command!") 

    @app_commands.command()
    @app_commands.checks.cooldown(1, 15.0)
    async def cooldowntest(self, interaction: discord.Interaction):
        await interaction.response.send_message("This command is now on cooldown for 15 seconds.")

    @cooldowntest.error
    async def cooldowntest_error(self, interaction: discord.Interaction, error: commands.CommandError):
        error = str(error)
        seconds = error.split("again in ", 1)
        if isinstance(error, commands.CommandOnCooldown):
            await interaction.response.send_message(str(error), ephemeral=True)
        else:
            await interaction.response.send_message(f"This command is on cooldown. {seconds[1]} left", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))