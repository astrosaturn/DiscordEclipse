import discord
from discord.ext import commands
from discord import app_commands
from profilemanager import *
from datetime import datetime

class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None
    
    @commands.Cog.listener()
    async def on_ready():
        print("Currency cog ready.")

    @app_commands.command(name="givecredits", description="Transfer some of your credits to someone else")
    async def givecredits(self, interaction: discord.Interaction, target: discord.User, amount: int):        
        author_balance = get_credits(interaction.user.id)

        if author_balance >= amount:
            remove_credits(amount, interaction.user.id)
            add_credits(amount, target.id)
            author_new_balance = get_credits(interaction.user.id)
            embed = discord.Embed(
                colour=0x53c970,
                timestamp=datetime.now()
            )
            embed.add_field(name="Transfer:", value=f"You have transfered {amount} credits to {target.mention}.", inline=False)
            embed.add_field(name="Remaning balance:", value=f"{author_new_balance} credits", inline=False)
            embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar)
            await interaction.response.send_message(embed=embed)
            
            
            #await interaction.response.send_message(f"You have given {amount} credits to {target.mention}")
        else:
            await interaction.response.send_message(f"You do not have enough credits to transfer.")
    
    @app_commands.command(name="daily", description="Redeem 1000 credits every day")
    async def daily(self, interaction: discord.Interaction):
        if cooldown_complete(interaction.user.id):
            add_credits(1000, interaction.user.id)
            init_cooldown(interaction.user.id)
            
            embed = discord.Embed(
                title="Daily Credits",
                colour=0x53c970,
                timestamp=datetime.now()
            )
            embed.add_field(name=f"{interaction.user.name}, 1000 Credits have been added to your account!", 
                            value=f"Your next Daily will be available on <t:{int(datetime.now().timestamp()) + 86400}>.",
                            inline=False
                            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"Your next daily will be available <t:{int(datetime.now().timestamp()) + 86400}:R>")

    
async def setup(bot):
    await bot.add_cog(Currency(bot))