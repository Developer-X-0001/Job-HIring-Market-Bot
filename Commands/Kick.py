#----------------Required Imports----------------
import discord
import aiosqlite

#----------------Further Imports----------------
from discord.ext import commands
from discord import app_commands
from discord.app_commands.checks import has_permissions

#----------------Command Class----------------
class Kick(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    #--------Kick Command--------
    @app_commands.command(name="kick", description="Kick a user from the server")
    @has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, user: discord.User, reason:str=None):
        database = await aiosqlite.connect("data.db")
        await database.execute("CREATE TABLE IF NOT EXISTS Modlogs (case_no, type, user_id, moderator_id, reason)")
        if user == interaction.user:
            await interaction.response.send_message(f"You can't kick yourself!", ephemeral=True)
            return
        if reason is None:
            reason = "No Reason Provided"
        try:
            async with database.execute(f"SELECT case_no FROM Modlogs ORDER BY case_no DESC LIMIT 1") as cursor:
                data = await cursor.fetchone()
            if data is None:
                case = 1
            else:
                case = int(data[0]) + 1
            await interaction.guild.kick(user=user, reason=reason)
            await database.execute(f"INSERT INTO Modlogs VALUES ({case}, 'Kick', {user.id}, {interaction.user.id}, '{reason}')")
            await interaction.response.send_message(f"**{user.name}** has been kicked from the server", ephemeral=True)
            await database.commit()
            await database.close()
        except:
            await interaction.response.send_message(f"I'm unable to kick **{user.name}**", ephemeral=True)

    #--------Kick Command Exceptions--------
    @kick.error
    async def kick_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description=f"❌ Missing Permissions, you are missing (Kick Members) permission", color=discord.Color.red()), ephemeral=True)
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description=f"❌ Permission Error, I'm missing (Kick Members) permission", color=discord.Color.red()), ephemeral=True)
        else:
            raise Exception

#----------------Cog Setup Function----------------
async def setup(bot: commands.Bot):
    await bot.add_cog(Kick(bot))