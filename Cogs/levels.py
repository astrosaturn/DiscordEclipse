import discord
from discord.ext import commands
import random 
from random import *
import math
from profilemanager import *


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
        
        member = check_db_for_user(member_id)

        #If the user ID is not in the database, add it.
        if member == None:       
            initiate_user(member_id)
        
        else:
            member_xp = get_user_xp(member_id)
            member_level = get_user_level(member_id)
            
            
            xp_amount = randint(3, 10)      # Pick a random value
            xp_to_give = member_xp + xp_amount      # Add together
            set_user_xp(xp_to_give, member_id)      # Give the user XP

            xp_to_level_up = math.floor(100*(1.10) ** member_level)
            if member_xp >= xp_to_level_up:
                member_new_level = member_level + 1  
                level_set(member_new_level, member_id)      # Level the user up
                set_user_xp(0, member_id)       # Reset their XP back to 0
                await message.channel.send(f"<@{message.author.id}>, you have leveled up to level {member_new_level}!")   
                return            
    
    @commands.command()
    async def xp(self, ctx):
        author_id = ctx.author.id
        author_xp = get_user_xp(author_id)
        await ctx.reply(f"You have {author_xp} XP!")

    @commands.command()
    async def level(self, ctx):
        author_id = ctx.author.id
        author_level = get_user_level(author_id)
        xp_to_level_up = math.floor(100*(1.30) ** author_level)
        author_xp = get_user_xp(author_id)

        total_xp_to_levelup = xp_to_level_up - author_xp
        if total_xp_to_levelup < 0:
            total_xp_to_levelup = 0
        await ctx.reply(f"You are level `{author_level}`. You have `{xp_to_level_up - author_xp}` XP left until `{author_level + 1}`.")



async def setup(bot):
    await bot.add_cog(Levels(bot))