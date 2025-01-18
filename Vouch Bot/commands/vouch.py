import discord
from discord import app_commands
from discord.ext import commands
import json
from db.database import Database 

class Vouch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.load_config()
        self.db = Database()  

    def load_config(self):
        with open('config.json') as f:
            return json.load(f)

    @app_commands.command(name="vouch", description="Create a vouch for the owner.")
    @app_commands.describe(rating="Choose a star rating for the vouch.")
    @app_commands.choices(rating=[
        app_commands.Choice(name="⭐", value=1),
        app_commands.Choice(name="⭐⭐", value=2),
        app_commands.Choice(name="⭐⭐⭐", value=3),
        app_commands.Choice(name="⭐⭐⭐⭐", value=4),
        app_commands.Choice(name="⭐⭐⭐⭐⭐", value=5),
    ])
    async def vouch(self, interaction: discord.Interaction, rating: app_commands.Choice[int], message: str):
        owner_id = self.config["owner_id"]  
        author_id = interaction.user.id  

        
        self.db.create_vouch(author_id, owner_id, rating.value, message)

        
        embed = discord.Embed(title="New Vouch Created", description=f"{'⭐' * rating.value}", color=discord.Color.green())
        embed.add_field(name="Vouch:", value=message, inline=False)
        embed.add_field(name="Vouched By:", value=interaction.user.mention, inline=True)
        embed.add_field(name="Vouched At:", value=discord.utils.format_dt(discord.utils.utcnow(), 'R'), inline=True)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.set_footer(text="Vouch System", icon_url=self.config["footer_icon_url"])

        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="vouches", description="View total number of vouches.")
    async def vouches(self, interaction: discord.Interaction):
        
        vouches = self.db.get_all_vouches()
        total_vouches = len(vouches)

        
        embed = discord.Embed(title="Vouches", color=discord.Color.blue())
        embed.add_field(name="Vouches:", value=str(total_vouches), inline=False)
        embed.add_field(name="Requested By:", value=interaction.user.mention, inline=True)
        embed.add_field(name="Requested At:", value=discord.utils.format_dt(discord.utils.utcnow(), 'R'), inline=True)

        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Vouch(bot))
