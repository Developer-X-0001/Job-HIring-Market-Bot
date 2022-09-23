#----------------Required Imports----------------
import discord

#----------------Further Imports----------------
from discord.ext import commands
from discord import app_commands

#----------------Command Class----------------
class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    #--------Help Command--------
    @app_commands.command(name="help", description="Lists all of the available commands.")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"Commands for {self.bot.user.name}",
            color=self.bot.user.color
        )
        embed.add_field(name="🛡 **__Moderation Commands__**", value="**Kick:**\nKicks the mentioned user from the server.\n**Ban:**\nBans the mentioned user from the server.\n**Unban:**\nUnbans the banned user whos ID is provided.\n**Timeout:**\nTimes-out the mentioned user for a certain duration.\n**Warn:**\nWarns the mentioned user.\n**Warns:**\nShows current warnings of the mentioned user.\n**Pardon:**\nRemove warnings of the mentioned user.\n**Modlog:**\nShow moderation history of a specific user.", inline=False)
        embed.add_field(name="⚙ **__Utility Commands__**", value="**Avatar:**\nShows the avatar of the mentioned user.", inline=False)
        embed.add_field(name="🎭 **__Fun Commands__**", value="**Meme:**\nGenerates a random meme.", inline=False)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text="For further help on a specific command, do /help <command.name>")

        await interaction.response.send_message(embed=embed)

#----------------Cog Setup Function----------------
async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))