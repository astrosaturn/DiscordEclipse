import discord
import os
import mariadb
import sys
from discord.ext import commands
import random 
from random import *
import math
import time
# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT")),
        database=os.getenv("DATABASE")
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")

cur = conn.cursor()


class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Levels cog ready.")

    
        
    #Get XP per message sent.
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 485057961358524427:
            return
        
        member_id = message.author.id
        
        cur.execute(
            "SELECT user_id FROM users WHERE user_id=?", (member_id,)            
        )
        member = cur.fetchone()

        #If the user ID is not in the database, add it.
        if member == None:       
            cur.execute("INSERT INTO users (user_id, level, current_xp) VALUES (?, 1, 100)", (member_id,))
        
        else:
            cur.execute(
                "SELECT current_xp FROM users WHERE user_id=?", (member_id,)
            )
            member_xp = cur.fetchone()

            cur.execute(
                "SELECT level FROM users WHERE user_id=?", (member_id,)
            )
            member_level = cur.fetchone()

            xp_amount = randint(3, 10)
            xp_to_give = int(member_xp[0]) + xp_amount
            cur.execute(
                "UPDATE users SET current_xp = ? WHERE user_id=?", (xp_to_give, member_id,)
            )
            
            #God I fucking hate MySQL           
            member_level = int(member_level[0])

            xp_to_level_up = math.floor(100*(1.10) ** member_level)
            if int(member_xp[0]) >= xp_to_level_up:
                member_new_level = member_level + 1
                cur.execute(
                    "UPDATE users SET level=? WHERE user_id=?", (member_new_level, member_id,)                   
                )
                cur.execute(
                    "UPDATE users SET current_xp = 0 WHERE user_id=?", (member_id,)
                )
                await message.channel.send(f"<@{message.author.id}>, you have leveled up to level {member_new_level}!")   
                return            
        conn.commit()
    
    @commands.command()
    async def xp(self, ctx):
        author_id = ctx.author.id
        cur.execute(
            "SELECT current_xp FROM users WHERE user_id=?", (author_id,)
        )
        author_xp = cur.fetchone()
        author_xp = int(author_xp[0])
        await ctx.reply(f"You have {author_xp} XP!")

    @commands.command()
    async def level(self, ctx):
        author_id = ctx.author.id
        cur.execute(
            "SELECT level FROM users WHERE user_id=?", (author_id,)
        )
        author_level = cur.fetchone()
        author_level = int(author_level[0])
        xp_to_level_up = math.floor(100*(1.10) ** author_level)
        cur.execute(
            "SELECT current_xp FROM users WHERE user_id=?", (author_id,)    
        )
        author_xp = cur.fetchone()
        author_xp = int(author_xp[0])

        total_xp_to_levelup = xp_to_level_up - author_xp
        if total_xp_to_levelup < 0:
            total_xp_to_levelup = 0
        await ctx.reply(f"You are level `{author_level}`. You have `{xp_to_level_up - author_xp}` XP left until `{author_level + 1}`.")



async def setup(bot):
    await bot.add_cog(Levels(bot))