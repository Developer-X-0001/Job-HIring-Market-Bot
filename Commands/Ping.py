#----------------Required Imports----------------
import discord
import aiosqlite
import datetime

#----------------Further Imports----------------
from discord.ext import commands
from discord import app_commands
from discord.app_commands.checks import has_permissions

#----------------Command Class----------------
class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    #--------Ping Command--------
    @app_commands.command(name="ping", description="Shows current bot latency.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(content=f"Latency: `{round(self.bot.latency * 1000)}`ms")


#----------------Cog Setup Function----------------
async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))