import discord
from discord.ext import commands
import os
from dotenv import load_dotenv


load_dotenv()
intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="$",
    help_command=None,
    intents=intents,
)

@bot.event
async def on_ready():
    print(f"Logged in!")

@bot.command()
async def test(ctx):
    await ctx.reply("Test Complete.")

@bot.command()
async def ping(ctx):
    await ctx.send(
        f"Pong! My ping is  `{round(bot.latency * 1000)}ms.`"
    )

bot.run(os.getenv("TOKEN"))