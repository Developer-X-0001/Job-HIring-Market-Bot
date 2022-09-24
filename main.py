#----------------Required Imports----------------
import aiosqlite
import discord
import config
import os

#----------------Further Imports----------------
from discord.ext import commands

#----------------Bot Class----------------
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=config.PREFIX,
            intents=discord.Intents.all(),
            activity=discord.Activity(type=discord.ActivityType.listening, name="/help")
        )
    
    async def setup_hook(self):
        for filename in os.listdir("./Commands"):
            if filename.endswith(".py"):
                await self.load_extension(f"Commands.{filename[:-3]}")
                print(f"Loaded {filename}")
            
            else:
                pass
        
        await bot.tree.sync()

bot = Bot()

#----------------On Ready Event----------------
@bot.event
async def on_ready():
    database = await aiosqlite.connect("data.db")
    await database.execute("CREATE TABLE IF NOT EXISTS Warnings (user_id, warns, PRIMARY KEY (user_id))")
    await database.execute("CREATE TABLE IF NOT EXISTS Modlogs (case_no, type, user_id, moderator_id, reason)")
    await database.close()
    print(f"Logged in as: {bot.user}")
    print(f"Client ID: {bot.user.id}")
    print(f"Latency: {round(bot.latency * 1000)}ms")

#----------------Cog Reload Command----------------
@bot.command(name="reload")
async def reload(ctx: commands.Context, cog: str):
    await ctx.message.delete()
    if cog is None:
        await ctx.send("⚠ Please provide a cog name!", delete_after=5)
        return
    
    await bot.reload_extension(f"Commands.{cog}")
    await ctx.send(f"🔁 {cog} reloaded!", delete_after=5)

@reload.error
async def reload_error(ctx: commands.Context, error):
    if isinstance(error, commands.errors.BadArgument):
        await ctx.send("⚠ Invalid Cog Name!", delete_after=5)
    else:
        raise Exception

#----------------Re-sync Command----------------
@bot.command(name="resync")
async def resync(ctx: commands.Context):
    await bot.tree.sync()
    await ctx.send("✅ Re-sync complete", delete_after=5)

#----------------Logging into the Bot----------------
bot.run(config.TOKEN)
