import discord
from discord.ext import commands
import random
import mariadb
import os
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
    print(f"Error connecting to MariaDB Platform in fun.py: {e}")

cur = conn.cursor()

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun cog ready.")

#TODO: make these games linked with XP and a currency system

    #I am well aware I could just pick a random win, lose, or tie condition
    #However I wanted to show what the bot had picked to the player
    #So it seemed like an actual game
    @commands.command(aliases=["rock paper scissors", "psr", "paper scissors rock"])
    async def rps(self, ctx, *, choice: str):
        bot_choices = ["rock", "paper", "scissors"]
        bot_choice = random.choice(bot_choices)
        user_id = ctx.author.id
        user_choice = choice.lower()


        if user_choice == bot_choice:
            outcome = "It's a tie!"
        elif user_choice == "rock" and bot_choice == "scissors":
            outcome = "win"
        elif user_choice == "scissors" and bot_choice == "paper":
            outcome = "win"
        elif user_choice == "paper" and bot_choice == "rock":
            outcome = "win"
        else:
            outcome = "You lose!"

        if outcome == "win":
            await ctx.reply(f"You win! I chose `{bot_choice}` and you chose `{user_choice}`! You have been awarded `15` XP for winning!")
            cur.execute(
                "SELECT current_xp FROM users WHERE user_id = ?", (user_id,)
            )
            user_currentxp = cur.fetchone()
            user_currentxp = int(user_currentxp[0])     #Covert to an integer from a truple
            xp_to_give = user_currentxp + 15
            #Give the user 15 experience points for winning, because why the fuck not
            cur.execute(
                "UPDATE users SET current_xp = ? WHERE user_id = ?", (xp_to_give, user_id,)
            )
            print(f"User {user_id} has been successfully given XP for winning Rock paper scissors.")
        else:
            await ctx.reply(f"{outcome} I chose `{bot_choice}` and you chose `{user_choice}`! ")


    

async def setup(bot):
    await bot.add_cog(Fun(bot))


