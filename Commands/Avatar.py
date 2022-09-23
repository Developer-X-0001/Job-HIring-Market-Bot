#----------------Required Imports----------------
import discord
import datetime

#----------------Further Imports----------------
from discord.ext import commands
from discord import app_commands
from discord.app_commands.checks import has_permissions

#----------------Command Class----------------
class Avatar(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    #--------Avatar Command--------
    @app_commands.command(name="avatar", description="Get avatar of the mentioned user.")
    @app_commands.describe(user="User whos avatar you are going to get.", privacy="Choose wether the avatar is sent publicly or privately. Default: Public")
    @app_commands.choices(privacy=[
        app_commands.Choice(name="Public", value=1),
        app_commands.Choice(name="Private", value=2)
    ])
    async def avatar(self, interaction: discord.Interaction, user: discord.Member, privacy: app_commands.Choice[int]=None):
        embed = discord.Embed(
            title=f"{user.name}'s Avatar",
            color=user.color,
            timestamp=datetime.datetime.now()
        )
        embed.set_image(url=user.avatar.url)

        if privacy is None:
            embed.set_footer(text=f"Requested by {interaction.user.name}")
            await interaction.response.send_message(embed=embed)
            return
        
        if privacy.value == 1:
            embed.set_footer(text=f"Requested by {interaction.user.name}")
            await interaction.response.send_message(embed=embed)
            return

        if privacy.value == 2:
            embed.set_footer(text=f"Requested privately 🤫")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

#----------------Cog Setup Function----------------
async def setup(bot: commands.Bot):
    await bot.add_cog(Avatar(bot))