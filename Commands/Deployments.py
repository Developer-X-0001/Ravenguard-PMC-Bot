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
    @app_commands.checks.has_role(config.BOT_OPERATOR_ROLE_ID)
    async def deploy_create(self, interaction: discord.Interaction):
        deployment_embed = discord.Embed(
            title="New Deployment Draft",
            description="You're going to create a new deployment.\nPlease click \"Next\" to proceed, this will bind a unique identifier with this deployment which makes it accessible in future.",
            color=config.RAVEN_RED
        )

        await interaction.response.send_message(embed=deployment_embed, view=DeploymentStartView(), ephemeral=True)

    @deploy_create.error
    async def deploy_create_error(self, interaction: discord.Interaction, error: app_commands.errors):
        if isinstance(error, app_commands.errors.MissingRole):
            await interaction.response.send_message(embed=discord.Embed(description="{} **You aren't authorized to do that!**".format(config.ERROR_EMOJI), color=config.RAVEN_RED), ephemeral=True)
        else:
            raise Exception

    
    @deployments_group.command(name="load", description="Load a previously created deployment.")
    @app_commands.checks.has_role(config.BOT_OPERATOR_ROLE_ID)
    async def deploy_load(self, interaction: discord.Interaction):
        response_embed = discord.Embed(
            title="Deployment Selector",
            description="Please select a previously created a deployment.",
            color=config.RAVEN_RED
        )

        await interaction.response.send_message(embed=response_embed, view=DeploymentSelectView(guild=interaction.guild), ephemeral=True)
    
    @deploy_load.error
    async def deploy_load_error(self, interaction: discord.Interaction, error: app_commands.errors):
        if isinstance(error, app_commands.errors.MissingRole):
            await interaction.response.send_message(embed=discord.Embed(description="{} **You aren't authorized to do that!**".format(config.ERROR_EMOJI), color=config.RAVEN_RED), ephemeral=True)
        else:
            raise Exception

async def setup(bot: commands.Bot):
    await bot.add_cog(Deployments(bot))