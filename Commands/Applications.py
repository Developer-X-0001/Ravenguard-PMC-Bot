import discord

from discord.ext import commands
from discord import app_commands
from Interface.ApplicationModal import ApplicationModal

class Application(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="apply", description="Apply to become a personnel in Ravenguard PMC")
    async def apply(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ApplicationModal())

async def setup(bot: commands.Bot):
    await bot.add_cog(Application(bot))