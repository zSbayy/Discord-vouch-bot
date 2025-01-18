import discord
from discord import app_commands
from discord.ext import commands
from db.database import Database  
from datetime import datetime  

class Backup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()  

    @app_commands.command(name="backup", description="Backup vouches to the specified channel using webhooks.")
    async def backup(self, interaction: discord.Interaction, backup_channel: discord.TextChannel):

        webhook = await backup_channel.create_webhook(name="Vouch Backup")

        
        vouches = self.db.get_all_vouches()

        if not vouches:
            await interaction.response.send_message("No vouches found to back up.", ephemeral=True)
            return

        
        for vouch in vouches:
            
            author = await self.bot.fetch_user(vouch['author_id'])
            vouched_user = await self.bot.fetch_user(vouch['vouched_user_id'])


            vouch_timestamp = datetime.fromisoformat(vouch['timestamp'])

            
            embed = discord.Embed(title="New Vouch Created", description=f"{'⭐' * vouch['rating']}", color=discord.Color.green())
            embed.add_field(name="Vouch:", value=vouch['message'], inline=False)
            embed.add_field(name="Vouched By:", value=author.mention, inline=True)
            embed.add_field(name="Vouched At:", value=discord.utils.format_dt(vouch_timestamp, 'R'), inline=True)
            embed.set_thumbnail(url=vouched_user.display_avatar.url)
            embed.set_footer(text="Vouch System", icon_url=interaction.guild.icon.url)

            
            await webhook.send(
                embed=embed, 
                username=author.name, 
                avatar_url=author.display_avatar.url
            )

        await interaction.response.send_message(f"Backup completed in {backup_channel.mention}.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Backup(bot))
