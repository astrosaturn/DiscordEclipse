import discord
from discord.ext import commands
from discord import app_commands
from profilemanager import *
from datetime import datetime
from random import randint
import math

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
                            value=f"Your next Daily will be available on <t:{cooldown_left(interaction.user.id)}>.",
                            inline=False
                            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"Your next daily will be available <t:{cooldown_left(interaction.user.id)}:R>")

    @app_commands.command(name="steal", description="Attempt to steal credits from your target")
    async def steal(self, interaction: discord.Interaction, target: discord.User):
        if target is not None:
            
            target_balance = get_credits(target.id)
            author_balance = get_credits(interaction.user.id)

            #Calculate this here because it will be used regardless
            #of if the user wins or loses the steal
            theft_amount = target_balance / 4
            theft_amount = math.trunc(theft_amount)
            
            if target.id == interaction.user.id:
                await interaction.response.send_message("You can't steal from yourself, moron.")
            else:
                if int(datetime.now().timestamp()) >= get_theft_cooldown(target.id):
                    cooldown = int(datetime.now().timestamp()) + 3600
                    
                    embed = discord.Embed(
                        title=f"{interaction.user.name} attemps to steal from {target.name}..",
                        colour=0xfc0f03,
                        timestamp=datetime.now()
                    )

                    if theft_amount < 1:
                        embed.add_field(name=f"... and finds nothing?", value=f"{target.name} has insufficent credits to steal!")
                    else:
                        chance = randint(1, 3)
                        if chance > 1:      #66% chance to steal, this may need to be adjusted.
                            add_credits(theft_amount, interaction.user.id)
                            remove_credits(theft_amount, target.id)
                            set_theft_cooldown(cooldown, target.id)
                            embed.add_field(name="..and succeeds!", value=f"{interaction.user.mention} successfully stole {theft_amount} credits from {target.mention}!")
                            
                        else:       #33% to fail and lose your balance instead LOL!
                            if author_balance < theft_amount:
                                set_credits(0, interaction.user.id)                        
                                set_theft_cooldown(cooldown, target.id)
                                embed.add_field(name="..and fails miserably!", value=f"{interaction.user.mention} failed to steal from {target.mention} and lost all of their credits!")
                            else:
                                remove_credits(theft_amount, interaction.user.id)
                                set_theft_cooldown(cooldown, target.id)
                                embed.add_field(name="...and fails!", value=f"{interaction.user.mention} failed to steal from {target.mention} and lost {theft_amount} credits!")
                    await interaction.response.send_message(embed=embed)
                else:
                    cooldown_remaining = get_theft_cooldown(target.id)
                    await interaction.response.send_message(f"{interaction.user.mention}, you must wait <t:{cooldown_remaining}:R> before stealing from {target.mention} again!")

    @app_commands.command(name="gamble", description="Gamble a sum of your coins!")
    async def gamble(self, interaction: discord.Interaction, amount: int):
        user_balance = get_credits(interaction.user.id)
        
        #Some preliminary stupid-checks. Fuck you @frantictaco.
        if user_balance == 0:
            await interaction.response.send_message(f"{interaction.user.mention} you don't have any coins to gamble, numbnuts.")
            return
        else:
            if amount <= 0:
                await interaction.response.send_message(f"{interaction.user.mention}, you can't gamble nothing. Input a value higher than 0.")
            else:
                x = user_balance
                y = randint(1,5)
                i = randint(1,6)

                z = (x * y) 
                w = (x * i)

                print(f"z = {z} w = {w}")
                embed = discord.Embed(
                    title=f"{interaction.user.name} makes a bet of {amount} credits.",
                    colour=0x3492eb,
                    timestamp=datetime.now()
                )


                if w > z:
                    winnings = amount * 2
                    add_credits(winnings, interaction.user.id)
                    new_bal = get_credits(interaction.user.id)
                    embed.add_field(name="And wins!", value=f"{interaction.user.mention} has won `{winnings}` credits.\n Their balance is now `{new_bal}`.")
                else:
                    remove_credits(amount, interaction.user.id)
                    new_bal = get_credits(interaction.user.id)
                    embed.add_field(name="And loses.", value=f"{interaction.user.mention} has lost `{amount}` credits.\n Their new balance is `{new_bal}`.")
                
                await interaction.response.send_message(embed=embed)




async def setup(bot):
    await bot.add_cog(Currency(bot))