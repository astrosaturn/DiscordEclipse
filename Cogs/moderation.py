import discord
from discord.ext import commands
from databasemanager import *
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
                create_action(user.id,interaction.guild.id,"Ban",reason,interaction.user.id,user.name)
                case_num = get_case_num(user_id= user.id)               
                await interaction.response.send_message(f'{user} has been banned for the reason: `{reason}`. Case #{case_num}')
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
        user_id, guild_id, type, reason, moderator, casenum , username= get_case(case_num=casenumber)
        guild_id = int(guild_id)
        if casenumber != None:
            
            if guild_id == interaction.guild.id:
                embed = discord.Embed(
                    title=f"{username}",
                    colour=0xed5f5a,
                    timestamp=datetime.now()
                )
                embed.add_field(name=f"Case #{casenum}", value=f"{user_id}", inline=False)
                embed.add_field(name=f"Action: {type}", value=f"**Reason:**\n`{reason}`", inline=False)
                embed.set_footer(text=f"Moderator: {moderator}")
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(f"Sorry, this case {guild_id} is not from this guild {interaction.guild.id}.")
        else:
            await interaction.response.send_message("You must input a case number!")
    
    #Set a user's level
    @commands.command()
    async def setlevel(self, ctx, user:discord.User, level:int):
        if ctx.author.id == 345683515528183808:
            user = user.id        
            if user is not None:
                if level is not None:
                    level_set(level,user)
                    await ctx.reply(f"<@{user}>'s level has been set to {level}")
                else:
                    await ctx.reply(f"You must input a valid level.")
            else:
                await ctx.reply(f"You must input a valid user!")
        else:
            await ctx.reply(f"You do not have permission to use this command!")

    #Sets a user's XP
    @commands.command()
    async def setxp(self, ctx, user:discord.User, xp_toset: int):
        if ctx.author.id == 345683515528183808:
            user_id = user.id
            if user is not None:
                if xp_toset is not None:
                    set_user_xp(xp_toset, user_id)
                    await ctx.reply(f"<@{user_id}>'s XP has been set to {xp_toset}")
                else:
                    await ctx.reply(f"You must enter an XP value!")
            else:
                await ctx.reply(f"You must input a valid user!")
        else:
            await ctx.reply(f"You do not have permission to use this command!")
    
    #Set's a user's credits
    @commands.command()
    async def setcredits(self, ctx, user:discord.User, amount: int):
        if ctx.author.id == 345683515528183808:
            user_id = user.id
            if user is not None:
                set_credits(amount,user_id)
                await ctx.reply(f"<@{user_id}>'s Credits have been set to {amount}")
            else:
                await ctx.reply(f"You must enter a user!")
        else:
            await ctx.reply(f"You do not have permission to use this command!")     
    
    #Removes a user's credits
    @commands.command()
    async def removecredits(self, ctx, user:discord.User, amount: int):
        if ctx.author.id == 345683515528183808:
            user_id = user.id 
            if user is not None:
                remove_credits(amount, user_id)
                await ctx.reply(f"{amount} credits have been removed from <@{user_id}>.")
            else:
                await ctx.reply(f"You must enter a user.")
        else:
            await ctx.reply(f"You do not have permission to use this command!")    
    
    #Adds credit's to a user
    @commands.command()
    async def addcredits(self, ctx, user:discord.User, amount: int):
        if ctx.author.id == 345683515528183808:
            user_id = user.id
            if user is not None:
                add_credits(amount, user_id)
                await ctx.reply(f"{amount} credits have been added to <@{user_id}>.")
            else:
                await ctx.reply(f"You must enter a user.")
        else:
            await ctx.reply(f"You do not have permission to use this command!")        


    #Sets the channel to send logs to in the database
    @commands.command()
    async def setlogchannel(self, ctx, channel:commands.TextChannelConverter):
        if ctx.author.guild_permissions.manage_channels:
            
            guild_id = ctx.guild.id
            set_log_channel(channel.id, guild_id)
            await ctx.reply(f"The log channel has been set to <#{channel.id}>! in guild id `{guild_id}`!")
        else:
            await ctx.reply(f"You do not have permission to use this command!") 

    @app_commands.command(name="pfp", description="temp pfp command. ignore.")
    async def pfp(self, interaction: discord.Interaction):
        await interaction.response.send_message(interaction.user.avatar)

async def setup(bot):
    await bot.add_cog(Moderation(bot))