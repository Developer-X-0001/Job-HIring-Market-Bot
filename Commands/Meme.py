#----------------Required Imports----------------
import discord
import random
import aiohttp

#----------------Further Imports----------------
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button, button
from discord import ButtonStyle

#----------------Button Class----------------

class MemeButtons(View):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(timeout=30)
        self.latest_interaction = interaction
    
    async def interaction_check(self, interaction: discord.Interaction):
        result = await super().interaction_check(interaction)  # or your own condition
        self.latest_interaction = interaction
        if not result:
            await interaction.response.defer()
        return result

    async def on_timeout(self):
        self.meme_gen_button.disabled = True
        self.int_stop_button.disabled = True

        await self.latest_interaction.edit_original_response(view=self)

    @button(label="Generate More", style=ButtonStyle.green, custom_id="meme_gen_button")
    async def meme_gen_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://www.reddit.com/r/memes.json") as r:
                memes = await r.json()
                embed = discord.Embed(
                    color=discord.Color.random()
                )
                embed.set_image(url=memes["data"]["children"][random.randint(0, 25)]["data"]["url"])
        
        await interaction.edit_original_response(embed=embed, view=MemeButtons(interaction=interaction))
    
    @button(label="Stop Interaction", style=ButtonStyle.red, custom_id="int_stop_button")
    async def int_stop_button(self, interaction: discord.Interaction, button: Button):
        self.int_stop_button.disabled = True
        self.meme_gen_button.disabled = True
        await interaction.response.edit_message(view=self)

#----------------Command Class----------------
class Meme(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    #--------Meme Command--------
    @app_commands.command(name="meme", description="Get a random funny meme.")
    async def meme(self, interaction: discord.Interaction):
        await interaction.response.defer()
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://www.reddit.com/r/memes.json") as r:
                memes = await r.json()
                embed = discord.Embed(
                    color=discord.Color.random()
                )
                embed.set_image(url=memes["data"]["children"][random.randint(0, 25)]["data"]["url"])
                await interaction.followup.send(embed=embed, view=MemeButtons(interaction=interaction))

#----------------Cog Setup Function----------------
async def setup(bot: commands.Bot):
    await bot.add_cog(Meme(bot))