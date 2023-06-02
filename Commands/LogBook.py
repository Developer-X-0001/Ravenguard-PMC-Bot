import config
import sqlite3
import discord

from discord.ext import commands
from discord import app_commands
from Interface.LogsConfigureView import LogsConfigureButton

class LogBog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.database = sqlite3.connect("./Databases/data.sqlite")

    logs_group = app_commands.Group(name="logs", description="Commands related to logging")

    @logs_group.command(name="config", description="Configure points logging system.")
    async def logs_config(self, interaction: discord.Interaction):
        data = self.database.execute("SELECT logs_channel, status FROM LogSettings WHERE guild_id = ?", (interaction.guild.id,)).fetchone()
        settings_embed = discord.Embed(
            title="Ravenguard Bot Logs Configuration",
            description="Here you can configure your points logging preferences.",
            color=config.RAVEN_RED
        )
        settings_embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/DgUaEQpz7R97PAF_1ioQafZfsZ5WKrh3Fp2Vl7frGtY/%3Fsize%3D512/https/cdn.discordapp.com/icons/1041533895268651038/8795824b3873a3e88e8070b68ec851a4.png")
        if data is None:
            settings_embed.add_field(
                name="Logs Channel:",
                value="Not Specified",
                inline=True
            )
            settings_embed.add_field(
                name="Logging Status:",
                value="Disabled (No Channel Set)",
                inline=True
            )
        else:
            settings_embed.add_field(
                name="Logs Channel:",
                value="{}".format(interaction.guild.get_channel(data[0]).mention),
                inline=True
            )
            settings_embed.add_field(
                name="Logging Status:",
                value="{}".format(str(data[1]).capitalize()),
                inline=True
            )

        await interaction.response.send_message(embed=settings_embed, view=LogsConfigureButton(), ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(LogBog(bot))