import discord
import os
from dotenv import load_dotenv


load_dotenv()
intents = discord.Intents.all()

bot = Client(
    command_prefix="$",
    help_command=None,
    intents=intents,
)

@bot.event
async def on_ready():
    print(f"Logged in!")

bot.run(os.getenv("TOKEN"))