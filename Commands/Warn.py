#----------------Required Imports----------------
import aiosqlite
import discord
import datetime

#----------------Further Imports----------------
from discord.ext import commands
from discord import app_commands

#----------------Command Class----------------
class Warn(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    #--------Warn Command--------
    @app_commands.command(name="warn", description="Warn a member in your server")
    @app_commands.checks.has_permissions(administrator=True)
    async def warn(self, interaction: discord.Interaction, user: discord.User, warning:str):
        warnDB = await aiosqlite.connect("data.db")
        async with warnDB.execute(f"SELECT case_no FROM Modlogs ORDER BY case_no DESC LIMIT 1") as cursor:
            data = await cursor.fetchone()
        if data is None:
            case = 1
        else:
            case = int(data[0]) + 1
        async with warnDB.execute(f"SELECT warns FROM Warnings WHERE user_id = {user.id}") as cursor:
            data = await cursor.fetchone()
            print(data[0])
        if data is None:
            await warnDB.execute(f"INSERT INTO Modlogs VALUES ({case}, 'Warning', {user.id}, {interaction.user.id}, '{warning}')")
            await warnDB.execute(f"INSERT INTO Warnings VALUES ({user.id}, 1)")
            await warnDB.commit()
            await warnDB.close()
            await interaction.response.send_message(f"✅ **{user}** has been warned for {warning}", ephemeral=True)
            try:
                await user.send(f"You have been warned in **{interaction.guild.name}** for `{warning}`")
            except:
                pass
            return
        if data[0] > 6:
            await interaction.guild.get_member(user.id).timeout(datetime.timedelta(days=3), reason="Exceeded Warning Limit")
            await interaction.response.send_message(f"⚠ **{user}** has been timed-out for 3 days for having more than 6 warnings", ephemeral=True)
            await warnDB.execute(f"DELETE FROM Warnings WHERE user_id = {user.id}")
            await warnDB.commit()
            await warnDB.close()
            return
        else:
            await warnDB.execute(f"INSERT INTO Modlogs VALUES ({case}, 'Warning', {user.id}, {interaction.user.id}, '{warning}')")
            await warnDB.execute(f"UPDATE Warnings SET warns = warns + 1 WHERE user_id = {user.id}")
            await warnDB.commit()
            await warnDB.close()
            await interaction.response.send_message(f"✅ **{user}** has been warned for {warning}", ephemeral=True)
            try:
                await user.send(f"You have been warned in **{interaction.guild.name}** for `{warning}`")
            except:
                pass
    
    #--------My Warns Command--------
    @app_commands.command(name="check_warnings", description="Check your warnings")
    async def my_warns(self, interaction: discord.Interaction, user: discord.User = None):
        warnDB = await aiosqlite.connect("data.db")
        if user is None:
            user = interaction.user

        async with warnDB.execute(f"SELECT warns FROM Warnings WHERE user_id = {user.id}") as cursor:
            data = await cursor.fetchone()    
        if data is None:
            await interaction.response.send_message(f"**{user}** don't have any warnings", ephemeral=True)
            await warnDB.close()
        else:
            if data[0] == 6:
                await interaction.response.send_message(f"**{user}** have `6/6` warnings, one more warn and they are out of this server!", ephemeral=True)
                await warnDB.close()
            else:
                await interaction.response.send_message(f"**{user}** have `{data[0]}/6` warnings")
                await warnDB.close()
    
    #--------Pardon Command--------
    @app_commands.command(name="pardon", description="Remove a warning or all warnings from a user")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.choices(pardon=[
        app_commands.Choice(name="All", value="all"),
        app_commands.Choice(name="1", value="1"),
        app_commands.Choice(name="2", value="2"),
        app_commands.Choice(name="3", value="3"),
        app_commands.Choice(name="4", value="4"),
        app_commands.Choice(name="5", value="5"),
        app_commands.Choice(name="6", value="6")
    ])
    async def pardon(self, interaction: discord.Interaction, user: discord.User, pardon: app_commands.Choice[str]):
        warnDB = await aiosqlite.connect("data.db")
        async with warnDB.execute(f"SELECT warns FROM Warnings WHERE user_id = {user.id}") as cursor:
            data = await cursor.fetchone()
        if pardon.value == "all":
            if data is None:
                await interaction.response.send_message(f"⚠ **{user}** doesn't have any warnings", ephemeral=True)
            else:
                await warnDB.execute(f"DELETE FROM Warnings WHERE user_id = {user.id}")
                await warnDB.commit()
                await warnDB.close()
                await interaction.response.send_message(f"✅ Removed all warnings from **{user}**", ephemeral=True)
        
        if pardon.value == 1:
            if data is None:
                await interaction.response.send_message(f"⚠ **{user}** doesn't have any warnings", ephemeral=True)
            else:
                if data[0] == 1:
                    await warnDB.execute(f"DELETE FROM Warnings WHERE user_id = {user.id}")
                    await warnDB.commit()
                    await warnDB.close()
                    await interaction.response.send_message(f"✅ Removed all warnings from **{user}**", ephemeral=True)
                if data[0] > 1:
                    await warnDB.execute(f"UPDATE Warnings SET warns = warns - 1 WHERE user_id = {user.id}")
                    await warnDB.commit()
                    await warnDB.close()
                    await interaction.response.send_message(f"✅ Removed `1` warning from **{user}'s** warnings", ephemeral=True)

        if pardon.value == 2:
            if data is None:
                await interaction.response.send_message(f"⚠ **{user}** doesn't have any warnings", ephemeral=True)
            else:
                if data[0] == 2 or data[0] == 1:
                    await warnDB.execute(f"DELETE FROM Warnings WHERE user_id = {user.id}")
                    await warnDB.commit()
                    await warnDB.close()
                    await interaction.response.send_message(f"✅ Removed all warnings from **{user}**", ephemeral=True)
                if data[0] > 2:
                    await warnDB.execute(f"UPDATE Warnings SET warns = warns - 1 WHERE user_id = {user.id}")
                    await warnDB.commit()
                    await warnDB.close()
                    await interaction.response.send_message(f"✅ Removed `1` warning from **{user}'s** warnings", ephemeral=True)
        
        if pardon.value == 3:
            if data is None:
                await interaction.response.send_message(f"⚠ **{user}** doesn't have any warnings", ephemeral=True)
            else:
                if data[0] == 3 or data[0] == 1:
                    await warnDB.execute(f"DELETE FROM Warnings WHERE user_id = {user.id}")
                    await warnDB.commit()
                    await warnDB.close()
                    await interaction.response.send_message(f"✅ Removed all warnings from **{user}**", ephemeral=True)
                if data[0] > 3:
                    await warnDB.execute(f"UPDATE Warnings SET warns = warns - 1 WHERE user_id = {user.id}")
                    await warnDB.commit()
                    await warnDB.close()
                    await interaction.response.send_message(f"✅ Removed `1` warning from **{user}'s** warnings", ephemeral=True)
        
        if pardon.value == 4:
            if data is None:
                await interaction.response.send_message(f"⚠ **{user}** doesn't have any warnings", ephemeral=True)
            else:
                if data[0] == 4 or data[0] == 1:
                    await warnDB.execute(f"DELETE FROM Warnings WHERE user_id = {user.id}")
                    await warnDB.commit()
                    await warnDB.close()
                    await interaction.response.send_message(f"✅ Removed all warnings from **{user}**", ephemeral=True)
                if data[0] > 4:
                    await warnDB.execute(f"UPDATE Warnings SET warns = warns - 1 WHERE user_id = {user.id}")
                    await warnDB.commit()
                    await warnDB.close()
                    await interaction.response.send_message(f"✅ Removed `1` warning from **{user}'s** warnings", ephemeral=True)
        
        if pardon.value == 5:
            if data is None:
                await interaction.response.send_message(f"⚠ **{user}** doesn't have any warnings", ephemeral=True)
            else:
                if data[0] == 5 or data[0] == 1:
                    await warnDB.execute(f"DELETE FROM Warnings WHERE user_id = {user.id}")
                    await warnDB.commit()
                    await warnDB.close()
                    await interaction.response.send_message(f"✅ Removed all warnings from **{user}**", ephemeral=True)
                if data[0] > 5:
                    await warnDB.execute(f"UPDATE Warnings SET warns = warns - 1 WHERE user_id = {user.id}")
                    await warnDB.commit()
                    await warnDB.close()
                    await interaction.response.send_message(f"✅ Removed `1` warning from **{user}'s** warnings", ephemeral=True)
        
        if pardon.value == 6:
            if data is None:
                await interaction.response.send_message(f"⚠ **{user}** doesn't have any warnings", ephemeral=True)
            else:
                if data[0] == 6 or data[0] == 1:
                    await warnDB.execute(f"DELETE FROM Warnings WHERE user_id = {user.id}")
                    await warnDB.commit()
                    await warnDB.close()
                    await interaction.response.send_message(f"✅ Removed all warnings from **{user}**", ephemeral=True)
                if data[0] > 6:
                    await warnDB.execute(f"UPDATE Warnings SET warns = warns - 1 WHERE user_id = {user.id}")
                    await warnDB.commit()
                    await warnDB.close()
                    await interaction.response.send_message(f"✅ Removed `1` warning from **{user}'s** warnings", ephemeral=True)

#----------------Cog Setup Function----------------
async def setup(bot: commands.Bot):
    await bot.add_cog(Warn(bot))