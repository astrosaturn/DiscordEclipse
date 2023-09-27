import discord
from discord.ext import commands
import random
from databasemanager import *
from discord import app_commands
from datetime import datetime
import json

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None
    
    @commands.Cog.listener()
    async def on_ready():
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
            add_xp(15, user_id)
            await ctx.reply(f"You win! I chose `{bot_choice}` and you chose `{user_choice}`! You have been given 15 XP for winning!")
        
        else:
            await ctx.reply(f"{outcome} I chose `{bot_choice}` and you chose `{user_choice}`!")

    @app_commands.command(name="trivia", description="Play a game of trivia ")
    async def trivia(self, interaction: discord.Interaction):
        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel
        
        #Load the JSON file 
        def load_questions(filename):
            with open(filename, "r") as file:
                data = json.load(file)
            return data
        questions = load_questions("triviastuff.json")

        random.shuffle(questions)

        for question_data in questions:
            question = question_data["question"]
            options = question_data["options"]
            answer = question_data["answer"]
        
        embed = discord.Embed(
            colour=0xc35187,
            title=question,
            timestamp=datetime.now()
        )
        await interaction.response.defer(thinking=True)
        for i, option in enumerate(options, start=1):
            embed.add_field(name=' ', value=f"{i}. {option}", inline=False)
        msg = await interaction.original_response()
        await msg.edit(embed=embed)
        

        response = await self.bot.wait_for('message', check=check)
        if response.content.lower() == answer.lower():
            embed = discord.Embed(
                colour=0xc35187,
                title="Correct!",
                timestamp=datetime.now()
            )
            embed.add_field(name=question, value=f'You have been awarded 20 XP and 200 Credits!\nThe answer was "{answer}".')
            msg = await interaction.original_response()
            await msg.edit(embed=embed)
            add_credits(200, interaction.user.id)
            add_xp(20, interaction.user.id)
        else:
            embed = discord.Embed(
                colour=0xc35187,
                title="Incorrect!",
                timestamp=datetime.now()
            )
            embed.add_field(name=question, value=f'The correct answer was "{answer}".\nYour answer was "{response.content}."')
            
            
            msg = await interaction.original_response()
            await msg.edit(embed=embed)
            
            
async def setup(bot):
    await bot.add_cog(Fun(bot))


