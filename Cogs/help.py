import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from discord.ui import View, Button

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None

    @app_commands.command(name="help", description="Show a list of useable commands.")
    async def help(self, interaction: discord.Interaction):
        button0 = Button(label="Moderation commands")

        button1 = Button(label="Fun commands")


        view = View()
        view.add_item(button0)
        view.add_item(button1)

        main_menu = await interaction.response.send_message("Main Menu", view=view)

        async def button_callback(interaction):
            if interaction.component.label == "Moderation commands":
                await interaction.response.send_message("Moderation message")
            elif interaction.component.label == "Fun commands":
                await interaction.response.send_message("Fun commands")

        button0.callback = button_callback
        button1.callback = button_callback

        interaction = await self.bot.wait_for("button_click", check=lambda i: i.message == main_menu)

        await interaction.component.callback(interaction)
 




async def setup(bot):
    await bot.add_cog(Help(bot))