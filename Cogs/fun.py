import discord
from discord.ext import commands
import random
from databasemanager import *
from discord import app_commands
from datetime import datetime
import json
import textwrap
import openai
import os
import time
from dotenv import load_dotenv

openai.api_key = (os.getenv("OPEN_AI_KEY"))

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
    @app_commands.command()
    async def rps(self, interaction: discord.Interaction):
        def check(m):
            return m.author == interaction.user and m.channel == interaction.channel
        
        await interaction.response.defer(thinking=True)
        msg = await interaction.original_response()
        bot_choices = ["rock", "paper", "scissors"]
        bot_choice = random.choice(bot_choices)
        await msg.edit(content="Lets play Rock, Paper, Scissors! I've made my choice, now you make yours.")
        user_id = interaction.user.id
        user_choice = await self.bot.wait_for('message', check=check)


        if user_choice.content.lower() == bot_choice:
            outcome = "It's a tie!"
        elif user_choice.content.lower() == "rock" and bot_choice == "scissors":
            outcome = "win"
        elif user_choice.content.lower() == "scissors" and bot_choice == "paper":
            outcome = "win"
        elif user_choice.content.lower() == "paper" and bot_choice == "rock":
            outcome = "win"
        else:
            outcome = "You lose!"
        
        if outcome == "win":
            set_user_stat("current_xp", "add", 15, user_id)
            message = f"You win! I chose `{bot_choice}` and you chose `{user_choice.content.lower()}`! You have been given 15 XP for winning!"
            await msg.edit(content=message)
        
        else:
            message = f"{outcome} I chose `{bot_choice}` and you chose `{user_choice.content.lower()}`!"
            await msg.edit(content=message)

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
        #for i, option in enumerate(options, start=1):
        #    embed.add_field(name="Options:", value=f"{i}. {option}\n", inline=False)
        embed.add_field(name="Options:", value=f"1. {options[0]}\n2. {options[1]}\n3. {options[2]}\n4. {options[3]}\n")
        embed.set_footer(text="Say the numerical position or type actual answer.", icon_url=interaction.user.avatar)
        msg = await interaction.original_response()
        await msg.edit(embed=embed)
        

        response = await self.bot.wait_for('message', check=check)
        if response.content.lower() == answer[0].lower() or response.content == answer[1]:
            embed = discord.Embed(
                colour=0x1cfc03,
                title="Correct!",
                timestamp=datetime.now()
            )
            embed.add_field(name=question, value=f'You have been awarded 20 XP and 200 Credits!\n\nThe answer was "{answer[0]}".')
            embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar)
            msg = await interaction.original_response()
            await msg.edit(embed=embed)
            set_user_stat("credits", "add", 200, interaction.user.id)
            set_user_stat("current_xp", "add", 20, interaction.user.id)
            
        else:
            embed = discord.Embed(
                colour=0xfc0303,
                title="Incorrect!",
                timestamp=datetime.now()
            )
            embed.add_field(name=question, value=f'The correct answer was "{answer[0]}".\n\nYour answer was "{response.content}."')
            embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar)
            
            
            msg = await interaction.original_response()
            await msg.edit(embed=embed)
    """
    @app_commands.command(name="eclipseai", description="Use OpenAI to talk to Eclipse.")
    async def eclipseai(self, interaction: discord.Interaction, query: str):
        if len(query) < 256:
            interaction_channel = interaction.channel_id
            await interaction.response.defer()
            def get_completion(prompt, model="gpt-4-turbo"):
                messages = [{"role": "user", "content": f"Your name is Eclipse, respond to this prompt in under 255 characters unless specifically instructed not to in the prompt: {prompt}"}]
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages,
                    temperature=1
                )
                return response.choices[0].message["content"]
            response = get_completion(query)
            msg = await interaction.original_response()

            # This only applies if you are using the multiple embeds
            # out = [(response[i:i+255]) for i in range(0, len(response), 255)]

            embed = discord.Embed(
                colour=0xfc8c03,
                timestamp=datetime.now()
            )

            if (len(response) < 256):
                embed.add_field(name=f'{interaction.user.name}: "{query}"', value=f'Eclipse:\n {response}')
                embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar)
                await msg.edit(embed=embed)
            else:
                with open("response.txt", "w") as f:
                    f.write(str(response))
                file = discord.File("response.txt")
                await msg.edit(content="Response was too large, sending in a file format:")
                await interaction.channel.send(file=file)

            # Figure out a way to have it truncate at whitespace
            
            if len(response) > 2:
                for i in range(len(out)):
                    embedcont = discord.Embed(
                        colour=0xfc8c03
                    )
                    embedcont.add_field(name=' ', value=f"{out[i + 1]}")
                    await interaction.channel.send(embed=embedcont)     
            
        else:
            await interaction.response.send_message("Your query must be under 256 characters!")
    """

            
async def setup(bot):
    await bot.add_cog(Fun(bot))