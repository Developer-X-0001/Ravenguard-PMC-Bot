import config
import sqlite3
import discord

from discord import ButtonStyle
from discord.ui import Button, button, View, select, ChannelSelect, Select

database = sqlite3.connect("./Databases/data.sqlite")

class LogsConfigureButton(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Configure", emoji=config.SETTINGS_EMOJI, style=ButtonStyle.gray)
    async def logs_configure_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=LogsConfigurationViews())

class LogsConfigurationViews(View):
    def __init__(self):
        super().__init__(timeout=None)

    @select(cls=ChannelSelect, channel_types=[discord.ChannelType.text], placeholder="Set Logs Channel", min_values=1, max_values=1, row=0)
    async def LogsChannelSelect(self, interaction: discord.Interaction, select: ChannelSelect):
        settings_embed = interaction.message.embeds[0]
        settings_embed.set_field_at(
            index=0,
            name=settings_embed.fields[0].name,
            value=select.values[0].mention,
            inline=True
        )
        database.execute("INSERT INTO LogSettings VALUES (?, ?, ?) ON CONFLICT DO UPDATE SET logs_channel = ? WHERE guild_id = ?",
                         (interaction.guild.id, select.values[0].id, 'disabled', select.values[0].id, interaction.guild.id,)).connection.commit()
        data = database.execute("SELECT status FROM LogSettings WHERE guild_id = ?", (interaction.guild.id,)).fetchone()
        settings_embed.set_field_at(
            index=1,
            name=settings_embed.fields[1].name,
            value=str(data[0]).capitalize(),
            inline=True
        )
        await interaction.response.edit_message(embed=settings_embed)
    
    @button(label="Enable/Disable Logging", style=ButtonStyle.gray)
    async def change_logging_button(self, interaction: discord.Interaction, button: Button):
        settings_embed = interaction.message.embeds[0]
        data = database.execute("SELECT logs_channel, status FROM LogSettings WHERE guild_id = ?", (interaction.guild.id,)).fetchone()
        if data is None:
            await interaction.response.send_message(embed=discord.Embed(description="{} Please set a logs channel first!".format(config.WARN_EMOJI), color=config.RAVEN_RED), ephemeral=True)

        else:
            if str(data[1]).lower() == 'enabled':
                settings_embed.set_field_at(
                    index=1,
                    name=settings_embed.fields[1].name,
                    value="Disabled",
                    inline=True
                )
                database.execute("UPDATE LogSettings SET status = ? WHERE guild_id = ?", ('disabled', interaction.guild.id,)).connection.commit()
            if str(data[1]).lower() == 'disabled':
                settings_embed.set_field_at(
                    index=1,
                    name=settings_embed.fields[1].name,
                    value="Enabled",
                    inline=True
                )
                database.execute("UPDATE LogSettings SET status = ? WHERE guild_id = ?", ('enabled', interaction.guild.id,)).connection.commit()

            await interaction.response.edit_message(embed=settings_embed)
        
    @button(label="Go Back", emoji=config.BACK_EMOJI, style=ButtonStyle.gray)
    async def go_back_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(view=LogsConfigureButton())