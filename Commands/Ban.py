#----------------Required Imports----------------
import discord
import aiosqlite

#----------------Further Imports----------------
from discord.ext import commands
from discord import app_commands
from discord.app_commands.checks import has_permissions

#----------------Command Class----------------
class Ban(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #--------Ban Command--------
    @app_commands.command(name="ban", description="Ban a member from the server")
    @has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, user: discord.User, reason:str=None):
        database = await aiosqlite.connect("data.db")
        await database.execute("CREATE TABLE IF NOT EXISTS Modlogs (case_no, type, user_id, moderator_id, reason)")
        if user == interaction.user:
            await interaction.response.send_message(content="❌ You can't ban yourself!", ephemeral=True)
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

            await interaction.guild.ban(user=user, reason=reason)
            await database.execute(f"INSERT INTO Modlogs VALUES ({case}, 'Ban', {user.id}, {interaction.user.id}, '{reason}')")
            await interaction.response.send_message(content=f"✅ **{user.name}**, has been banned from the server.")
            await database.commit()
            await database.close()
        except app_commands.MissingPermissions:
            await interaction.response.send_message("⚠️ Sorry, I don't have **(Ban Members)** permissions.")

    #--------Ban Command Exceptions--------
    @ban.error
    async def ban_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description=f"❌ Missing Permissions, you are missing (Ban Members) permission", color=discord.Color.red()), ephemeral=True)
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description=f"❌ Permission Error, I'm missing (Ban Members) permission", color=discord.Color.red()), ephemeral=True)
        else:
            raise Exception
    
    #--------------------------------------

    #--------Unban Command--------
    @app_commands.command(name="unban", description="Unban a member from the server")
    @has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id:str, reason:str=None):
        database = await aiosqlite.connect("data.db")
        await database.execute("CREATE TABLE IF NOT EXISTS Modlogs (case_no, type, user_id, moderator_id, reason)")
        if reason is None:
            reason = "No Reason Provided"
        try:
            async with database.execute(f"SELECT case_no FROM Modlogs ORDER BY case_no DESC LIMIT 1") as cursor:
                data = await cursor.fetchone()
            if data is None:
                case = 1
            else:
                case = int(data[0]) + 1

            user = await self.bot.fetch_user(user_id)
            print(user)
            print(user.id)
            await interaction.guild.unban(user, reason=reason)
            await database.execute(f"INSERT INTO Modlogs VALUES ({case}, 'Unban', {user.id}, {interaction.user.id}, '{reason}')")
            await interaction.response.send_message(f'✅ **{user}** has been unbanned from the server!', ephemeral=True)
            await database.commit()
            await database.close()
        except NameError:
            await interaction.response.send_message(f"❌ The user isn't banned!", ephemeral=True)
    
    #--------Unban Command Exceptions--------
    @unban.error
    async def unban_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description=f"❌ Missing Permissions, you are missing (Ban Members) permission", color=discord.Color.red()), ephemeral=True)
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description=f"❌ Permission Error, I'm missing (Ban Members) permission", color=discord.Color.red()), ephemeral=True)
        else:
            raise Exception

#----------------Cog Setup Function----------------
async def setup(bot: commands.Bot):
    await bot.add_cog(Ban(bot))