import discord
from discord.ext import commands
import random 
from random import *
import math
from databasemanager import *
from datetime import datetime
import time
from discord import app_commands


class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None
    
    @commands.Cog.listener()
    async def on_ready():
        print("Levels cog ready.")

        
    #Let users gain XP through sending messages, figure out how to add a cooldown
    #to prevent further spam.
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 485057961358524427:
            return
        
        member_id = message.author.id
        
        member = check_db_for_user(user_id=member_id)

        #If the user ID is not in the database, add it.
        if member == None:       
            initiate_user(user_id=member_id)
        
        else:
            member_xp = get_user_stat("current_xp", member_id)
            member_level = get_user_level(user_id=member_id)
            member_level = int(member_level[0])
            
            xp_amount = randint(3, 10)      # Pick a random value
            set_user_stat("current_xp", "add", xp_amount, member_id)   # Give the user XP

            xp_to_level_up = math.floor(100*(1.10) ** member_level)
            
            if xp_to_level_up > 2000:
                xp_to_level_up = 2000
            
            if member_xp >= xp_to_level_up:
                member_new_level = member_level + 1
                set_user_stat("level", set, member_new_level, member_id) #Level the user up
                set_user_stat("current_xp", "set", 0, member_id)# Reset their XP back to 0
                await message.add_reaction("🎉")        #Not as annoying as a message.
                #await message.channel.send(f"<@{message.author.id}>, you have leveled up to level {member_new_level}!")   
                return            
    
    @app_commands.command(name="profile", description="Shows you a user's profile.")
    async def profile(self, interaction: discord.Interaction, target: discord.Member = None):
        #If you dont choose someone to inspect, 
        #It picks you.
        if target == None:
            target_id = interaction.user.id
            target_name = interaction.user.name
            target_avatar = interaction.user.avatar
        else:
            target_id = target.id
            target_name = target.name
            target_avatar = target.avatar

        user_exists = check_db_for_user(user_id=target_id)
        if user_exists == None:
            initiate_user(user_id=target_id)
            target_level = get_user_level(user_id=target_id)
        else:
            target_level = get_user_level(user_id=target_id)
        target_level = int(target_level[0])

        #1 in 20 change to include @snowytaiyaki's art
        funny = False
        funny_chance = randint(1,20)
        if funny_chance == 14:
            funny = True
        else:
            funny = False

        xp_to_level_up = math.floor(100*(1.30) ** target_level)
        if xp_to_level_up > 2000:
            xp_to_level_up = 2000
        target_xp = get_user_stat("current_xp", target_id)

        total_xp_to_levelup = xp_to_level_up - target_xp
        if total_xp_to_levelup < 0:
            total_xp_to_levelup = 0

        xp_left = xp_to_level_up - target_xp
        next_level = target_level + 1
        embed = discord.Embed(
            title=target_name,
            colour=0x9230FF,
            timestamp=datetime.now()
        )
        embed.add_field(name=f"Level: {target_level}", value=f"XP: {target_xp}\n {xp_left} XP left until level {next_level}!",inline=False)
        
        target_credits = get_user_stat("credits", target_id)
        target_bank = get_user_stat("bank", target_id)
        embed.add_field(name=f"Credits: {target_credits}",value=f"Bank Balance: {target_bank}", inline=False)
        pfp = interaction.user.avatar
        embed.set_footer(text=target_id, icon_url=pfp)
        embed.set_thumbnail(url=target_avatar)
        if funny == True:
            if next_level >= 15:
                embed.set_image(url="https://media.discordapp.net/attachments/666826461956669450/1133990279611949096/NOLIFEsaturn.png")
            else:
                embed.set_image(url="https://media.discordapp.net/attachments/666826461956669450/1134003251608567839/waytogotii.png")
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="leaderboard", description="Shows the top 10 users in order of most credits!")
    async def leaderboard(self, interaction: discord.Interaction):            
            ldb = get_leaderboard()
            embed = discord.Embed(
                title="Eclipse Leaderboard:",
                colour=0xc45241,
                timestamp=datetime.now()
            )
            for i, pos in enumerate(ldb, start=1):
                userid, level, credits = pos
                embed.add_field(name=" ", value=f"{i}. <@{userid}>: Level `{level}` | `{credits}` credits", inline=False)
            embed.set_footer(icon_url=interaction.user.avatar)
            await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Levels(bot))