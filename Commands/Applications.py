import config
import discord

from discord.ext import commands
from discord import app_commands
from Interface.ApplicationModal import ApplicationModal

class Application(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="apply", description="Apply to become a personnel in Ravenguard PMC")
    @app_commands.checks.has_role(config.VERIFIED_ROLE_ID)
    async def apply(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ApplicationModal())
    
    @apply.error
    async def apply_error(self, interaction: discord.Interaction, error: app_commands.errors):
        if isinstance(error, app_commands.errors.MissingRole):
            await interaction.response.send_message(embed=discord.Embed(description="{} **You aren't authorized to do that!**".format(config.ERROR_EMOJI), color=config.RAVEN_RED), ephemeral=True)
        else:
            raise Exception

async def setup(bot: commands.Bot):
    await bot.add_cog(Application(bot))