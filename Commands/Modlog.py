#----------------Required Imports----------------
import discord
import aiosqlite
import datetime

#----------------Further Imports----------------
from discord.ext import commands
from discord import app_commands
from discord.app_commands.checks import has_permissions

#----------------Command Class----------------
class Modlog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    #--------Modlog Command--------
    @app_commands.command(name="modlogs", description="Check mod logs for a specific user.")
    async def modlog(self, interaction: discord.Interaction, user: discord.Member, page:int=None):
        if page is None:
            page = 1
        database = await aiosqlite.connect("data.db")
        async with database.execute(f"SELECT case_no, type, user_id, moderator_id, reason FROM Modlogs WHERE user_id = {user.id} ORDER BY case_no DESC") as cursor:
            data = await cursor.fetchall()
            print(data)
        
        if len(data) == 0:
            await interaction.response.send_message(embed=discord.Embed(description="Your moderation log is clear. No violations though, stay safe!", color=discord.Color.green()))
            return
        
        page_no = page - 1
        embed = discord.Embed(
            title=f"Modlogs for {user} (Page {page} of {len(data)})",
            description=f"**Case ID {data[page_no][0]}**\n**Type:** {data[page_no][1]}\n**User:** ({data[page_no][2]}) {interaction.guild.get_member(data[page_no][2])}\n**Moderator:** {interaction.guild.get_member(data[page_no][3])}\n**Reason:** {data[page_no][4]}",
            timestamp=datetime.datetime.now(),
            color=discord.Color.teal()
        )
        embed.set_footer(text=f"{len(data)} Cases Found | Use /modlogs [user] [page] to view other pages")
        await interaction.response.send_message(embed=embed)
    
    @modlog.error
    async def modlog_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.CommandInvokeError):
            await interaction.response.send_message(embed=discord.Embed(description="❌ Page index out of range. Please correct the page number.", color=discord.Color.red()), ephemeral=True)

#----------------Cog Setup Function----------------
async def setup(bot: commands.Bot):
    await bot.add_cog(Modlog(bot))