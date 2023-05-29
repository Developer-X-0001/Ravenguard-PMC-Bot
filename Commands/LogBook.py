import discord
from discord.ext import commands
from discord import app_commands

class LogBog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="logbook", description="Check Ravenguard bot logs.")
    async def _logs(self, interation: discord.Interaction):
        print()

async def setup(bot: commands.Bot):
    await bot.add_cog(LogBog(bot))