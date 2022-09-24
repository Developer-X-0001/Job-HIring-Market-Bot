#----------------Required Imports----------------
import discord

#----------------Further Imports----------------
from discord.ext import commands
from discord import app_commands
from discord.app_commands.checks import has_permissions

#----------------Command Class----------------
class Clean(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    #--------Clean Command--------
    @app_commands.command(name="clean", description="Delete any number of messages.")
    @has_permissions(manage_messages=True)
    async def clean(self, interaction: discord.Interaction, amount: int=None):
        await interaction.response.defer(ephemeral=True)
        if amount is None:
            amount = 5

        if amount > 100:
            await interaction.followup.send("⚠ You can't delete more than 100 messages at once.")
            return
        if amount <= 0:
            await interaction.followup.send("⚠ 0? What do you expect from me?")
            return
        
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(f"Deleted `{len(deleted)}/{amount}` messages.")


#----------------Cog Setup Function----------------
async def setup(bot: commands.Bot):
    await bot.add_cog(Clean(bot))