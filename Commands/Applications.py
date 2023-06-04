import discord
from discord.ext import commands
from discord import app_commands

class Application(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="apply", description="Apply to become a personnel in Ravenguard PMC")
    async def apply(self, interaction: discord.Interaction):
        application_embed = discord.Embed(
            title="Ravenguard PMC Application"
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(Application(bot))