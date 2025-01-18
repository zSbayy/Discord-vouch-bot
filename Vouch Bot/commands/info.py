import discord
from discord import app_commands
from discord.ext import commands
import psutil  
import json
s
with open("config.json") as config_file:
    config = json.load(config_file)

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="info", description="Show bot information.")
    async def info(self, interaction: discord.Interaction):
        memory = psutil.virtual_memory()
        memory_percent = memory.percent  

        embed = discord.Embed(title="Bot Information", color=discord.Color.purple())
        embed.add_field(name="Owner", value=f"<@{config['owner_id']}>", inline=True)
        embed.add_field(name="Developer", value=f"<@{config['developer_id']}>", inline=True)
        embed.add_field(name="Version", value=f"{config['version']}", inline=True)
        embed.add_field(name="Memory Used", value=f"{memory_percent}%", inline=True)
        embed.set_footer(text=config["footer_text"], icon_url=config["footer_icon_url"])
        embed.set_thumbnail(url=config["thumbnail_url"])

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Info(bot))
