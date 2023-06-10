import re
import config
import sqlite3
import discord
import asyncio
import datetime

from discord import ButtonStyle
from discord.ui import Button, button, View
from Functions.ColorConverter import hex_to_int

profiles_database = sqlite3.connect("./Databases/profiles.sqlite")
database = sqlite3.connect("./Databases/data.sqlite")

class PointsConfirmButtons(View):
    def __init__(self, message: discord.Message):
        self.original_message = message
        super().__init__(timeout=None)
    
    @button(label="Confirm", emoji=config.DONE_EMOJI, style=ButtonStyle.gray)
    async def confirm_button(self, interaction: discord.Interaction, button: Button):
        embed = interaction.message.embeds[0]
        embed.title = "Changes in Progress"
        embed.footer.text = "Please don't close this message."
        self.confirm_button.disabled = True
        self.confirm_button.label = "Updating Data..."
        self.confirm_button.emoji = config.LOAD_EMOJI
        await interaction.response.edit_message(embed=embed, view=self)

        pattern = r'<@(\d+)>\s+(\d+)'
        matches = re.findall(pattern, self.original_message.content)
        user_count = 0
        for match_point in matches:
            user = interaction.guild.get_member(int(match_point[0]))
            points = match_point[1]
            profiles_database.execute(
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
                    points,
                    points,
                    user.id,
                )
            ).connection.commit()
            user_count += 1
        
        logs_data = database.execute("SELECT logs_channel, status FROM LogSettings WHERE guild_id = ?", (interaction.guild.id,)).fetchone()
        if logs_data is None:
            pass
        else:
            if logs_data[1] == 'disabled':
                pass
            if logs_data[1] == 'enabled':
                given_users = ""
                for match in matches:
                    user = interaction.guild.get_member(int(match[0]))
                    given_users += "{} {}\n".format(user.mention, match[1])
                
                total_points = 0
                for match in matches:
                    total_points += int(match[1])

                logs_channel = interaction.guild.get_channel(logs_data[0])
                logs_embed = discord.Embed(
                    title="Points Update Log",
                    description="This action took place @ <t:{timestamp}:F> (<t:{timestamp}:R>)".format(timestamp=round(datetime.datetime.now().timestamp())),
                    color=config.RAVEN_RED
                )
                logs_embed.add_field(
                    name="Action Type:",
                    value="Batch Update",
                    inline=False
                )
                logs_embed.add_field(
                    name="Points Given By:",
                    value=interaction.user.mention,
                    inline=False
                )
                logs_embed.add_field(
                    name="Points Given To:",
                    value=given_users,
                    inline=False
                )
                logs_embed.add_field(
                    name="Total Points Given:",
                    value="{} ({} Users)".format(total_points, user_count),
                    inline=False
                )
                logs_embed.add_field(
                    name="Message Jump URL:",
                    value=self.original_message.jump_url,
                    inline=False
                )
                await logs_channel.send(embed=logs_embed)

        await asyncio.sleep(1)
        await interaction.edit_original_response(embed=discord.Embed(description="{} Update successful!".format(config.DONE_EMOJI), color=config.RAVEN_RED), view=None)
        await self.original_message.add_reaction(config.DONE_EMOJI)
