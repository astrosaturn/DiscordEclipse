import discord
from discord.ext import commands
import random 
from random import *
import math
from profilemanager import *
from datetime import datetime
import time


class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None
    
    @commands.Cog.listener()
    async def on_ready(self):
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
            member_xp = get_user_xp(user_id=member_id)
            member_level = get_user_level(user_id=member_id)
            
            
            xp_amount = randint(3, 10)      # Pick a random value
            xp_to_give = member_xp + xp_amount      # Add together
            set_user_xp(xp_to_give, member_id)      # Give the user XP

            xp_to_level_up = math.floor(100*(1.10) ** member_level)
            
            if xp_to_level_up > 2000:
                xp_to_level_up = 2000
            
            if member_xp >= xp_to_level_up:
                member_new_level = member_level + 1  
                level_set(new_level=member_new_level, user_id=member_id)      # Level the user up
                set_user_xp(xp_amount=0, user_id=member_id)       # Reset their XP back to 0
                await message.channel.send(f"<@{message.author.id}>, you have leveled up to level {member_new_level}!")   
                return            


    @commands.command()
    async def level(self, ctx, *, target: discord.Member = None):
        #If you dont choose someone to inspect, 
        #It picks you.
        if target == None:
            target_id = ctx.author.id
            target_name = ctx.author.name
            target_avatar = ctx.author.avatar
        else:
            target_id = target.id
            target_name = target.name
            target_avatar = target.avatar

        #1 in 20 change to include @snowytaiyaki's art
        funny = False
        funny_chance = randint(1,20)
        if funny_chance == 14:
            funny = True
        else:
            funny = False

        target_level = get_user_level(user_id=target_id)

        xp_to_level_up = math.floor(100*(1.30) ** target_level)
        if xp_to_level_up > 2000:
            xp_to_level_up = 2000
        target_xp = get_user_xp(user_id=target_id)

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
        embed.add_field(name=f"Level: {target_level}", value=f"XP: {target_xp}\n {xp_left} XP left until level {next_level}!")
        author = ctx.message.author
        pfp = author.avatar
        embed.set_footer(text=target_id, icon_url=pfp)
        embed.set_thumbnail(url=target_avatar)
        if funny == True:
            if next_level >= 15:
                embed.set_image(url="https://media.discordapp.net/attachments/666826461956669450/1133990279611949096/NOLIFEsaturn.png")
            else:
                embed.set_image(url="https://media.discordapp.net/attachments/666826461956669450/1134003251608567839/waytogotii.png")
        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Levels(bot))