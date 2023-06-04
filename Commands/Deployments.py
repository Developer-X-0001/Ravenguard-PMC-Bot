import config
import sqlite3
import discord

from discord.ext import commands
from discord import app_commands
from Interface.DeploymentCreateView import DeploymentStartView
from Interface.DeploymentLoadView import DeploymentSelectView

class Deployments(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    deployments_group = app_commands.Group(name="deployments", description="Commands related to managing and configuring deployments.")

    @deployments_group.command(name="create", description="Create a new deployment")
    async def deploy_create(self, interaction: discord.Interaction):
        deployment_embed = discord.Embed(
            title="New Deployment Draft",
            description="You're going to create a new deployment.\nPlease click \"Next\" to proceed, this will bind a unique identifier with this deployment which makes it accessible in future.",
            color=config.RAVEN_RED
        )

        await interaction.response.send_message(embed=deployment_embed, view=DeploymentStartView())
    
    @deployments_group.command(name="load", description="Load a previously created deployment.")
    async def deploy_load(self, interaction: discord.Interaction):
        response_embed = discord.Embed(
            title="Deployment Selector",
            description="Please select a previously created a deployment.",
            color=config.RAVEN_RED
        )

        await interaction.response.send_message(embed=response_embed, view=DeploymentSelectView(guild=interaction.guild))

async def setup(bot: commands.Bot):
    await bot.add_cog(Deployments(bot))