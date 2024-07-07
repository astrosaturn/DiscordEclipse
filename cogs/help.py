import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from discord.ui import View, Button
from typing import Literal

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None

    @app_commands.command()
    @app_commands.describe(menus="Help menus")
    async def help(self, interaction: discord.Interaction, menus: Literal['Bot Setup ⚙️', 'Moderation 🛡️', 'Currency 💵', 'Fun 🎉', 'Profiles 📁', 'Jobs 💼']):
        embed = discord.Embed(
            title=f"{menus}",
            colour=0x94ff5e,
            timestamp=datetime.now()          
        )
        match menus:
            case 'Bot Setup ⚙️':
                embed.add_field(name="/setlogchannel [channel id]", value="This command will tell me where I send my logs.", inline=False)
                embed.add_field(name="/removelogchannel", value="This command removes the log channel.", inline=False)
                embed.add_field(name="/setscraperchannel", value="This command must be sent in the channel you want. This sets my message logging channel. (Use in channel you want to set)", inline=False)
                embed.add_field(name="/deletescraperchannel", value="This command removes the scraper channel.", inline=False)
            case 'Moderation 🛡️':
                embed.add_field(name="/warn", value="Sends a warning to a user's DMs", inline=False)
                embed.add_field(name="/ban", value="Bans a specified user.", inline=False)
                embed.add_field(name="/kick", value="Kicks a specified user.", inline=False)
                embed.add_field(name="/purge [x]", value="Deletes X amount of messages.", inline=False)
                embed.add_field(name="/slowmode [x]", value="Sets a channel's slowmode to X seconds.", inline=False)
                embed.add_field(name="/getcase [x]", value="Gets a user's case number, but only from the server the command is used in.", inline=False)
            case 'Currency 💵':
                embed.add_field(name="/transfer [x] [y]", value="Sends [x] credits to [y] user.", inline=False)
                embed.add_field(name="/daily", value="Gives you a daily amount of 1000 credits.", inline=False)
                embed.add_field(name="/gamble [x]", value="Gambles [x] amount of coins, you can either win or lose them.", inline=False)
                embed.add_field(name="/steal [x]", value="Steals a random amount from [x] user.", inline=False)
                embed.add_field(name="/bank [withdraw/deposit] [x]", value="Puts [x] credits into your bank, which cannot be stolen from.", inline=False)
            case 'Fun 🎉':
                embed.add_field(name="/rps [x]", value="Play Rock, Paper, Scissors for some XP and credits. You will play [x].", inline=False)
                embed.add_field(name="/eclipseai", value="Talk to Eclipse (it's just chatgpt)", inline=False)
                embed.add_field(name="/trivia", value="Play a game of trivia. A question will appear and if you choose the correct answer you get credits and xp", inline=False)
            case 'Profiles 📁':
                embed.add_field(name="/profile [x]", value="Gets user [x]'s profile. If [x] is none then it gets your profile.", inline=False)
                embed.add_field(name="/leaderboard", value="Gets the current gloabal leaderboard. Position is determined by highest credit count.", inline=False)
            case 'Jobs 💼':
                embed.add_field(name="Under construction", value="Jobs are a feature that will come later, still a work in progress", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    """ --- OLD MENU ---
    @app_commands.command(name="help", description="Querey commands and their specific usages!")
    async def help(self, interaction: discord.Interaction, query: str = None):
            #Make the ephemeral to prevent spam
            if query == None:
                embed = discord.Embed(
                    title="Help menu",
                    colour=0x94ff5e,
                    timestamp=datetime.now()          
                )        
                embed.add_field(name="Bot Setup ⚙️", value=f"IMPORTANT. Lists admin commands for setting up the bot's features.")
                embed.add_field(name="Moderation ⚔️", value=f"Lists available moderation commands.")
                embed.add_field(name="Currency 🪙", value="Lists available currency commands.")
                embed.add_field(name="Fun 🎉", value="Lists commands for various games and misc commands.")
                embed.add_field(name="Profiles 📁", value="Lists commands for viewing and changing your bot profile.")
                embed.add_field(name="Jobs 💼", value="Lists job-related commands. [WIP]")
                await interaction.response.send_message(embed=embed, ephemeral=True)
            
            elif query.lower() == "bot setup":
                embed = discord.Embed(
                    title="Bot Setup Menu",
                    colour=0x94ff5e,
                    timestamp=datetime.now()          
                )
                embed.add_field(name="/setlogchannel [id]", value="This command will tell me where I send my logs.")
                embed.add_field(name="/removelogchannel", value="This command removes the log channel.")
                embed.add_field(name="/setscraperchannel", value="This command must be sent in the channel you want. This sets my message logging channel.")
                embed.add_field(name="/deletescraperchannel", value="This command removes the scraper channel.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
            
            elif query.lower() == "moderation":
                embed = discord.Embed(
                    title="Moderation Commands",
                    colour=0x94ff5e,
                    timestamp=datetime.now()
                )
                embed.add_field(name="/ban", value="Bans a specified user.")
                embed.add_field(name="/kick", value="Kicks a specified user.")
                embed.add_field(name="/purge [x]", value="Deletes X amount of messages.")
                embed.add_field(name="/slowmode [x]", value="Sets a channel's slowmode to X seconds.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
            
            elif query.lower() == "currency":
                embed = discord.Embed(
                    title="Currency Commands",
                    colour=0x94ff5e,
                    timestamp=datetime.now()
                )
                embed.add_field(name="/transfer [x] [y]", value="Sends [x] credits to [y] user.")
                embed.add_field(name="/daily", value="Gives you a daily amount of 1000 credits.")
                embed.add_field(name="/gamble [x]", value="Gambles [x] amount of coins, you can either win or lose them.")
                embed.add_field(name="/steal [x]", value="Steals a random amount from [x] user.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
            
            elif query.lower() == "fun":
                embed = discord.Embed(
                    title="Fun Commands (WIP)",
                    colour=0x94ff5e,
                    timestamp=datetime.now()
                )
                embed.add_field(name="/rps [x]", value="Play Rock, Paper, Scissors for some XP and credits. You will play [x].")
                await interaction.response.send_message(embed=embed, ephemeral=True)
            
            elif query.lower() == "profiles":
                embed = discord.Embed(
                    title="Profile Commands",
                    colour=0x94ff5e,
                    timestamp=datetime.now()
                )
                embed.add_field(name="/profile [x]", value="Gets user [x]'s profile. If [x] is none then it gets your profile.")
                embed.add_field(name="/leaderboard", value="Gets the current gloabal leaderboard. Position is determined by currency.")
                await interaction.response.send_message(embed=embed, ephemeral=True)
    """


async def setup(bot):
    await bot.add_cog(Help(bot))