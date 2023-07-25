import discord
import os
import mariadb
import sys
from discord.ext import commands
import random 
from random import *
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
        member_id = message.author.id
        
        cur.execute(
            "SELECT user_id FROM users WHERE user_id=?",(member_id,)
        )
        member = cur.fetchone()

        if member == None:
            cur.execute(
                "INSERT INTO users (user_id, level, current_xp) VALUES (?, 0, 0)", (member_id,)
            )
        else:
            cur.execute(
                "SELECT current_xp FROM users WHERE user_id=?", (member_id,)
            )
            member_xp = cur.fetchone()
            xp_amount = randint(10, 35)
            xp_to_give = member_xp + xp_amount
            cur.exectue(
                "UPDATE users SET current_xp = ?", (xp_to_give,)
            )

async def setup(bot):
    await bot.add_cog(Levels(bot))