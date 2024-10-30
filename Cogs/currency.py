import discord
from discord.ext import commands
from discord import app_commands
from databasemanager import *
from datetime import datetime
from random import randint
import math
from typing import Literal

class Currency(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None
    
    @commands.Cog.listener()
    async def on_ready():
        print("Currency cog ready.")

    @app_commands.command(name="transfer", description="Transfer some of your credits to someone else")
    async def transfer(self, interaction: discord.Interaction, amount: int, target: discord.User):        
        author_balance = get_user_stat("credits", interaction.user.id)

        if author_balance >= amount:
            set_user_stat("credits", "remove", amount, interaction.user.id)
            set_user_stat("credits", "add", amount, target.id)

            author_new_balance = get_user_stat("credits", interaction.user.id)
            embed = discord.Embed(
                colour=0x53c970,
                timestamp=datetime.now()
            )
            embed.add_field(name="Transfer:", value=f"You have transfered {amount} credits to {target.mention}.", inline=False)
            embed.add_field(name="Remaning balance:", value=f"{author_new_balance} credits", inline=False)
            embed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"You do not have enough credits to transfer.")
    
    @app_commands.command(name="daily", description="Redeem 1000 credits every day")
    async def daily(self, interaction: discord.Interaction):
        if cooldown_complete(interaction.user.id):
            set_user_stat("credits", "add", 1000, interaction.user.id)
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
            
            target_balance = get_user_stat("credits", target.id)
            author_balance = get_user_stat("credits", interaction.user.id)

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
                            set_user_stat("credits", "add", theft_amount, interaction.user.id)
                            set_user_stat("credits", "remove", theft_amount, target.id)

                            set_theft_cooldown(cooldown, target.id)
                            embed.add_field(name="..and succeeds!", value=f"{interaction.user.mention} successfully stole {theft_amount} credits from {target.mention}!")
                            
                        else:       #33% to fail and lose your balance instead LOL!
                            if author_balance < theft_amount: 
                                set_user_stat("credits", "set", 0, interaction.user.id)                   
                                set_theft_cooldown(cooldown, target.id)
                                embed.add_field(name="..and fails miserably!", value=f"{interaction.user.mention} failed to steal from {target.mention} and lost all of their credits!")
                            else:
                                set_user_stat("credits", "remove", theft_amount, interaction.user.id) 
                                set_theft_cooldown(cooldown, target.id)
                                embed.add_field(name="...and fails!", value=f"{interaction.user.mention} failed to steal from {target.mention} and lost {theft_amount} credits!")
                    await interaction.response.send_message(embed=embed)
                else:
                    cooldown_remaining = get_theft_cooldown(target.id)
                    await interaction.response.send_message(f"{interaction.user.mention}, you must wait <t:{cooldown_remaining}:R> before stealing from {target.mention} again!")
        else:
            await interaction.response.send_message(f"You must input a user to steal from!")
            
    @app_commands.command(name="gamble", description="Gamble a sum of your coins!")
    async def gamble(self, interaction: discord.Interaction, amount: int):
        user_balance = get_user_stat("credits", interaction.user.id)
        user_balance = int(user_balance) 

        #Some preliminary stupid-checks. Fuck you @frantictaco.
        print("User balance:", user_balance)
        if user_balance > 0:

            if user_balance < amount:
                    await interaction.response.send_message(f"{interaction.user.mention}, you can't gamble more than your current balance.")
            elif amount <= 0:
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
            # I am aware this is OP.
            if w > z:
                winnings = amount * 2
                        
                set_user_stat("credits", "add", winnings, interaction.user.id)
                new_bal = get_user_stat("credits", interaction.user.id)
                embed.add_field(name="And wins!", value=f"{interaction.user.mention} has won `{winnings}` credits.\n Their balance is now `{new_bal}`.")
            else:
                set_user_stat("credits", "remove", amount, interaction.user.id)
                new_bal = get_user_stat("credits", interaction.user.id)
                embed.add_field(name="And loses.", value=f"{interaction.user.mention} has lost `{amount}` credits.\n Their new balance is `{new_bal}`.")
                        
            await interaction.response.send_message(embed=embed)
        else:    
            await interaction.response.send_message(f"{interaction.user.mention} you don't have any coins to gamble, numbnuts.")


    @app_commands.command(name="bank", description="Make withdrawls or deposits in your bank account!")
    async def bank(self, interaction:discord.Interaction, action: Literal['Deposit', 'Withdraw'], amount: int):
        user_id = interaction.user.id
        user_balance = get_user_stat("credits", interaction.user.id)
        current_bank_balance = get_user_stat("bank", user_id)
    
        if amount > 0:
            if action == "Withdraw":
                if current_bank_balance > 0:
                    if current_bank_balance >= amount: #i must be retarded because this was a bug for months lol
                        set_user_stat("bank", "remove", amount, user_id)
                        set_user_stat("credits", "add", amount, user_id)
                        await interaction.response.send_message(f"{amount} credits have been withdrawed from your account. You now have {current_bank_balance - amount} credits in your bank.")
                    else:
                        await interaction.response.send_message(f"You cannot withdraw more than whats in your account.")
                else:
                    await interaction.response.send_message("Can't withdraw if you have nothing to withdraw.")
                
            elif action == "Deposit":
                if user_balance <= amount:
                    if user_balance > 0:
                        set_user_stat("bank", "add", amount, user_id)
                        set_user_stat("credits", "remove", amount, user_id)
                        await interaction.response.send_message(f"{amount} credits have been deposited. Your bank balance is {current_bank_balance + amount} credits.")
                    else:
                        await interaction.response.send_message("Can't deposit if you have nothing to deposit. Broke ass")
                else:
                    await interaction.response.send_message("You cant deposit more than what you currently have.")
            else:
                await interaction.response.send_message("Please enter `withdraw` or `deposit`.")
        else:
            await interaction.response.send_message(f"Insert a value higher than 0.")
        



async def setup(bot):
    await bot.add_cog(Currency(bot))