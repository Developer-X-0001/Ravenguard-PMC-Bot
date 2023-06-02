import discord
from discord.ext import commands
from discord import app_commands

class Deployments(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    deployments_group = app_commands.Group(name="deployments", description="Commands related to managing and configuring deployments.")

    @deployments_group.command(name="create", description="Create a new deployment")
    async def deploy_create(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=""
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(Deployments(bot))