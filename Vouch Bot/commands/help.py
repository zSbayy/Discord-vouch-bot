import discord
from discord import app_commands
from discord.ext import commands
import json

with open("config.json") as config_file:
    config = json.load(config_file)

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Show all bot commands.")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Help - Best Commands to Use!", color=discord.Color.gold())
        

        embed.add_field(name="👏 Member Commands", value="/vouch - Respond to seller/owner\n/vouches - Check all vouches\n/help - Show all bot commands\n/info - Show bot information", inline=False)
        
        # Admin Commands
        embed.add_field(name="🎯 Admin Commands", value="/backup - Send backup vouches", inline=False)

        embed.set_footer(text=config["footer_text"], icon_url=config["footer_icon_url"])
        embed.set_thumbnail(url=config["thumbnail_url"])

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))
