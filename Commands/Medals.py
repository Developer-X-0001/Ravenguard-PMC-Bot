import config
import discord

from discord.ext import commands
from discord import app_commands
from Interface.MedalsViews import MedalsSelectView

class Medals(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    medals_group = app_commands.Group(name="medals", description="Commands related to medals management")

    @medals_group.command(name="show", description="Show information about a medal")
    async def medal_show(self, interaction: discord.Interaction):
        medal_embed = discord.Embed(
            description="Please select a medal from the drop-down menu to view it's information",
            colour=config.RAVEN_RED
        )

        await interaction.response.send_message(embed=medal_embed, view=MedalsSelectView())

async def setup(bot: commands.Bot):
    await bot.add_cog(Medals(bot))