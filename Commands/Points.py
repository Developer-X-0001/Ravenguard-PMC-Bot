import re
import config
import sqlite3
import discord

from discord.ext import commands
from discord import app_commands
from Functions.ColorConverter import hex_to_int
from Interface.PointsConfirmView import PointsConfirmButtons

database = sqlite3.connect("./Databases/profiles.sqlite")

class Points(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="addpoints", description="Add points to a user.")
    @app_commands.checks.has_role(config.BOT_OPERATOR_ROLE_ID)
    async def add_points(self, interaction: discord.Interaction, amount: int, users: str):
        pattern = r'<@(\d+)>'

        matches = re.findall(pattern, users)

        data = ""

        for match in matches:
            user = interaction.guild.get_member(int(match))
            data += "{} **Username:** {} | **Points:** {}+\n".format(config.ARROW_EMOJI, user.mention, amount)
            
            database.execute(
                '''
                    INSERT INTO UserProfiles VALUES (?, ?, ?, ?)
                    ON CONFLICT(
                        user_id
                    ) DO UPDATE SET
                    points = points + ?
                    WHERE user_id = ?
                ''',
                (
                    user.id,
                    "Bio and embed color isn't configurable yet",
                    hex_to_int(hex_code="FFFFFF"),
                    amount,
                    amount,
                    user.id,
                )
            ).connection.commit()

        points_embed = discord.Embed(
            title="Successfully Updated Points",
            description=data,
            color=config.RAVEN_RED
        )
        await interaction.response.send_message(embed=points_embed)
    
    @add_points.error
    async def app_points_error(self, interaction: discord.Interaction, error: app_commands.errors):
        if isinstance(error, app_commands.errors.MissingRole):
            await interaction.response.send_message(embed=discord.Embed(description="{} **You aren't authorized to do that!**".format(config.ERROR_EMOJI), color=config.RAVEN_RED), ephemeral=True)
        else:
            raise Exception

    @app_commands.command(name="removepoints", description="Remove points from users.")
    @app_commands.checks.has_role(config.BOT_OPERATOR_ROLE_ID)
    async def remove_points(self, interaction: discord.Interaction, amount: int, users: str):
        pattern = r'<@(\d+)>'

        matches = re.findall(pattern, users)

        data = ""

        for match in matches:
            user = interaction.guild.get_member(int(match))
            data += "{} **Username:** {} | **Points:** {}+\n".format(config.ARROW_EMOJI, user.mention, amount)
        
            database.execute(
                '''
                    INSERT INTO UserProfiles VALUES (?, ?, ?, ?)
                    ON CONFLICT(
                        user_id
                    ) DO UPDATE SET
                    points = points - ?
                    WHERE user_id = ?
                ''',
                (
                    user.id,
                    "Bio and embed color isn't configurable yet",
                    hex_to_int(hex_code="FFFFFF"),
                    amount,
                    amount,
                    user.id,
                )
            ).connection.commit()

        points_embed = discord.Embed(
            title="Successfully Updated Points",
            description=data,
            color=config.RAVEN_RED
        )
        await interaction.response.send_message(embed=points_embed)
    
    @remove_points.error
    async def remove_points_error(self, interaction: discord.Interaction, error: app_commands.errors):
        if isinstance(error, app_commands.errors.MissingRole):
            await interaction.response.send_message(embed=discord.Embed(description="{} **You aren't authorized to do that!**".format(config.ERROR_EMOJI), color=config.RAVEN_RED), ephemeral=True)
        else:
            raise Exception


async def setup(bot: commands.Bot):
    await bot.add_cog(Points(bot))