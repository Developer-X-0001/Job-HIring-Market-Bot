#----------------Required Imports----------------
import discord

#----------------Further Imports----------------
from discord.ext import commands
from discord import app_commands

#----------------Command Class----------------
class Rules(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    #--------Rules Command--------
    @app_commands.command(name="rules", description="Show rules")
    async def rules(self, interaction: discord.Interaction, rule:str=None):
        if rule is None:
            await interaction.response.send_message("LoL", ephemeral=True)
            return
        if rule == "No NSFW":
            rule_index = 1
            rule_title = "No NSFW"
            rule_content = "There will be no tolerance for NSFW or NSFL content or discussions. This includes usernames/nicknames and avatars."
        
        if rule == "No Inappropriate Language":
            rule_index = 2
            rule_title = "No Inappropriate Language"
            rule_content = "To some extent, mild profanity is permitted, but certain words are prohibited just in case. And using those words will result in you being muted."
        
        if rule == "Be respectful":
            rule_index = 3
            rule_title = "Be respectful"
            rule_content = "You must respect all users, regardless of your liking towards them. Treat others the way you want to be treated. Also, any derogatory language towards any user is prohibited. This includes threats to other users of DDoS, Death, DoX, abuse, and other malicious threats"
            
        if rule == "No inappropriate names and avatars":
            rule_index = 4
            rule_title = "No inappropriate names and avatars"
            rule_content = "Avatars with brightly flashing colors, as well as names and avatars that are inappropriate or offensive, are not permitted."
        
        if rule == "Don't talk on jobs ads channel":
            rule_index = 5
            rule_title = "Don't talk on jobs ads channel"
            rule_content = "People will post ads on the jobs channel if you are interested in that job or want to hire that guy don't direct replay him on the jobs channel you can dm him or go to #work chat and ask there."

        if rule == "Use English only":
            rule_index = 6
            rule_title = "Use English only"
            rule_content = "Because we cannot moderate chat in any other language besides English, you must use English at all times. However, occasional use while remaining relevant to the ongoing topic is acceptable."
        
        if rule == "Staff may moderate at their discretion":
            rule_index = 7
            rule_title = "Staff may moderate at their discretion"
            rule_content = "Nothing, including our set of rules, is perfect. We reserve the right to moderate anything not on this list that we deem inappropriate. Use common sense and refrain from complaining when the staff team attempts to keep the server calm and safe."
        
        embed = discord.Embed(
            title=f"**`Rule {rule_index}` {rule_title}**",
            description=rule_content,
            color=discord.Color.from_rgb(255, 255, 255)
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/964964856103055460/1022575979161464903/JOB.png")

        await interaction.response.send_message(embed=embed)

    @rules.autocomplete(name="rule")
    async def autocomplete_callback(self, interaction: discord.Interaction, current: str):
        print(current)

        return [
            app_commands.Choice(name="No NSFW", value="No NSFW"),
            app_commands.Choice(name="No Inappropriate Language", value="No Inappropriate Language"),
            app_commands.Choice(name="Be respectful", value="Be respectful"),
            app_commands.Choice(name="No inappropriate names and avatars", value="No inappropriate names and avatars"),
            app_commands.Choice(name="Don't talk on jobs ads channel", value="Don't talk on jobs ads channel"),
            app_commands.Choice(name="Use English only", value="Use English only"),
            app_commands.Choice(name="Staff may moderate at their discretion", value="Staff may moderate at their discretion")
            ]

#----------------Cog Setup Function----------------
async def setup(bot: commands.Bot):
    await bot.add_cog(Rules(bot))