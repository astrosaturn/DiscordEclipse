import discord
from discord.ext import commands
from databasemanager import *
from discord import app_commands
from discord import SyncWebhook


class Scraper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_member = None

    @commands.Cog.listener()
    async def on_ready():
        print("Scraper cog ready.")

    @app_commands.command(name="setscraperchannel", description="Sets the scraper channel to the channel this command is executed in.")
    async def setscraperchannel(self, interaction: discord.Interaction):
        if interaction.user.guild_permissions.manage_channels:
            set_scrape_chan_id(interaction.channel.id, interaction.guild.id)
            await interaction.response.send_message(f"Scraping channel has been set to <#{interaction.channel.id}>")
            webhook = await interaction.channel.create_webhook(name="Scraper", avatar=None, reason="Created by Eclipse for the scraper channel.")
            #Set the webhook's ID for later use!
            print(webhook.id)
            set_webhook_id(int(webhook.id), interaction.guild.id)
        else:
            interaction.response.send_message("You do not have permission to use this command!")

    
    @commands.Cog.listener()
    async def on_message(self, message):        
        if message.author.id != 485057961358524427 and message.author.id != 1081004946872352958:
            try:
                if get_scrape_channel_id(message.guild.id):
                    webhook_id = get_webhook_id(message.guild.id)
                    channel_id = message.channel.id
                    webhook_ref = await self.bot.fetch_webhook(webhook_id)
                    webhook_url = webhook_ref.url
                    webhook = SyncWebhook.from_url(str(webhook_url))

                    if message.webhook_id != None:
                        return
                    
                    else:
                        attachments = ""
                        if len(message.attachments):
                            for attachment in message.attachments:
                                attachments += f"\n{attachment.url}"
                        content=f"[ [Jump]({message.jump_url}) | <#{channel_id}> | {message.author.id} ] \n {message.content} {attachments}"
                        webhook.send(content=content, avatar_url=message.author.avatar, username=message.author.name)
                else:
                    return
            except:
                pass
        else:
            return

async def setup(bot):
    await bot.add_cog(Scraper(bot))