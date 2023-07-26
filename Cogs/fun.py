import discord
from discord.ext import commands
import random

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
            await ctx.reply(f"You win! I chose `{bot_choice}` and you chose `{user_choice}`!")
        else:
            await ctx.reply(f"You lose! I chose `{bot_choice}` and you chose `{user_choice}`!")


    

async def setup(bot):
    await bot.add_cog(Fun(bot))


