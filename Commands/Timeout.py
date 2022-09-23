#----------------Required Imports----------------
import aiosqlite
import datetime
import discord

#----------------Further Imports----------------
from discord.ext import commands
from discord import app_commands
from discord.app_commands.checks import has_permissions

#----------------Command Class----------------
class Timeout(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    #--------Timeout Command--------
    app_commands.command(name="timeout", description="Timeout a user to stop them from sending messages")
    @app_commands.choices(duration=[
        app_commands.Choice(name="60 secs", value="60secs"),
        app_commands.Choice(name="5 mins", value="5mins"),
        app_commands.Choice(name="10 mins", value="10mins"),
        app_commands.Choice(name="1 hour", value="1hour"),
        app_commands.Choice(name="1 day", value="1day"),
        app_commands.Choice(name="1 week", value="1week")
    ])
    @has_permissions(moderate_members=True)
    async def timeout(self, interaction: discord.Interaction, user:discord.Member, duration: app_commands.Choice[str], reason: str=None):
        database = await aiosqlite.connect("data.db")
        await database.execute("CREATE TABLE IF NOT EXISTS Modlogs (case_no, type, user_id, moderator_id, reason)")
        async with database.execute(f"SELECT case_no FROM Modlogs ORDER BY case_no DESC LIMIT 1") as cursor:
            data = await cursor.fetchone()
        if data is None:
            case = 1
        else:
            case = int(data[0]) + 1
            print(f"case 2: {case}")

        if duration.value == "60secs":
            await user.timeout(datetime.timedelta(seconds=60), reason=reason)
            await database.execute(f"INSERT INTO Modlogs VALUES ({case}, 'Timeout', {user.id}, {interaction.user.id}, '{reason}')")
            await interaction.response.send_message(content=f"**{user}** has been timedout for 60 seconds!", ephemeral=True)
            await database.commit()
            await database.close()
            return
        
        if duration.value == "5mins":
            await user.timeout(datetime.timedelta(minutes=5), reason=reason)
            await database.execute(f"INSERT INTO Modlogs VALUES ({case}, 'Timeout', {user.id}, {interaction.user.id}, '{reason}')")
            await interaction.response.send_message(content=f"**{user}** has been timedout for 5 minutes!", ephemeral=True)
            await database.commit()
            await database.close()
            return
        
        if duration.value == "10mins":
            await user.timeout(datetime.timedelta(minutes=10), reason=reason)
            await database.execute(f"INSERT INTO Modlogs VALUES ({case}, 'Timeout', {user.id}, {interaction.user.id}, '{reason}')")
            await interaction.response.send_message(content=f"**{user}** has been timedout for 10 minutes!", ephemeral=True)
            await database.commit()
            await database.close()
            return
        
        if duration.value == "1hour":
            await user.timeout(datetime.timedelta(hours=1), reason=reason)
            await database.execute(f"INSERT INTO Modlogs VALUES ({case}, 'Timeout', {user.id}, {interaction.user.id}, '{reason}')")
            await interaction.response.send_message(content=f"**{user}** has been timedout for 1 hour!", ephemeral=True)
            await database.commit()
            await database.close()
            return
        
        if duration.value == "1day":
            await user.timeout(datetime.timedelta(days=1), reason=reason)
            await database.execute(f"INSERT INTO Modlogs VALUES ({case}, 'Timeout', {user.id}, {interaction.user.id}, '{reason}')")
            await interaction.response.send_message(content=f"**{user}** has been timedout for 1 day!", ephemeral=True)
            await database.commit()
            await database.close()
            return
        
        if duration.value == "1week":
            await user.timeout(datetime.timedelta(weeks=1), reason=reason)
            await database.execute(f"INSERT INTO Modlogs VALUES ({case}, 'Timeout', {user.id}, {interaction.user.id}, '{reason}')")
            await interaction.response.send_message(content=f"**{user}** has been timedout for 1 week!", ephemeral=True)
            await database.commit()
            await database.close()
            return

#----------------Cog Setup Function----------------
async def setup(bot: commands.Bot):
    await bot.add_cog(Timeout(bot))